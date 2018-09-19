"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import os
import shutil
import re
import zipfile
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import xml.etree.cElementTree as ET
from wui.core.core_utils import core_utils
from native.wapp_management.wapp_management_utils.app_validator import AppValidator
from native.wapp_management.wapp_management_utils.installer import Installer
from native.wapp_management.wapp_management_utils.uninstaller import Uninstaller
from utils.directory_traversal_utils import join_path, get_sub_files, get_parent_directory, \
    create_dir, get_dir_from_path
from utils.file_utils import copy_dir
from utils.navigator_util import Navigator
from utils.string_utils import get_repository_name
from wui.core.core_utils.app_info_class import AppInformation
from katana.utils.user_utils import UserData

from katana.native.wapp_management import apps

from katana.native.wapp_management.wapp_management_utils import wapp_mgmt_utils

#from katana.utils import file_utils
nav_obj = Navigator()

# path to katana/static
# define as a global variable
katana_static = join_path(nav_obj.get_katana_dir(), 'static')

class WappManagementView(View):
    template = 'wapp_management/wapp_management.html'
    dot_data_directory = join_path(nav_obj.get_katana_dir(), "native", "wapp_management", ".data")

    def get(self, request):
        """
        Get Request Method
        """
        files = get_sub_files(WappManagementView.dot_data_directory)
        preferences = []
        for subfile in files:
            filename, file_extension = os.path.splitext(subfile)
            if file_extension == ".xml":
                preferences.append(filename)
        output = {"data": {"app": AppInformation.information.apps, "preferences": preferences}}
        return render(request, WappManagementView.template, output)


def update_installed_apps_section(request):
    output = {"data": {"app": AppInformation.information.apps}}
    return render(request, 'wapp_management/installed_apps.html', output)


def uninstall_an_app(request):
    app_path = request.POST.get("app_path", None)
    app_type = request.POST.get("app_type", None)
    uninstaller_obj = Uninstaller(get_parent_directory(nav_obj.get_katana_dir()), app_path, app_type)
    # check if inside container
    # get path to wapp
    # uninstaller_obj's field app_path contains path to a particular wapp
    # where as installer_obj's field app_path contains path to the wapps directory.
    path_to_wapp = join_path(uninstaller_obj.app_dir, uninstaller_obj.app_name)
    # delete katana static files from katana static before uninstall
    if core_utils.katana_container_operations(False, katana_static, path_to_wapp):
        print('deleted static files from katana/static')
    if not uninstaller_obj.uninstall():
        # undo delete of files
        print('Error during uninstall, doing a rollback...')
        # check if inside container
        if core_utils.katana_container_operations(True, katana_static, app_path):
            print('Copied static files to katana/static')
    output = {"data": {"app": AppInformation.information.apps}}
    return render(request, 'wapp_management/installed_apps.html', output)


def install_an_app(request):
    app_path = request.POST.get("app_paths")
    dot_data_dir = join_path(nav_obj.get_katana_dir(), "native", "wapp_management", ".data")
    temp_dir_path = join_path(dot_data_dir, "temp")
    output_data = {"status": True, "message": ""}

    if os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    create_dir(temp_dir_path)

    # test userdata
    app_name = apps.WappManagementConfig.name
    ud = UserData(app_name)
    ud.get_dotdata_dir(request)

    status, app_path = wapp_mgmt_utils.handle_wapp_sources(app_path, dot_data_dir, temp_dir_path, output_data)
    if status:
        installer_obj = Installer(get_parent_directory(nav_obj.get_katana_dir()), app_path)
        print('app_directory: ' + installer_obj.app_directory)
        print('app_name: ' + installer_obj.app_name)
        # check if inside container
        # get the path to wapp
        path_to_wapp = join_path(installer_obj.app_directory, installer_obj.app_name)
        # copy wapp static files to katana static
        if core_utils.katana_container_operlations(True, katana_static, path_to_wapp):
            print('Copied static files to katana/static')
        if installer_obj.install():
            print('App installation complete')
        elif installer_obj.message != "":
            output_data["status"] = False
            output_data["message"] += "\n" + installer_obj.message
    return JsonResponse(output_data)


class AppInstallConfig(View):

    def post(self, request):
        app_paths = request.POST.getlist("app_paths[]")
        filename = request.POST.get("filename")

        root = ET.Element("data")
        for app_path in app_paths:
            app = ET.SubElement(root, "app")
            if os.path.exists(app_path):
                ET.SubElement(app, "filepath").text = app_path
            else:
                ET.SubElement(app, "repository").text = app_path
        fpath = join_path(WappManagementView.dot_data_directory, "{0}.xml".format(filename))
        xml_str = ET.tostring(root, method='xml')
        with open(fpath, "w") as f:
            f.write(xml_str.decode('utf-8'))

        files = get_sub_files(WappManagementView.dot_data_directory)
        preferences = []
        for subfile in files:
            filename, file_extension = os.path.splitext(subfile)
            if file_extension == ".xml":
                preferences.append(filename)
        output_data = {"data": {"preferences": preferences}}

        return render(request, 'wapp_management/saved_preferences.html', output_data)


def load_configs(request):
    files = get_sub_files(WappManagementView.dot_data_directory)
    config_files = []
    for subfile in files:
        filename, file_extension = os.path.splitext(subfile)
        if file_extension == ".xml":
            config_files.append(filename)
    output_data = {"data": {"config_files": {"names": config_files}}}
    return render(request, 'wapp_management/popup.html', output_data)


def open_config(request):
    config_name = request.GET['config_name']
    config_path = join_path(WappManagementView.dot_data_directory, "{0}.xml".format(config_name))

    config_file_data_dir = join_path(WappManagementView.dot_data_directory, config_name)

    info = []
    show_install_btn = True
    with open(config_path, 'r') as f:
        data = f.read()
    tree = ET.ElementTree(ET.fromstring(data))
    apps = tree.findall('app')
    for app in apps:
        temp = {}
        if app.find('zip', None) is not None:
            node = app.find('zip', None)
            type_of_app = "zip"
            text = node.text
            if not os.path.exists(join_path(config_file_data_dir, text)):
                show_install_btn = False
                needs_update = True
            else:
                needs_update = False
        elif app.find('repository', None) is not None:
            node = app.find('repository', None)
            type_of_app = "repository"
            text = node.text
            needs_update = False
        else:
            node = app.find('filepath', None)
            type_of_app = "filepath"
            text = node.text
            if not os.path.exists(text):
                show_install_btn = False
                needs_update = True
            else:
                needs_update = False
        temp["name"] = text
        temp["type"] = type_of_app
        temp["needs_update"] = needs_update

        info.append(temp)

    output_data = {"config_name": config_name, "preference_details": info,
                   "show_install_btn": show_install_btn}
    return render(request, 'wapp_management/config_details.html', output_data)


def validate_app_path(request):
    output = {"status": True, "message": ""}
    detail_type = request.POST.get("type", None)
    detail_info = request.POST.get("value", None)
    dot_data_dir = join_path(nav_obj.get_katana_dir(), "native", "wapp_management", ".data")
    temp_dir_path = join_path(dot_data_dir, "temp")
    app_path = False

    if os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    if create_dir(temp_dir_path):
        if detail_type == "repository":
            repo_name = get_repository_name(detail_info)
            os.system("git clone {0} {1}".format(detail_info, join_path(temp_dir_path, repo_name)))
            app_path = join_path(temp_dir_path, repo_name)
        elif detail_type == "zip":
            if os.path.exists(detail_info):
                temp = detail_info.split(os.sep)
                temp = temp[len(temp) - 1]
                shutil.copyfile(detail_info, join_path(temp_dir_path, temp))
                zip_ref = zipfile.ZipFile(join_path(temp_dir_path, temp), 'r')
                zip_ref.extractall(temp_dir_path)
                zip_ref.close()
                app_path = join_path(temp_dir_path, temp[:-4])
            else:
                output["status"] = False
                output["message"] = "{0} does not exist".format(detail_info)
                print("-- An Error Occurred -- ".format(output["message"]))
        elif detail_type == "filepath":
            if os.path.isdir(detail_info):
                filename = get_dir_from_path(detail_info)
                copy_dir(detail_info, join_path(temp_dir_path, filename))
                app_path = join_path(temp_dir_path, filename)
            else:
                output["status"] = False
                output["message"] = "{0} does not exist or is not a directory".format(detail_info)
                print("-- An Error Occurred -- {0}".format(output["message"]))
        else:
            print("-- An Error Occurred -- Type of validation not given.")
        if app_path:
            app_validator_obj = AppValidator(app_path)
            output = app_validator_obj.is_valid()
    else:
        print("-- An Error Occurred -- Could not create temporary directory.")
    return JsonResponse(output)

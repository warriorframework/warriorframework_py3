# -*- coding: utf-8 -*-
import collections
import json
import re
import os
import xmltodict
from django.http import JsonResponse
from django.shortcuts import render
from collections import OrderedDict
from django.template.loader import render_to_string
from django.views import View
from katana.utils.directory_traversal_utils import join_path, get_dir_from_path, get_parent_dir_path
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
from katana.wapps.testwrapper.testwrapper_utils.defaults import impacts, on_errors, runmodes, iteration_types, contexts
from katana.wapps.testwrapper.testwrapper_utils.get_drivers import GetDriversActions
from katana.wapps.testwrapper.testwrapper_utils.verify_testwrapper_file import VerifyTestWrapperFile


navigator = Navigator()
CONFIG_FILE = join_path(navigator.get_katana_dir(), "config.json")
APP_DIR = join_path(navigator.get_katana_dir(), "wapps", "testwrapper")
STATIC_DIR = join_path(APP_DIR, "static", "testwrapper")
TEMPLATE = join_path(STATIC_DIR, "base_templates", "Untitled.xml")
DROPDOWN_DEFAULTS = read_json_data(join_path(STATIC_DIR, "base_templates", "dropdowns_data.json"))


class TestWrapperView(View):

    def get(self, request):
        """
        Get Request Method
        """
        return render(request, 'testwrapper/cases.html')


def get_list_of_testwrappers(request):
    """
    Returns a list of cases
    """
    config = read_json_data(CONFIG_FILE)
    return JsonResponse({"data": navigator.get_dir_tree_json(config["testwrapper"])})


def get_file(request):
    """
    Reads a case file and returns it's contents in JSOn format
    """

    try:
            file_path = request.GET.get('path')
            if file_path == "false":
                file_path = TEMPLATE
            vcf_obj = VerifyTestWrapperFile(TEMPLATE, file_path)
            output, data = vcf_obj.verify_file()
            if output["status"]:
                repo_dirs = navigator.get_user_repos_dir()
                repo_dict = {}

                for repo in repo_dirs:
                    repo_dict[repo] = {}

                    repo_path = repo_dirs[str(repo)]
                    da_obj = GetDriversActions(repo_path)
                    if file_path == TEMPLATE:
                        output["filepath"] = read_json_data(CONFIG_FILE)["testwrapper"]
                    else:
                        output["filepath"] = get_parent_dir_path(file_path)
                    output["filename"] = os.path.splitext(get_dir_from_path(file_path))[0]
                    output["user_repos"] = repo_dirs

                    repo_dict[repo] = da_obj.get_all_actions()
                output["drivers"] = repo_dict
                output["html_data"] = render_to_string('testwrapper/display_case.html', {"data": data,
                                                                                   "defaults": DROPDOWN_DEFAULTS,
                                                                                   "drivers": output["drivers"],
                                                                                         "user_repos":repo_dirs})
                return JsonResponse(output)
            else:
                JsonResponse({"status": output["status"], "message": output["message"]})
    except Exception as e:
        return JsonResponse({"status": 0,"message":"Exception opening the file"})

def validate_details_data(data):
    """
    Validates details of the file before saving
    """

    return data


def validate_step_data(data):
    """
    Validates steps of the file before saving
    """
    for ts in range(0, len(data)):
        if data[ts]["impact"] in impacts():
            data[ts]["impact"] = impacts()[data[ts]["impact"]]
        if data[ts]["context"] in contexts():
            data[ts]["context"] = contexts()[data[ts]["context"]]
        for i in range(0, len(data[ts]["Execute"]["Rule"])):
            if data[ts]["Execute"]["Rule"][i]["@Else"] in on_errors():
                data[ts]["Execute"]["Rule"][i]["@Else"] = on_errors()[data[ts]["Execute"]["Rule"][i]["@Else"]]
        if data[ts]["runmode"]["@type"] in runmodes():
            data[ts]["runmode"]["@type"] = runmodes()[data[ts]["runmode"]["@type"]]
        if data[ts]["Iteration_type"]["@type"] in iteration_types():
            data[ts]["Iteration_type"]["@type"] = iteration_types()[data[ts]["Iteration_type"]["@type"]]
        if data[ts]["onError"]["@action"] in on_errors():
            data[ts]["onError"]["@action"] = on_errors()[data[ts]["onError"]["@action"]]
    return data


def save_file(request):
    """ This function saves the file in the given path. """
    output = {"status": True, "message": ""}
    data = json.loads(request.POST.get("data"), object_pairs_hook=collections.OrderedDict)
    data["TestWrapper"]["Details"] = validate_details_data(data["TestWrapper"]["Details"])
    data["TestWrapper"]["Setup"]["step"] = validate_step_data(data["TestWrapper"]["Setup"]["step"])
    data["TestWrapper"]["Cleanup"]["step"] = validate_step_data(data["TestWrapper"]["Cleanup"]["step"])
    data["TestWrapper"]["Debug"]["step"] = validate_step_data(data["TestWrapper"]["Debug"]["step"])
    xml_data = xmltodict.unparse(data, pretty=True)
    directory = request.POST.get("directory")
    filename = request.POST.get("filename")
    extension = request.POST.get("extension")
    if output['status']:
        try:
            with open(join_path(directory, filename + extension), 'w') as f:
                f.write(xml_data)
        except Exception as e:
            output["status"] = False
            output["message"] = e
            print("-- An Error Occurred -- {0}".format(e))
    return JsonResponse(output)

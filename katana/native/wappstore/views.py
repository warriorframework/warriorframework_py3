# -*- coding: utf-8 -*-
import collections
import json

import os

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
import requests

from native.wapp_management.wapp_management_utils.installer import Installer
from utils.directory_traversal_utils import get_parent_directory
from utils.navigator_util import Navigator
from wui.core.core_utils.app_info_class import AppInformation

nav_obj = Navigator()
app_path = os.path.join(nav_obj.get_katana_dir(), "native", "wappstore", ".data")
address_port = "http://localhost:5000"


class WappStoreView(View):

    template = 'wappstore/wappstore.html'

    def get(self, request):
        """
        Get Request Method
        """
        content = requests.get('{0}/wapps/get_all_wapps_data/'.format(address_port)).content
        response = order_wapp_content(json.loads(content.decode("utf-8")))
        response.update({"installed_apps": get_installed_wapp_names()})
        return render(request, WappStoreView.template, response)


def expand_wapp(request):
    content = requests.get(url='{0}/wapps/expand_wapp/?wapp_name={1}'.format(address_port, request.GET.get("name"))).content
    response = json.loads(content.decode("utf-8"))
    return render(request, 'wappstore/expand_wapp.html', response)


def install_app(request):
    app_name = request.GET.get("app-name")
    output_data = {"status": True, "message": ""}
    print(os.path.join(app_path, app_name))
    if os.path.exists(os.path.join(app_path, app_name) and os.path.isdir(os.path.join(app_path, app_name))):
        installer_obj = Installer(get_parent_directory(nav_obj.get_katana_dir()), os.path.join(app_path, app_name))
        installer_obj.install()
        if installer_obj.message != "":
            output_data["status"] = False
            output_data["message"] += "\n" + installer_obj.message
    else:
        output_data["status"] = False
        output_data["message"] += "App not available for installation"
    return JsonResponse(output_data)


def go_to_account(request):
    return render(request, 'wappstore/account_login.html')


def go_to_home_page(request):
    content = requests.get('{0}/wapps/get_all_wapps_data/'.format(address_port)).content
    response = order_wapp_content(json.loads(content.decode("utf-8")))
    response.update({"installed_apps": get_installed_wapp_names()})
    return render(request, 'wappstore/home_page_content.html', response)


def see_more_wapps(request):
    wapp_type = request.GET.get('wapp_type', 'pop')
    content = requests.get('{0}/wapps/see_more_wapps_data/{1}'.format(address_port, wapp_type)).content
    response = json.loads(content.decode("utf-8"))
    response.update({"installed_apps": get_installed_wapp_names()})
    return render(request, 'wappstore/individual_section.html', response)


def order_wapp_content(input_data):
    order = ["pop", "wa", "ta", "nw", "oss"]
    data = {"data": collections.OrderedDict()}
    for o in order:
        data["data"][o] = input_data["data"][o]
    return data


def get_installed_wapp_names():
    apps = set()
    for app in AppInformation.information.apps:
        apps.add(app.data["app"]["name"])
    return apps

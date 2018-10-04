# -*- coding: utf-8 -*-
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
        response = json.loads(content.decode("utf-8"))
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
    response = json.loads(content.decode("utf-8"))
    return render(request, 'wappstore/home_page_content.html', response)


def see_more_wapps(request):
    wapp_type = request.GET.get('wapp_type', 'pop')
    content = requests.get('{0}/wapps/see_more_wapps_data/{1}'.format(address_port, wapp_type)).content
    response = json.loads(content.decode("utf-8"))
    for wapp in response["data"]["gen"]:
        print(wapp["name"])
    return render(request, 'wappstore/individual_section.html', response)


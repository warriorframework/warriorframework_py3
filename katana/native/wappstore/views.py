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
app_path = os.path.join(nav_obj.get_katana_dir(), "native", "wappstore", ".data", "terminal")
address_port = "http://167.254.211.230:30898"


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
    content = requests.get('{0}/wapps/get_wapp_info/'.format(address_port)).content
    response = json.loads(content.decode("utf-8"))
    return render(request, 'wappstore/expand_wapp.html', response)


def install_terminal_app(request):
    output_data = {"status": True, "message": ""}
    installer_obj = Installer(get_parent_directory(nav_obj.get_katana_dir()), app_path)
    installer_obj.install()
    if installer_obj.message != "":
        output_data["status"] = False
        output_data["message"] += "\n" + installer_obj.message
    return JsonResponse(output_data)
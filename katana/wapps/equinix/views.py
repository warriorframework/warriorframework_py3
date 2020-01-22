
import collections
import json
import os
import re
import xmltodict
import requests
from collections import OrderedDict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from katana.utils.directory_traversal_utils import join_path, get_dir_from_path, get_parent_dir_path
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
from katana.wapps.cases.cases_utils.defaults import impacts, on_errors, runmodes, iteration_types, contexts
from katana.wapps.cases.cases_utils.get_drivers import GetDriversActions
from katana.wapps.cases.cases_utils.verify_case_file import VerifyCaseFile

navigator = Navigator()
equinix_measure_data_json_path = join_path(navigator.get_katana_dir(), "wapps/equinix/equinix_measure_data.json")
equinix_set_data_json_path = join_path(navigator.get_katana_dir(), "wapps/equinix/equinix_set_data.json")
class EquinixView(View):

    def get(self, request):
        """
        Get Request Method
        """
        return render(request, 'equinix/equinix_home.html')

def set_api(request):
    otsi_interface_name = request.GET.get("odi")
    set_freq = request.GET.get("set_freq")
    pr_type = request.GET.get("pr_type")
    equinix_json_data = read_json_data(equinix_set_data_json_path)
    devices = equinix_json_data["devices"].keys()
    for device in devices:
        equinix_json_data["devices"][device]["interface_name"] = otsi_interface_name
        equinix_json_data["devices"][device]["protection_type"] = pr_type
    with open(equinix_set_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    response = requests.post('http://0.0.0.0:5002/set', json=read_json_data(equinix_set_data_json_path))
    return HttpResponse(response)

def measure_api(request):
    otsi_interface_name = request.GET.get("odi")
    pr_type = request.GET.get("pr_type")
    equinix_json_data = read_json_data(equinix_measure_data_json_path)
    devices = equinix_json_data["devices"].keys()
    for device in devices:
        equinix_json_data["devices"][device]["interface_name"] = otsi_interface_name
        equinix_json_data["devices"][device]["protection_type"] = pr_type
    with open(equinix_measure_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    response = requests.post('http://0.0.0.0:5002/measure', json=read_json_data(equinix_measure_data_json_path))
    return HttpResponse(response)
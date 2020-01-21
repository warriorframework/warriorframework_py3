
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
    set_min_freq = request.GET.get("set_min_freq")
    set_max_freq = request.GET.get("set_max_freq")
    path_type = request.GET.get("pr_type")
    equinix_json_data = read_json_data(equinix_set_data_json_path)
    # print(equinix_json_data)
    # import pdb; pdb.set_trace()
    # equinix_json_data[]
    devices = equinix_json_data["set"].keys()
    for device in devices:
        equinix_json_data["set"][device]["interface_name"] = otsi_interface_name
        equinix_json_data["set"][device]["preset_work_max_frequency"] = set_max_freq
        equinix_json_data["set"][device]["preset_protect_max_frequency"] = set_max_freq
        equinix_json_data["set"][device]["min_frequency_preset_work"] = set_min_freq
        equinix_json_data["set"][device]["min_frequency_preset_protect"] = set_min_freq
        equinix_json_data["set"][device]["path_type"] = path_type
    with open(equinix_set_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    # print(read_json_data(equinix_set_data_json_path))
    response = requests.post('http://0.0.0.0:5002/measure', json=read_json_data(equinix_set_data_json_path))
    return HttpResponse(response)

def measure_api(request):
    otsi_interface_name = request.GET.get("odi")
    msr_min_freq = request.GET.get("msr_min_freq")
    msr_max_freq = request.GET.get("msr_max_freq")
    path_type = request.GET.get("pr_type")
    equinix_json_data = read_json_data(equinix_measure_data_json_path)
    # print(equinix_json_data)
    # import pdb; pdb.set_trace()
    # equinix_json_data[]
    devices = equinix_json_data["set"].keys()
    for device in devices:
        equinix_json_data["set"][device]["interface_name"] = otsi_interface_name
        equinix_json_data["set"][device]["preset_work_max_frequency"] = msr_max_freq
        equinix_json_data["set"][device]["preset_protect_max_frequency"] = msr_max_freq
        equinix_json_data["set"][device]["min_frequency_preset_work"] = msr_min_freq
        equinix_json_data["set"][device]["min_frequency_preset_protect"] = msr_min_freq
        equinix_json_data["set"][device]["path_type"] = path_type
    with open(equinix_measure_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    # print(otsi_interface_name, msr_min_freq, msr_max_freq, path_type )
    # print(read_json_data(equinix_measure_data_json_path))
    response = requests.post('http://0.0.0.0:5002/measure', json=read_json_data(equinix_measure_data_json_path))
    return HttpResponse(response)
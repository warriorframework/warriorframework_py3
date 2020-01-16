
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


class EquinixView(View):

    def get(self, request):
        """
        Get Request Method
        """
        return render(request, 'equinix/equinix_home.html')

def set_api(request):
    json_string = request.POST.get('json_data')
    json_data = json.loads(json_string)
    response =  requests.post('http://0.0.0.0:5002/set', json=json_data)
    return HttpResponse(response)

def measure_api(request):
    json_string = request.POST.get('json_data')
    json_data = json.loads(json_string)
    response = requests.post('http://0.0.0.0:5002/measure', json=json_data)
    return HttpResponse(response)
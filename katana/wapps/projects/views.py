# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
import collections
import json
import os
import xmltodict
from django.http import JsonResponse
from django.template.loader import render_to_string
from utils.directory_traversal_utils import join_path, get_parent_dir_path, get_dir_from_path
from utils.json_utils import read_json_data, read_xml_get_json
from utils.navigator_util import Navigator
from wapps.projects.suite_utils.defaults import on_errors, impacts, contexts, runmodes, \
    executiontypes, runtypes
from wapps.projects.suite_utils.verify_suite_file import VerifySuiteFile

navigator = Navigator()
CONFIG_FILE = join_path(navigator.get_katana_dir(), "config.json")
APP_DIR = join_path(navigator.get_katana_dir(), "wapps", "projects")
STATIC_DIR = join_path(APP_DIR, "static", "projects")
TEMPLATE = join_path(STATIC_DIR, "base_templates", "Untitled.xml")
DROPDOWN_DEFAULTS = read_json_data(join_path(STATIC_DIR, "base_templates", "dropdowns_data.json"))


class projectsView(View):
    print("project View")
    def get(self, request):
        """
        Get Request Method
        """
        return render(request, 'projects/projects.html')


def get_list_of_suites(request):
    """
    Returns a list of suites
    """
    config = read_json_data(CONFIG_FILE)
    return JsonResponse({"data": navigator.get_dir_tree_json(config["projdir"])})


def get_file(request):
    print("project")
    """
    Reads a file, validates it, computes the HTML and returns it as a JSON response
    """
    file_path = request.GET.get('path')
    if file_path == "false":
        file_path = TEMPLATE
    vcf_obj = VerifySuiteFile(TEMPLATE, file_path)

    output, data = vcf_obj.verify_file()
    
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@22")
    if output["status"]:
        mid_req = (len(data["Project"]["Requirements"]["Requirement"]) + 1) / 2
        if file_path == TEMPLATE:
            output["filepath"] = read_json_data(CONFIG_FILE)["projdir"]
        else:
            output["filepath"] = get_parent_dir_path(file_path)
        output["filename"] = os.path.splitext(get_dir_from_path(file_path))[0]
        print("*********************")
        print(output)
        output["html_data"] = render_to_string('projects/display_suite.html',
                                               {"data": data, "mid_req": mid_req,
                                                "defaults": DROPDOWN_DEFAULTS})
        print(output)
        return JsonResponse(output)
    else:
        print(output)
        JsonResponse({"status": output["status"], "message": output["message"]})


def save_file(request):
    """ This function saves the file in the given path. """
    print("___________________________________output data")
    output = {"status": True, "message": ""}
    data = json.loads(request.POST.get("data"), object_pairs_hook=collections.OrderedDict)
    print(data["Project"])
    data["Project"]["Details"] = validate_details_data(data["Project"]["Details"])
    data["Project"]["Testsuites"]["Testsuite"] = validate_step_data(data["Project"]["Testsuites"]["Testsuite"])
    xml_data = xmltodict.unparse(data, pretty=True)
    directory = request.POST.get("directory")
    filename = request.POST.get("filename")
    extension = request.POST.get("extension")
    print(directory, filename)
    try:
        with open(join_path(directory, filename + extension), 'w') as f:
            f.write(xml_data)
    except Exception as e:
        output["status"] = False
        output["message"] = e
        print("-- An Error Occurred -- {0}".format(e))
    return JsonResponse(output)


def validate_details_data(data):
    """
    Validates default_onerror and type tags in details section while saving
    """
    if data["default_onError"]["@action"] in on_errors():
        data["default_onError"]["@action"] = on_errors()[data["default_onError"]["@action"]]
    return data


def validate_step_data(data):
    """
    Validates steps of the file before saving
    """
    print(data)
    for ts in range(0, len(data)):
        if data[ts]["impact"] in impacts():
            data[ts]["impact"] = impacts()[data[ts]["impact"]]
        for i in range(0, len(data[ts]["Execute"]["Rule"])):
            if data[ts]["Execute"]["Rule"][i]["@Else"] in on_errors():
                data[ts]["Execute"]["Rule"][i]["@Else"] = on_errors()[data[ts]["Execute"]["Rule"][i]["@Else"]]
        if data[ts]["onError"]["@action"] in on_errors():
            data[ts]["onError"]["@action"] = on_errors()[data[ts]["onError"]["@action"]]
    return data
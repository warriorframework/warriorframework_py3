from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse

import os
import json
import subprocess

from utils.navigator_util import Navigator

MOCK_DATA = {
    "host": {
        "address": "localhost",
        "port": "22",
        "username": "arch",
        "password": "arch",
        "end_prompt": "[arch@arch microservice_store]$"
    },
    "registry": {
        "address": "fnc-docker-reg:3000",
        "image": "opce-algo"
    }
}

WARRIOR_DIR = Navigator().get_warrior_dir()
PLUGINSPACE_DIR = os.path.join(WARRIOR_DIR, "plugins", "microservice_store_plugin", "pluginspace")
PLUGINSPACE_WDF_DIR = os.path.join(PLUGINSPACE_DIR, "data")
PLUGINSPACE_TC_DIR = os.path.join(PLUGINSPACE_DIR, "testcases")
PLUGINSPACE_TS_DIR = os.path.join(PLUGINSPACE_DIR, "suites")
PLUGINSPACE_TD_VC_DIR = os.path.join(PLUGINSPACE_DIR, "config_files")

WARRIOR_EXE = os.path.join(WARRIOR_DIR, 'Warrior')



# Create your views here.
def index(request):
    """
    Renders landing page of the App
    :param request:
    :return:
    """
    context = {

    }
    template = "microservice_store/index.html"
    return render(request, template, context)

def generate_host_system_data(host):
    """
    Takes host data, device on which microservice is deployed,
    and generates Input Data File from a template
    :param host:
    :return:
    """
    df = render_to_string("xml_templates/WDF_microservices_host_system_data_template.xml", {"host": host})
    open(os.path.join(PLUGINSPACE_WDF_DIR, "WDF_microservices_host_system_data.xml"), "w+").write(df)
    return

def generate_registry_operations(data):
    """
    Takes host and registry information, and generates
    variable config file from a template
    :param data:
    :return:
    """
    df = render_to_string("xml_templates/VC_microservices_registry_operations_template.xml", {"data": data})
    open(os.path.join(PLUGINSPACE_TD_VC_DIR, "VC_microservices_registry_operations.xml"), "w+").write(df)
    return

def deploy(request):
    """
    Takes request from the browser, makes call to generate
        1. Input Data File
        2. Variable Config File
    and return StreamHTTP back to client, invoking a stream
    function as an yeild
    :param request:
    :return:
    """
    data = json.loads(request.GET.get("data"))
    host = data["host"]

    if host["deployment_environment"] == "docker":
        f  = "TC_microservices_host_docker_operations.xml"
    elif host["deployment_environment"] == "kubernetes":
        f = "TC_microservices_host_kubernetes_operations.xml"

    generate_host_system_data(data["host"])

    if host["deployment_environment"] == "docker":
        if host["bind_host_interface"].strip() != "":
            host["bind_host_interface_port"] = "-p " + host["bind_host_interface"]
            if host["bind_host_port"].strip() != "":
                host["bind_host_interface_port"] += ":" + host["bind_host_port"]
    elif host["deployment_environment"] == "kubernetes":
        if host["bind_host_port"].strip() != "":
            host["port_flag"] = "--port={}".format(host["bind_host_port"])
        if host["replicas"].strip() != "":
            host["replicas_flag"] = "--replicas={}".format(host["replicas"])

    data["registry"]["just_image"] = data["registry"]["image"].split(":")[0]

    generate_registry_operations(data)

    return StreamingHttpResponse(stream(f))

def stream(file_list):
    """
    Takes TC or TS, and executes warrior, and yields
    response to StreamHTTP
    :param file_list:
    :return:
    """
    f = os.path.join(PLUGINSPACE_TC_DIR, file_list)
    warrior_cmd = '{0} {1} {2}'.format("python3", WARRIOR_EXE, f)
    output = subprocess.Popen(str(warrior_cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)

    print_cmd = '{0} {1} {2}'.format("python3", WARRIOR_EXE, f)

    first_poll = True

    file_li_string = "<li>{0}</li>".format(file_list)

    file_list_html = "<ol>{0}</ol>".format(file_li_string)
    cmd_string = "<h6><strong>Command: </strong></h6>{0}<br>".format(print_cmd)
    logs_heading = "<br><h6><strong>Logs</strong>:</h6>"
    init_string = "<br><h6><strong>Executing:</strong></h6>{0}" \
                       .format(file_list_html) + cmd_string + logs_heading

    while output.poll() is None:
        line = output.stdout.readline()
        if first_poll:
            line = init_string + line
            first_poll = False
            # Yield this line to be used by streaming http response
        yield line + '</br>'
        if line.startswith('-I- DONE'):
            break
    return
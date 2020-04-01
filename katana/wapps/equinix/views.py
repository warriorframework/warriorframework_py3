
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
from katana.wapps.equinix.models import equinixgroups, equinixtransponder, equinixops
from katana.wapps.equinix.forms import equinixgroupsForm, equinixtransponderForum, equinixopsForum
navigator = Navigator()
equinix_measure_data_json_path = join_path(navigator.get_katana_dir(), "wapps/equinix/equinix_measure_data.json")
equinix_set_data_json_path = join_path(navigator.get_katana_dir(), "wapps/equinix/equinix_set_data.json")

class EquinixView(View):

    def get(self, request):
        """
        Get Request Method
        """
        group_list=["None"]
        try:
            group_list=[]
            data = equinixgroups.objects.all()
            if len(data):
                for i in data:
                    group_list.append(i.groupname)
        except:
            print("=================================================================================")
            print("Something went wrong!\n Unable to fetch data from database.")
            print("=================================================================================")
        return render(request, 'equinix/equinix_home.html',{"group_list":group_list})

def set_api(request):
    groupname1 = request.GET.get("set_group1")
    groupname2 = request.GET.get("set_group2")
    # group details fetching from db
    group_details1 = equinixgroups.objects.get(groupname=groupname1)
    group_details2 = equinixgroups.objects.get(groupname=groupname2)
    transpondername1 = group_details1.transpondername
    opsname1 = group_details1.opsname
    interface1 = group_details1.interfacename
    transponder_details1 = equinixtransponder.objects.get(transpondername=transpondername1)
    transponderip1 = transponder_details1.transponderip
    transponderport1 = transponder_details1.transponderport
    transponderusername1 = transponder_details1.transponderusername
    transponderpassword1 = transponder_details1.transponderpassword
    ops_details1 = equinixops.objects.get(opsname=opsname1)
    opsname1 = ops_details1.opsname
    opsusername1 = ops_details1.opsusername
    opspassword1 = ops_details1.opspassword
    opsip1 = ops_details1.opsip
    opsport1 = ops_details1.opsport
    transpondername2 = group_details2.transpondername
    opsname2 = group_details2.opsname
    interface2 = group_details2.interfacename
    transponder_details2 = equinixtransponder.objects.get(transpondername=transpondername2)
    transponderip2 = transponder_details2.transponderip
    transponderport2 = transponder_details2.transponderport
    transponderusername2 = transponder_details2.transponderusername
    transponderpassword2 = transponder_details2.transponderpassword
    ops_details2 = equinixops.objects.get(opsname=opsname2)
    opsname2 = ops_details2.opsname
    opsusername2 = ops_details2.opsusername
    opspassword2 = ops_details2.opspassword
    opsip2 = ops_details2.opsip
    opsport2 = ops_details2.opsport
    equinix_json_data={}
    equinix_json_data["T600"] = {}
    equinix_json_data["OPS"] = {}
    equinix_json_data["T600"][transpondername1]={}
    equinix_json_data["T600"][transpondername2]={}
    equinix_json_data["T600"][transpondername1]["interface_name"] = interface1
    equinix_json_data["T600"][transpondername1]["password"] = transponderpassword1
    equinix_json_data["T600"][transpondername1]["username"] = transponderusername1
    equinix_json_data["T600"][transpondername1]["protocol"] = "ssh"
    equinix_json_data["T600"][transpondername1]["port"] = transponderport1
    equinix_json_data["T600"][transpondername1]["ip"] = transponderip1
    equinix_json_data["T600"][transpondername2]["interface_name"] = interface2
    equinix_json_data["T600"][transpondername2]["password"] = transponderpassword2
    equinix_json_data["T600"][transpondername2]["username"] = transponderusername2
    equinix_json_data["T600"][transpondername2]["protocol"] = "ssh"
    equinix_json_data["T600"][transpondername2]["port"] = transponderport2
    equinix_json_data["T600"][transpondername2]["ip"] = transponderip2
    equinix_json_data["OPS"][opsname1]={}
    equinix_json_data["OPS"][opsname2]={}
    equinix_json_data["OPS"][opsname1]["interface_name"] = interface1
    equinix_json_data["OPS"][opsname1]["password"] = opspassword1
    equinix_json_data["OPS"][opsname1]["username"] = opsusername1
    equinix_json_data["OPS"][opsname1]["protocol"] = "ssh"
    equinix_json_data["OPS"][opsname1]["port"] = opsport1
    equinix_json_data["OPS"][opsname1]["ip"] = opsip1
    equinix_json_data["OPS"][opsname2]["interface_name"] = interface2
    equinix_json_data["OPS"][opsname2]["password"] = opspassword2
    equinix_json_data["OPS"][opsname2]["username"] = opsusername2
    equinix_json_data["OPS"][opsname2]["protocol"] = "ssh"
    equinix_json_data["OPS"][opsname2]["port"] = opsport2
    equinix_json_data["OPS"][opsname2]["ip"] = opsip2
    
    
    with open(equinix_set_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    response = requests.post('http://0.0.0.0:5002/set', json=read_json_data(equinix_set_data_json_path))
    return HttpResponse(response)

def measure_api(request):
    # getdata(request)
    groupname1 = request.GET.get("msr_group1")
    groupname2 = request.GET.get("msr_group2")
    # group details fetching from db
    group_details1 = equinixgroups.objects.get(groupname=groupname1)
    group_details2 = equinixgroups.objects.get(groupname=groupname2)
    transpondername1 = group_details1.transpondername
    interfacename1 = group_details1.interfacename
    opsname1 = group_details1.opsname
    transponder_details1 = equinixtransponder.objects.get(transpondername=transpondername1)
    transponderip1 = transponder_details1.transponderip
    transponderport1 = transponder_details1.transponderport
    transponderusername1 = transponder_details1.transponderusername
    transponderpassword1 = transponder_details1.transponderpassword
    ops_details1 = equinixops.objects.get(opsname=opsname1)
    opsname1 = ops_details1.opsname
    opsusername1 = ops_details1.opsusername
    opspassword1 = ops_details1.opspassword
    opsip1 = ops_details1.opsip
    opsport1 = ops_details1.opsport
    transpondername2 = group_details2.transpondername
    interfacename2 = group_details2.interfacename
    opsname2 = group_details2.opsname
    transponder_details2 = equinixtransponder.objects.get(transpondername=transpondername2)
    transponderip2 = transponder_details2.transponderip
    transponderport2 = transponder_details2.transponderport
    transponderusername2 = transponder_details2.transponderusername
    transponderpassword2 = transponder_details2.transponderpassword
    ops_details2 = equinixops.objects.get(opsname=opsname2)
    opsname2 = ops_details2.opsname
    opsusername2 = ops_details2.opsusername
    opspassword2 = ops_details2.opspassword
    opsip2 = ops_details2.opsip
    opsport2 = ops_details2.opsport
    equinix_json_data={}
    equinix_json_data["T600"] = {}
    equinix_json_data["OPS"] = {}
    equinix_json_data["T600"][transpondername1]={}
    equinix_json_data["T600"][transpondername2]={}
    equinix_json_data["T600"][transpondername1]["interface_name"] = interfacename1
    equinix_json_data["T600"][transpondername1]["password"] = transponderpassword1
    equinix_json_data["T600"][transpondername1]["username"] = transponderusername1
    equinix_json_data["T600"][transpondername1]["protocol"] = "ssh"
    equinix_json_data["T600"][transpondername1]["port"] = transponderport1
    equinix_json_data["T600"][transpondername1]["ip"] = transponderip1
    equinix_json_data["T600"][transpondername2]["interface_name"] = interfacename2
    equinix_json_data["T600"][transpondername2]["password"] = transponderpassword2
    equinix_json_data["T600"][transpondername2]["username"] = transponderusername2
    equinix_json_data["T600"][transpondername2]["protocol"] = "ssh"
    equinix_json_data["T600"][transpondername2]["port"] = transponderport2
    equinix_json_data["T600"][transpondername2]["ip"] = transponderip2
    equinix_json_data["OPS"][opsname1]={}
    equinix_json_data["OPS"][opsname2]={}
    equinix_json_data["OPS"][opsname1]["interface_name"] = interfacename1
    equinix_json_data["OPS"][opsname1]["password"] = opspassword1
    equinix_json_data["OPS"][opsname1]["username"] = opsusername1
    equinix_json_data["OPS"][opsname1]["protocol"] = "ssh"
    equinix_json_data["OPS"][opsname1]["port"] = opsport1
    equinix_json_data["OPS"][opsname1]["ip"] = opsip1
    equinix_json_data["OPS"][opsname2]["interface_name"] = interfacename2
    equinix_json_data["OPS"][opsname2]["password"] = opspassword2
    equinix_json_data["OPS"][opsname2]["username"] = opsusername2
    equinix_json_data["OPS"][opsname2]["protocol"] = "ssh"
    equinix_json_data["OPS"][opsname2]["port"] = opsport2
    equinix_json_data["OPS"][opsname2]["ip"] = opsip2
    
    with open(equinix_measure_data_json_path, "w") as f:
        json.dump(equinix_json_data, f)
    response = requests.post('http://0.0.0.0:5002/measure', json=read_json_data(equinix_measure_data_json_path))
    return HttpResponse(response)

def add_group(request):
    new_group_data = equinixgroupsForm(request.POST)
    
    try:
        groups_list=[]
        data = equinixgroups.objects.all()
        for i in data:
           groups_list.append(i.groupname)
        if request.POST.get("groupname") in groups_list:
            return HttpResponse("duplicate")
        else:
            new_group_data.save()
            response = "success"
    except:
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)
   
def get_group_list(request):
    new_group_data = equinixgroupsForm(request.POST)

    try:
        groups_list=[]
        data = equinixgroups.objects.all()
        for i in data:
            groups_list.append(i.groupname)
    except:
        print("=================================================================================")
        print("Something went wrong!\n Unable to fetch data from database.")
        print("=================================================================================")

    else:
        return HttpResponse(str(groups_list))

def fetch_group_details(request):
    details_json = {}
    groupname = request.POST.get("groupname")
    group_details = equinixgroups.objects.get(groupname=groupname)
    details_json["groupname"] = group_details.groupname
    details_json["transpondername"]=group_details.transpondername
    details_json["opsname"]=group_details.opsname
    details_json["interfacename"]=group_details.interfacename
    return JsonResponse(details_json)

def edit_group(request):
    edit_group_data = equinixgroupsForm(request.POST)
    try:
        groups_list=[]
        data = equinixgroups.objects.all()
        for i in data:
           groups_list.append(i.groupname)
        if request.POST.get("groupname") in list(set(groups_list) - {request.POST.get("selgrpname")}):
            return HttpResponse("duplicate")
        else:
            if (request.POST.get("groupname")).strip() != "" and (request.POST.get("transpondername")).strip() != ""\
                 and (request.POST.get("opsname")).strip() != "":
                    group_detail = equinixgroups.objects.get(groupname = request.POST.get("selgrpname"))  
                    group_detail.delete()
            edit_group_data.save()
            response = "success"
    except Exception as e:
        print(str(e))
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)
   
def add_transponder(request):
    add_new_device = equinixtransponderForum(request.POST)
    try:
        device_list=[]
        data = equinixtransponder.objects.all()
        for i in data:
           device_list.append(i.transpondername)
        if request.POST.get("transpondername") in device_list:
            return HttpResponse("duplicate")
        else:
            add_new_device.save()
            response = "success"
    except:
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)

def add_ops(request):
    add_new_device = equinixopsForum(request.POST)
    try:
        device_list=[]
        data = equinixops.objects.all()
        for i in data:
           device_list.append(i.opsname)
        if request.POST.get("opsname") in device_list:
            return HttpResponse("duplicate")
        else:
            add_new_device.save()
            response = "success"
    except:
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)

def fetch_devices(request):
    if request.POST.get("device_type") == "T600":
        try:
            device_list=[]
            data = equinixtransponder.objects.all()
            for i in data:
                device_list.append(i.transpondername)
        except:
            print("=================================================================================")
            print("Something went wrong!\n Unable to fetch data from database.")
            print("=================================================================================")

        else:
            return HttpResponse(str(device_list))
    elif request.POST.get("device_type") == "OPS":
        try:
            device_list=[]
            data = equinixops.objects.all()
            for i in data:
                device_list.append(i.opsname)
        except:
            print("=================================================================================")
            print("Something went wrong!\n Unable to fetch data from database.")
            print("=================================================================================")

        else:
            return HttpResponse(str(device_list))

def get_device_details(request):
    device_type = request.POST.get("device_type")
    selected_device = request.POST.get("selected_device")
    if device_type == "T600":
        details_json = {}
        device_details = equinixtransponder.objects.get(transpondername=selected_device)
        details_json["transpondername"]=device_details.transpondername
        details_json["transponderip"]=device_details.transponderip
        details_json["transponderport"]=device_details.transponderport
        details_json["transponderusername"]=device_details.transponderusername
        details_json["transponderpassword"]=device_details.transponderpassword
        return JsonResponse(details_json)
    elif device_type == "OPS":
        details_json = {}
        device_details = equinixops.objects.get(opsname=selected_device)
        details_json["opsname"]=device_details.opsname
        details_json["opsip"]=device_details.opsip
        details_json["opsport"]=device_details.opsport
        details_json["opsusername"]=device_details.opsusername
        details_json["opspassword"]=device_details.opspassword
        return JsonResponse(details_json)

def edit_transponder(request):
    edit_device_data = equinixtransponderForum(request.POST)
    try:
        device_list=[]
        data = equinixtransponder.objects.all()
        for i in data:
           device_list.append(i.transponderusername)
        if request.POST.get("transpondername") in list(set(device_list) - {request.POST.get("seldevname")}):
            return HttpResponse("duplicate")
        else:
            if (request.POST.get("transpondername")).strip() != "" and (request.POST.get("transponderip")).strip() != ""\
               and (request.POST.get("transponderusername")).strip() != "" and (request.POST.get("transponderpassword")).strip() != "" :
                    device_detail = equinixtransponder.objects.get(transpondername = request.POST.get("seldevname"))  
                    device_detail.delete()
            edit_device_data.save()
            response = "success"
    except Exception as e:
        print(str(e))
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)


def edit_ops(request):
    edit_device_data = equinixopsForum(request.POST)
    try:
        device_list=[]
        data = equinixops.objects.all()
        for i in data:
           device_list.append(i.opsname)
        if request.POST.get("opsname") in list(set(device_list) - {request.POST.get("seldevname")}):
            return HttpResponse("duplicate")
        else:
            if (request.POST.get("opsname")).strip() != "" and (request.POST.get("opsip")).strip() != ""\
               and (request.POST.get("opsusername")).strip() != "" and (request.POST.get("opspassword")).strip() != "" :
                    device_detail = equinixops.objects.get(opsname = request.POST.get("seldevname"))  
                    device_detail.delete()
            edit_device_data.save()
            response = "success"
    except Exception as e:
        print(str(e))
        response = "fail"
        return HttpResponse(response)
    else:
        return HttpResponse(response)

def get_list_of_transponders(request):
    try:
        transponder_list=[]
        data = equinixtransponder.objects.all()
        for i in data:
            transponder_list.append(i.transpondername)
    except:
        print("=================================================================================")
        print("Something went wrong!\n Unable to fetch data from database.")
        print("=================================================================================")

    else:
        return HttpResponse(str(transponder_list))


def get_list_of_ops(request):
    try:
        ops_list=[]
        data = equinixops.objects.all()
        for i in data:
            ops_list.append(i.opsname)
    except:
        print("=================================================================================")
        print("Something went wrong!\n Unable to fetch data from database.")
        print("=================================================================================")

    else:
        return HttpResponse(str(ops_list))

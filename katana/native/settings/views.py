"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

# -*- coding: utf-8 -*-


import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from katana.native.settings.settings import Settings
from katana.utils.navigator_util import Navigator
import ast

nav_obj = Navigator()
REF_FILE = os.path.join(nav_obj.get_katana_dir(), "katana.native", "assembler", "static", "assembler",
                        "base_templates", "empty.xml")

controls = Settings()

def index(request):
    return render(request, 'settings/index.html', {"data": controls.get_location()})

def email_setting_handler( request ):
    return render(request, 'settings/email_setting_handler.html', {"setting": controls.email_setting_handler(request)})

def secret_handler( request ):
    return render(request, 'settings/secret.html', {"secret": controls.secret_handler(request)})

def jira_setting_handler( request ):
    return render(request, 'settings/jira_setting_handler.html', {"jira": controls.jira_setting_handler(request)})

def general_setting_handler( request ):
    return render(request, 'settings/general_setting_handler.html', {"data": controls.general_setting_handler(request)})

def profile_setting_handler( request ):
    return render(request, 'settings/profile_setting_handler.html', {"data": controls.profile_setting_handler(request)})

def smart_analysis_handler( request ):
    return render(request, 'settings/smart_analysis_handler.html', {"data": controls.smart_analysis_handler(request)})

def prerequisites_handler(request):
    return render(request, 'settings/prerequisites_handler.html', {"data": controls.prerequisites_handler(request)})

def install_prerequisite(request):
    return JsonResponse(controls.prereq_installation_handler(request))

def validate_input_repo(request):
    paths_string=request.POST.get('paths')
    paths_list = ast.literal_eval(paths_string)
    for i in paths_list:
        if os.path.exists(i):
           in_valid=False
        else:
            in_valid=True
            break
    if(in_valid):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def myajaxtestview(request):
    return HttpResponse(request.POST['text'])
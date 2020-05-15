#!/usr/bin/env python
'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import sys
import threading
import multiprocessing
import subprocess
import time
import requests
import json
import shutil
from os.path import abspath, dirname
from termcolor import colored

try:
    import katana

    os.environ["pipmode"] = "True"
# except ModuleNotFoundError as error:
except:
    WARRIORDIR = dirname(dirname(abspath(__file__)))
    sys.path.append(WARRIORDIR)
    try:
        import katana

        os.environ["pipmode"] = "False"
    except:
        raise
from katana.primary_process import __appmanager__, install_custom_app, install_default_apps, \
    remove_app_from_settings_custom, remove_appurl_from_urls_custom, remove_cust_app_source, \
    update_fname, update_logo, update_panel_color, create_log
from katana.utils.navigator_util import Navigator
from katana.utils.json_utils import read_json_data
from katana.utils.directory_traversal_utils import join_path


nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()
wapps_dir_path = BASE_DIR + "/wapps/"
wapps_dir = BASE_DIR + "/wapps"
native_dir = BASE_DIR + "/native"
settings_file = BASE_DIR + "/wui/settings.py"
app_config_file = os.path.join(BASE_DIR, "katana_configs", "app_config.json")
manage_py = os.path.join(BASE_DIR, "manage.py")
urls_file = BASE_DIR + "/wui/urls.py"
wapps_content = os.listdir(wapps_dir)
wapp_ignore = ["__init__.py", "__pycache__", "readme.txt"]
wapps_app = list(set(wapps_content) - set(wapp_ignore))
native_content = os.listdir(native_dir)
native_app = list(set(native_content) - set(wapp_ignore))
Updated_Apps_list = []
json_path = ""
PORT = '6352'
app_config_data = {}
input_json_data = {}
final_input_json_data = {}
invalid_json_path = "false"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "katana.wui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    try:
        import katana

        os.environ["pipmode"] = "True"
    # except ModuleNotFoundError as error:
    except:
        WARRIORDIR = dirname(dirname(abspath(__file__)))
        sys.path.append(WARRIORDIR)
        try:
            import katana

            os.environ["pipmode"] = "False"
        except:
            raise

    def __port_error__():
        """this function prints port error message"""
        print(colored("Error: You don't have permission to access that port.", "red"))
        sys.exit()

    def read_config_file_data():
        """this function reads the data from appconfig.json file"""
        config_file_path = join_path(
            nav_obj.get_katana_dir(), "katana_configs", "app_config.json")
        data = read_json_data(config_file_path)
        return data
    app_config_data = read_config_file_data()

    try:
        PORT = str(sys.argv[3])
    except:
        PORT = '6352'
    else:
        if int(PORT) < 1024:
            __port_error__()

    with open("log.txt", "w") as f:
        f.writelines("")

    if len(sys.argv) > 2 and sys.argv[0].split("/")[-1] == "appmanage.py" and sys.argv[1] == "appconfig":
        if not os.path.exists(sys.argv[2]):
            invalid_json_path = "true"
            print(colored("Invalid json path", "red"))
            create_log("Invalid json path")
            sys.exit()
        else:
            json_path = sys.argv[2]
            try:
                with open(json_path) as f:
                    input_json_data = json.loads(f.read())
            except:
                print(colored("Input json file format is not valid!", "red"))
                create_log("Input json file format is not valid")
                sys.exit()
            else:
                app_config_data = read_config_file_data()
                with open(json_path) as f:
                    input_json_data = json.loads(f.read())
                if "app_title" in input_json_data:
                    final_input_json_data["app_title"] = input_json_data["app_title"]
                else:
                    final_input_json_data["app_title"] = ""
                if "custom_logo_path" in input_json_data:
                    final_input_json_data["custom_logo_path"] = input_json_data["custom_logo_path"]
                else:
                    final_input_json_data["custom_logo_path"] = ""
                if "panel_color" in input_json_data:
                    final_input_json_data["panel_color"] = input_json_data["panel_color"]
                else:
                    final_input_json_data["panel_color"] = ""
                if "katana_default_apps" in input_json_data:
                    final_input_json_data["katana_default_apps"] = input_json_data["katana_default_apps"]
                else:
                    final_input_json_data["katana_default_apps"] = ""
                if "user_custom_apps" in input_json_data:
                    final_input_json_data["user_custom_apps"] = input_json_data["user_custom_apps"]
                else:
                    final_input_json_data["user_custom_apps"] = {}
                if "katana_default_apps_branch" in input_json_data:
                    final_input_json_data["katana_default_apps_branch"] = input_json_data["katana_default_apps_branch"]
                else:
                    final_input_json_data["katana_default_apps_branch"] = ""

                if app_config_data["__READ_ACCESS__"] == "True":
                    app_config_json_path = os.path.join(BASE_DIR, "katana_configs", "app_config.json")
                    final_input_json_data["__READ_ACCESS__"] = "True"
                    final_input_json_data["__userconfigured__"] = "True"
                    final_input_json_data["__normal_run__"] = "True"
                    with open(app_config_json_path, "w") as f:
                        json.dump(final_input_json_data, f)
                        print("======================================================================================")
                        print(colored("configuring katana apps...\nPlease do not quit (or) kill the server manually, wait until the server closes itself...!", "yellow"))
                        print("======================================================================================")
    elif len(sys.argv) == 2 and sys.argv[0].split("/")[-1] == "appmanage.py" and sys.argv[1] == "appconfig":
        invalid_json_path = "true"
        print(colored("E: json path is missing. Usage: python3 appmanage.py appconfig <json path>", "red"))
        create_log("E: json path is missing. Usage: python3 appmanage.py appconfig <json path>")
        sys.exit()
    elif(len(sys.argv) == 1 and sys.argv[0].split("/")[-1] == "appmanage.py"):
        print(colored("Restoring katana configuration...", "yellow"))
    else:
        print("Usage:\n1. To make new configuration: python3 appmanage.py appconfig <json file path>\n2. To restore: python3 appmanage.py")
        sys.exit()


    app_config_data = read_config_file_data()
    if app_config_data["__READ_ACCESS__"] == "True":
        config_apps = app_config_data["user_custom_apps"].keys()
    else:
        config_apps = []
    if app_config_data["katana_default_apps"] == "True" or \
            app_config_data["katana_default_apps"] == "true":
        deafault_wapps = ["cases", "assembler", "cli_data", "execution",
                            "projects", "suites", "testwrapper",
                            "wdf_edit"]
        cust_wapps = list(set(wapps_app) - set(deafault_wapps))
        deleted_Apps_list = list(set(cust_wapps) - set(config_apps))
        deleted_Apps_list = list(
            set(deleted_Apps_list) - set(["__init__.py", "__pycache__"]))
    else:
        deleted_Apps_list = list(set(wapps_app) - set(config_apps))
        deleted_Apps_list = list(
            set(deleted_Apps_list).union(set(native_app)))
        deleted_Apps_list = list(
            set(deleted_Apps_list) - set(["__init__.py", "__pycache__"]))
    if app_config_data["__READ_ACCESS__"] == "True":
        __appmanager__(deleted_Apps_list)

    def function_to_give_read_access():
        """removes the temporary lock and enable the read access of appconfig.json file"""
        clean_data = read_config_file_data()
        clean_data["__READ_ACCESS__"] = "True"
        with open(app_config_file, "w") as f:
            f.write(json.dumps(clean_data, indent=4))
            
    def wait_for(sec):
        i = sec
        while i>0:
            print("{0} {1} {2}".format("Re-checking server status in:", i, "seconds"),  end="  \r")
            time.sleep(1)
            i = i-1
        print("{0}".format(" "*50),  end="  \r")

    def thread_function_to_kill(name):
        """this function is used to kill the server"""
        time.sleep(5)
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(
            ['fuser', '-k', PORT+'/tcp'], stdout=FNULL, stderr=subprocess.STDOUT)

    def thread_function_to_ping(name):
        """this function is used to ping server"""
        print("Installing: " + name)
        create_log("Installing: " + name)
        print("Checking Compatability for:" + name)
        create_log("Checking Compatability for: " + name)
        time.sleep(11)
        try:
            time.sleep(5)
            url = 'http://127.0.0.1:' + PORT + '/'
            resp = requests.get(url)
        except:
            try:
                create_log("Server is taking too long to respond, retrying in a moment...(First retry)")
                print(colored("Server is taking too long to respond    ", "yellow"))
                wait_for(20)
                url = 'http://127.0.0.1:' + PORT + '/'
                resp = requests.get(url)
            except:
                try:
                    time.sleep(3)
                    create_log("Server is taking too long to respond, retrying in a moment...(Second retry)")
                    print(colored("Server is taking too long to respond    ", "yellow"))
                    wait_for(20)
                    time.sleep(3)
                    url = 'http://127.0.0.1:' + PORT + '/'
                    resp = requests.get(url)
                except Exception as e:
                    create_log(str(e))
                    create_log(
                name + " app is not compatible with katana, so it is not going to be installed.")
                    print(colored(
                name + " app is not compatible with katana, so it is not going to be installed.", "red"))
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "True"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    remove_appurl_from_urls_custom(name, "wapps")
                    remove_app_from_settings_custom(name, "wapps")
                    remove_cust_app_source(name, "wapps")
                    clean_data = read_config_file_data()
                    del clean_data["user_custom_apps"][name]
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    thread_function_to_kill("")
                else:
                    create_log(name + " app installed successfully.")
                    print(colored(name + " app installed successfully.", "green"))
                    fnull = open(os.devnull, 'w')
                    retcodee = subprocess.call(
                ['fuser', '-k', PORT+'/tcp'], stdout=fnull, stderr=subprocess.STDOUT)
            else:
                    create_log(name + " app installed successfully.")
                    print(colored(name + " app installed successfully.", "green"))
                    fnull = open(os.devnull, 'w')
                    retcodee = subprocess.call(
                ['fuser', '-k', PORT+'/tcp'], stdout=fnull, stderr=subprocess.STDOUT)
        else:
            create_log(name + " app installed successfully.")
            print(colored(name + " app installed successfully.", "green"))
            fnull = open(os.devnull, 'w')
            retcodee = subprocess.call(
                ['fuser', '-k', PORT+'/tcp'], stdout=fnull, stderr=subprocess.STDOUT)

    if app_config_data["__READ_ACCESS__"] == "True":
        if app_config_data["app_title"].strip() != "":
            frame_name = app_config_data["app_title"]
            update_fname(frame_name)
        if app_config_data["custom_logo_path"].strip() != "":
            logo_path = app_config_data["custom_logo_path"]
            update_logo(logo_path)
        if app_config_data["panel_color"].strip() != "":
            panel_color = app_config_data["panel_color"]
            update_panel_color(panel_color)
        else:
            update_panel_color("#343a40")
        if app_config_data["katana_default_apps"] == "True" or \
                app_config_data["katana_default_apps"] == "true":
            default_apps_list = ["cases", "assembler", "cli_data", "execution",
                                    "projects", "suites", "testwrapper",
                                    "wdf_edit", "microservice_store", "settings",
                                    "wapp_management", "wappstore"]
            all_inst_apps = list(set(wapps_app).union(set(native_app)))
            check_def_apps = list(
                set(default_apps_list) - set(all_inst_apps))
            if len(check_def_apps) > 0:
                install_default_apps(
                    app_config_data['katana_default_apps_branch'])
            else:
                print("\n")
                print("\n")
                create_log("Default apps are installed.")

        elif app_config_data["katana_default_apps"] == "False" or \
            app_config_data["katana_default_apps"] == "false":
            create_log(
                "Default Apps value has set to False in app_config.json, so no Default Apps will be installed in the framework.")
            if not os.path.exists(wapps_dir_path):
                os.mkdir(wapps_dir)
            if not os.path.exists(native_dir):
                os.mkdir(native_dir)
        default_apps_list = ["cases", "assembler", "cli_data", "execution", 
                                "projects", "suites", "testwrapper", "wdf_edit"]
        if app_config_data["katana_default_apps"] == "True" or \
            app_config_data["katana_default_apps"] == "true":
            cust_wapps = list(set(wapps_app) - set(default_apps_list))
            Updated_Apps_list = list(set(config_apps) - set(cust_wapps))
            Updated_Apps_list = list(
                set(Updated_Apps_list) - set(default_apps_list))
        else:
            Updated_Apps_list = list(set(config_apps) - set(wapps_app))
            Updated_Apps_list = list(
                set(Updated_Apps_list) - set(default_apps_list))
    
        if len(Updated_Apps_list) >= 1:
            for app in Updated_Apps_list:
                app_url = app_config_data["user_custom_apps"][app]
                x = multiprocessing.Process(
                    target=thread_function_to_ping, args=(app,))
                try:
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                        install_custom_app(app, app_url)
                except Exception as e:
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    remove_app_from_settings_custom(app, "wapps")
                    remove_cust_app_source(app, "wapps")
                    tempdir = os.path.join(BASE_DIR, app)
                    if os.path.exists(tempdir):
                        shutil.rmtree(tempdir)
                    print(colored(
                        "Error: "+app +
                        " app is not going to be installed!. The possible reasons are:\n1. Poor internet connection\n2. There might be something wrong in the app-name (or) git-url in the input json file\n3. wf_config.json file is missing in the "+app+" app.","red"))
                    create_log(
                        "Error: "+app+" is not going to be installed!. There might be something wrong in the app-name (or) git-url in the input json file (or) may be the app your trying to install is incompatible with warrior framework.")
                    del clean_data["user_custom_apps"][app]
                    clean_data["__READ_ACCESS__"] = "True"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                else:
                    x.start()
                    FNULL = open(os.devnull, 'w')
                    retcode = subprocess.call(
                ['fuser', '-k', PORT+'/tcp'], stdout=FNULL, stderr=subprocess.STDOUT)
                    retcode = subprocess.call(
                        ['python3', manage_py, 'runserver', PORT], stdout=FNULL,
                        stderr=subprocess.STDOUT)
                    x.join()
            function_to_give_read_access()
            print("[100%]\nDone!")
        else:
            # print("Finishing the setup...")
            default_apps_list = ["cases", "assembler", "cli_data", "execution", "projects",
                                 "suites", "testwrapper",
                                 "wdf_edit"]
            conf_apps = app_config_data["user_custom_apps"].keys()
            if app_config_data["katana_default_apps"] == "True" or \
                    app_config_data["katana_default_apps"] == "true":
                cust_wapps = list(set(wapps_app) - set(default_apps_list))
                failed_app = list(set(conf_apps) - set(cust_wapps))
                failed_app = list(set(failed_app) - set(default_apps_list))
            else:
                failed_app = list(set(conf_apps) - set(wapps_app))
                failed_app = list(set(failed_app) - set(default_apps_list))
            Apps_content = list(set(os.listdir(wapps_dir)).union(
                set(os.listdir(native_dir))))
            installed_apps = list(set(Apps_content) - set(wapp_ignore))
            if len(failed_app) > 0:
                clean_data = read_config_file_data()
                if failed_app[0] in clean_data["user_custom_apps"].keys():
                    del clean_data["user_custom_apps"][failed_app[0]]
                with open(app_config_file, "w") as f:
                    f.write(json.dumps(clean_data, indent=4))
            function_to_give_read_access()

            # y = threading.Thread(
            #     target=thread_function_to_kill, args=("app",), daemon=True)
            # y.start()
            # FNULL = open(os.devnull, 'w')
            # retcode = subprocess.call(
            #     ['python3', manage_py, 'runserver', PORT], stdout=FNULL,
            #     stderr=subprocess.STDOUT)
            print("[100%]\nDone!")
#!/usr/bin/env python
import os
import sys
import logging
import threading
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
    remove_app_from_settings_custom, remove_appurl_from_urls_custom, remove_cust_app_source, configure_settings_file, \
    configure_settings_file_custom_app, configure_urls_file, configure_urls_file_custom, update_fname, update_logo, \
    update_panel_color, create_log
from katana.utils.navigator_util import Navigator
from katana.utils.json_utils import read_json_data
from katana.utils.directory_traversal_utils import join_path

nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()
wapps_dir_path = BASE_DIR + "/wapps/"
wapps_dir = BASE_DIR + "/wapps"
native_dir = BASE_DIR + "/native"
settings_file = BASE_DIR + "/wui/settings.py"
app_config_file = BASE_DIR + "/app_config.json"
urls_file = BASE_DIR + "/wui/urls.py"
PORT = 0
wapps_content = os.listdir(wapps_dir)
wapp_ignore = ["__init__.py", "__pycache__", "readme.txt"]
wapps_app = list(set(wapps_content) - set(wapp_ignore))
native_content = os.listdir(native_dir)
native_app = list(set(native_content) - set(wapp_ignore))
Updated_Apps_list = []
json_path = ""
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
        return print('\033[31m', "Error: You don't have permission to access that port.")


    def read_config_file_data():
        nav_obj = Navigator()
        config_file_path = join_path(nav_obj.get_katana_dir(), "app_config.json")
        data = read_json_data(config_file_path)
        return data


    app_config_data = read_config_file_data()

    if len(sys.argv) >= 2 and sys.argv[0].split("/")[-1] == "appmanage.py" and sys.argv[1] == "appconfig":
        program_name = sys.argv[0].split("/")[-1]
        command = sys.argv[1]
        if command == "appconfig" and len(sys.argv) > 2:
            if not os.path.exists(sys.argv[2]):
                invalid_json_path = "true"
                print("Invalid json path")
                create_log("Invalid json path")
            else:
                json_path = sys.argv[2]
        elif command == "appconfig" and len(sys.argv) == 2:
            invalid_json_path = "true"
            print("E: json path is missing. Usage: python3 appmanage.py appconfig <json path>")
            create_log("E: json path is missing. Usage: python3 appmanage.py appconfig <json path>")
        input_json_data = {}
        final_input_json_data = {}
        if command == "appconfig" and program_name == "appmanage.py" and invalid_json_path == "false":
            if not os.path.exists(json_path):
                print(colored("Invalid json path", "red"))
                create_log("Invalid json path")
            else:
                try:
                    with open(json_path) as f:
                        input_json_data = json.loads(f.read())
                except:
                    print(colored("Input json file format is not valid!", "red"))
                    create_log("Input json file format is not valid")
                else:
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
                        app_config_json_path = os.path.join(BASE_DIR, "app_config.json")
                        final_input_json_data["__READ_ACCESS__"] = "True"
                        final_input_json_data["__userconfigured__"] = "True"
                        final_input_json_data["__normal_run__"] = "True"
                        with open(app_config_json_path, "w") as f:
                            json.dump(final_input_json_data, f)
                            print("======================================================================================")
                            print(colored("configuring katana apps...\n Please do not quit (or) kill the server manually, wait until the server closes itself...!", "yellow"))
                            print("======================================================================================")

        app_config_data = read_config_file_data()
        if app_config_data["__READ_ACCESS__"] == "True":
            config_apps = app_config_data["user_custom_apps"].keys()
        else:
            config_apps = []
        if (app_config_data["katana_default_apps"] == "True" or app_config_data["katana_default_apps"] == "true"):
            deafault_wapps = ["cases", "assembler", "cli_data", "execution", "projects", "suites", "testwrapper",
                              "wdf_edit"]
            cust_wapps = list(set(wapps_app) - set(deafault_wapps))
            deleted_Apps_list = list(set(cust_wapps) - set(config_apps))
            deleted_Apps_list = list(set(deleted_Apps_list) - set(["__init__.py", "__pycache__"]))
        else:
            deleted_Apps_list = list(set(wapps_app) - set(config_apps))
            deleted_Apps_list = list(set(deleted_Apps_list).union(set(native_app)))
            deleted_Apps_list = list(set(deleted_Apps_list) - set(["__init__.py", "__pycache__"]))
        if app_config_data["__READ_ACCESS__"] == "True":
            __appmanager__(deleted_Apps_list)


        def function_to_give_read_access():
            clean_data = read_config_file_data()
            clean_data["__READ_ACCESS__"] = "True"
            with open(app_config_file, "w") as f:
                f.write(json.dumps(clean_data, indent=4))


        def thread_function_to_kill(name):
            time.sleep(40)
            os.system("fuser -k 9999/tcp")


        def thread_function_to_ping(name):
            create_log("Checking Compatability for:" + name)
            create_log("Waiting for server to restart...")
            time.sleep(11)
            create_log("Checking katana compatibility for :" + name)
            if PORT == 0:
                try:
                    resp = requests.get('http://127.0.0.1:9999/')
                except Exception as e:
                    print(str(e))
                    create_log(name + " app is not compatible with katana, so it is not going to be installed.")
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    remove_appurl_from_urls_custom(name, "wapps")
                    remove_app_from_settings_custom(name, "wapps")
                    remove_cust_app_source(name, "wapps")
                    Apps_content = list(set(os.listdir(wapps_dir)).union(set(os.listdir(native_dir))))
                    installed_apps = list(set(Apps_content) - set(wapp_ignore))
                    all_apps = ""
                    for app in installed_apps:
                        all_apps += " " + app + " "
                    create_log("INSTALLED APPS: " + all_apps)
                    time.sleep(2)
                else:
                    create_log(name + " app installed successfully.")
                    Apps_content = list(set(os.listdir(wapps_dir)).union(set(os.listdir(native_dir))))
                    installed_apps = list(set(Apps_content) - set(wapp_ignore))
                    all_apps = ""
                    for app in installed_apps:
                        all_apps += " " + app + " "
                    create_log("INSTALLED APPS: " + all_apps)
            else:
                url = 'http://127.0.0.1:' + PORT + '/'
                try:
                    resp = requests.get(url)
                except:
                    create_log(name + " app is not compatible with katana, so it is not going to be installed.")
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    remove_appurl_from_urls_custom(name, "wapps")
                    remove_app_from_settings_custom(name, "wapps")
                    remove_cust_app_source(name, "wapps")
                    Apps_content = list(set(os.listdir(wapps_dir)).union(set(os.listdir(native_dir))))
                    installed_apps = list(set(Apps_content) - set(wapp_ignore))
                    all_apps = ""
                    for app in installed_apps:
                        all_apps += " " + app + " "
                    create_log("INSTALLED APPS: " + all_apps)
                else:
                    create_log(name + " app installed successfully.")
                    Apps_content = list(set(os.listdir(wapps_dir)).union(set(os.listdir(native_dir))))
                    installed_apps = list(set(Apps_content) - set(wapp_ignore))
                    all_apps = ""
                    for app in installed_apps:
                        all_apps += " " + app + " "
                    create_log("INSTALLED APPS: " + all_apps)


        if app_config_data["__READ_ACCESS__"] == "True":
            if (app_config_data["app_title"].strip() != ""):
                frame_name = app_config_data["app_title"]
                update_fname(frame_name)
            if (app_config_data["custom_logo_path"].strip() != ""):
                logo_path = app_config_data["custom_logo_path"]
                update_logo(logo_path)
            if (app_config_data["panel_color"].strip() != ""):
                panel_color = app_config_data["panel_color"]
                update_panel_color(panel_color)
            else:
                update_panel_color("#343a40")
            if (app_config_data["katana_default_apps"] == "True" or app_config_data["katana_default_apps"] == "true"):
                default_apps_list = ["cases", "assembler", "cli_data", "execution", "projects", "suites", "testwrapper",
                                     "wdf_edit", "microservice_store", "settings", "wapp_management", "wappstore"]
                all_inst_apps = list(set(wapps_app).union(set(native_app)))
                check_def_apps = list(set(default_apps_list) - set(all_inst_apps))
                if (len(check_def_apps)):
                    install_default_apps(app_config_data['katana_default_apps_branch'])
                else:
                    print("\n")
                    print("\n")
                    create_log("Default apps are installed.")

            elif (app_config_data["katana_default_apps"] == "False" or app_config_data["katana_default_apps"] == "false"):
                create_log("Default Apps value has set to False in app_config.json, so no Default Apps will be installed in the framework.")
                if not (os.path.exists(wapps_dir_path)):
                    os.mkdir(wapps_dir)
                if not (os.path.exists(native_dir)):
                    os.mkdir(native_dir)
            default_apps_list = ["cases", "assembler", "cli_data", "execution", "projects", "suites", "testwrapper",
                                 "wdf_edit"]
            if (app_config_data["katana_default_apps"] == "True" or app_config_data["katana_default_apps"] == "true"):
                cust_wapps = list(set(wapps_app) - set(default_apps_list))
                Updated_Apps_list = list(set(config_apps) - set(cust_wapps))
                Updated_Apps_list = list(set(Updated_Apps_list) - set(default_apps_list))
            else:
                Updated_Apps_list = list(set(config_apps) - set(wapps_app))
                Updated_Apps_list = list(set(Updated_Apps_list) - set(default_apps_list))
        if (len(Updated_Apps_list) == 1):
            for app in Updated_Apps_list:
                app_url = app_config_data["user_custom_apps"][app]
                x = threading.Thread(target=thread_function_to_ping, args=(app,), daemon=True)
                try:
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    install_custom_app(app, app_url)
                except:
                    clean_data = read_config_file_data()
                    clean_data["__READ_ACCESS__"] = "False"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                    remove_app_from_settings_custom(app, "wapps")
                    remove_cust_app_source(app, "wapps")
                    tempdir = os.path.join(BASE_DIR, app)
                    if (os.path.exists(tempdir)):
                        shutil.rmtree(tempdir)
                    print(colored(
                        "Error: There might be something wrong in the app-name (or) git-url in the input json file (or) may be the app your trying to install is incompatible with warrior framework.",
                        "red"))
                    create_log(
                        "Error: There might be something wrong in the app-name (or) git-url in the input json file (or) may be the app your trying to install is incompatible with warrior framework.")
                    clean_data["__READ_ACCESS__"] = "True"
                    with open(app_config_file, "w") as f:
                        f.write(json.dumps(clean_data, indent=4))
                else:
                    time.sleep(5)
                    x.start()
                    execute_from_command_line(["manage.py", "runserver", "9999"])
                    x.join()
        elif (len(Updated_Apps_list) > 1):
            print(colored("\n------------------------------------------------------\n", "red"))
            print(colored("Error: Multiple apps can't be installed at the same time, please install one app at a time!",
                          "red"))
            print(colored("\n------------------------------------------------------\n", "red"))
            create_log("Error: Multiple apps can't be installed at the same time, please install one app at a time.")
        else:
            default_apps_list = ["cases", "assembler", "cli_data", "execution", "projects", "suites", "testwrapper",
                                 "wdf_edit"]
            conf_apps = app_config_data["user_custom_apps"].keys()
            if (app_config_data["katana_default_apps"] == "True" or app_config_data["katana_default_apps"] == "true"):
                cust_wapps = list(set(wapps_app) - set(default_apps_list))
                failed_app = list(set(conf_apps) - set(cust_wapps))
                failed_app = list(set(failed_app) - set(default_apps_list))
            else:
                failed_app = list(set(conf_apps) - set(wapps_app))
                failed_app = list(set(failed_app) - set(default_apps_list))
            Apps_content = list(set(os.listdir(wapps_dir)).union(set(os.listdir(native_dir))))
            installed_apps = list(set(Apps_content) - set(wapp_ignore))
            if len(failed_app):
                clean_data = read_config_file_data()
                if failed_app[0] in clean_data["user_custom_apps"].keys():
                    del clean_data["user_custom_apps"][failed_app[0]]
                with open(app_config_file, "w") as f:
                    f.write(json.dumps(clean_data, indent=4))
            function_to_give_read_access()

            y = threading.Thread(target=thread_function_to_kill, args=("app",), daemon=True)
            y.start()
            execute_from_command_line(["manage.py", "runserver", "9999"])
    else:
        print("Usage: python3 appmanage.py appconfig <json file path>")
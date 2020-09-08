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
import site
import shutil
import sys
import time
import subprocess
import requests
import json
import pkg_resources
from os.path import abspath, dirname
from termcolor import colored
from collections import OrderedDict

if sys.version_info < (3, 4):
    print("Warrior doesn't support Python version lower than 3.4, now exiting")
    sys.exit(0)
try:
    from warrior.WarriorCore import warrior_cli_driver
    virtual_env = os.getenv('VIRTUAL_ENV')
    if virtual_env:
        war_tools_dir = virtual_env + os.sep + "warrior_settings/Tools"
        backup_dir = virtual_env + os.sep + ".backup/warrior_settings/Tools"
    else:
        if os.path.exists(site.getuserbase() + os.sep + "warrior_settings/Tools"):
            war_tools_dir = site.getuserbase() + os.sep + "warrior_settings/Tools"
            backup_dir = site.getuserbase() + os.sep + ".backup/warrior_settings/Tools"
        elif os.path.exists("/usr/local/warrior_settings/Tools"):
            war_tools_dir = "/usr/local/warrior_settings/Tools"
            backup_dir = "/usr/local/.backup/warrior_settings/Tools"
        else:
            Print("-- An error occured: Can not find the warrior_settings directory.")
            sys.exit()
except:
    print(colored("Could not find an existing warriorframework PIP package."))
    sys.exit()

data = requests.get('https://pypi.python.org/pypi/warriorframework/json')
data = data.json()
ord_dict = OrderedDict()
ord_dict = data['releases'].keys()
versn_list = list(ord_dict)

try:
    if (sys.argv[1] in ['-v', '-V'] and sys.argv[2] is not None):
        if sys.argv[2] == pkg_resources.get_distribution("warriorframework").version:
            print(colored("Current version of warriorframework is same as the given version.", "green"))
            sys.exit()
except Exception as e:
    if pkg_resources.get_distribution("warriorframework").version == versn_list[-1]:
        print(colored("You have already installed the latest version of warriorframework.", "green"))
        sys.exit()

print(colored("Upgrading warrior framework, please hold on a moment !", "green"))
time.sleep(1)
print(colored("Preparing to backup warrior tools...", "green"))
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
if os.path.exists(war_tools_dir):
    shutil.copytree(war_tools_dir, backup_dir)
    time.sleep(1)
    print(colored("Backup successful" + u'\u2713', "green"))
    #upgrade command here
    try:
        if len(sys.argv) == 1:
            _pkg = 'warriorframework==' + versn_list[-1]
            output_log = subprocess.call(['pip', 'install', _pkg])
        elif len(sys.argv) == 3:
            if sys.argv[1] in ['-v', '-V']:
                data = requests.get('https://pypi.python.org/pypi/warriorframework/json')
                json_data = data.json()
                versions_list = json_data["releases"].keys()
                if sys.argv[2].strip() in versions_list:
                    output_log = subprocess.call(['pip', 'uninstall', 'warriorframework', '-y'])
                    _pkg = 'warriorframework==' + sys.argv[2].strip()
                    output_log = subprocess.call(['pip', 'install', _pkg])
                else:
                    print(colored("Error: Could't find the specified version of warriorframework, please check the version you have provided and try again.", "red"))
                    sys.exit()
        else:
            print(colored("Version number is missing.", "red"))
            sys.exit()
    except Exception as e:
        print(colored("Unable to upgrade warriorframework, because of the below error:\n", "red"))
        print(e)
        sys.exit()
    else:
        if os.path.exists(backup_dir):
            if os.path.exists(war_tools_dir):
                shutil.rmtree(war_tools_dir)
            shutil.copytree(backup_dir, war_tools_dir)
            time.sleep(1)
            print(colored("Data files restored successfully" + u'\u2713', "green"))
            time.sleep(1)
            print(colored("Warrior framework upgrade completed.", "green"))
        else:
            print(colored("Backup not found!", "red"))
            sys.exit()
else:
    print(colored("Unable to backup the data ({0} directory not found!)", "red").format(war_tools_dir))
    sys.exit()

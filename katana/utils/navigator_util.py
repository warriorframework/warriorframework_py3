import copy
import os
import re
import json
from .directory_traversal_utils import get_parent_directory, join_path
from katana.utils.json_utils import read_json_data
import subprocess


class Navigator(object):

    def __init__(self):
        self.git_url = "https://github.com/warriorframework/warriorframework_py3.git"

    def get_katana_dir(self):
        """will get katanas main directory"""
        katana_dir = get_parent_directory(os.path.abspath(__file__), 3) + os.sep + 'katana' + os.sep
        return katana_dir

    def get_warrior_dir(self):
        """will get warriors main directory"""
        warrior_dir = get_parent_directory(os.path.abspath(__file__), 3) + os.sep + 'warrior' + os.sep
        return warrior_dir

    def get_user_repos_dir(self):
        """will get warriors main directory"""
        user_repos_dir = {}
        CONFIG_FILE = join_path(self.get_katana_dir(), "config.json")
        warrior_dir = self.get_warrior_dir()[:-1]
        user_repos_dir["warrior"] = warrior_dir

        with open(CONFIG_FILE) as fd:
                    json_data = json.load(fd)
                    for key in json_data:
                        pattern = r'userreposdir*[0-9a-zA-Z]*'
                        result = re.match(pattern, str(key))
                        if result and os.path.exists(json_data[key]):
                            key_values = json_data[key].split('/')[-1]
                            check_dir = next(os.walk(json_data[key]))[1]
                            if "ProductDrivers" and "Actions" in check_dir:
                                user_repos_dir[key_values] = json_data[key]
        return user_repos_dir

    def get_engineer_name(self):
        """
        This function returns the full name (if given in the user_profile.json) of the user.
        :return:
        """
        user_profile = join_path(self.get_katana_dir(), "user_profile.json")
        profile_data = read_json_data(user_profile)
        name = ""
        if profile_data is not None:
            name = (profile_data["firstName"] + " " + profile_data["lastName"]).strip()
        return name
      
    def get_warhorn_dir(self):
        """will get warriors main directory"""
        warrior_dir = get_parent_directory(os.path.abspath(__file__), 3) + os.sep + 'warhorn' + os.sep
        return warrior_dir

    def get_wf_version(self):
        """Gets the current warriorframework version"""
        wf_dir = get_parent_directory(os.path.abspath(__file__), 3)
        version_file = join_path(wf_dir, "version.txt")
        with open(version_file, 'r') as f:
            data = f.readlines()
        version_line = False
        for line in data:
            if line.strip().startswith("Version"):
                version_line = line.strip()
                break
        if version_line:
            return version_line.split(":")[1].strip()
        return version_line

    def get_all_wf_versions(self):
        """Returns a list of all available warrior versions"""
        tags_list = False
        output = self._get_versions()
        if output:
            temp_list = output.decode().strip().split("\n")
            tags_list = set()
            for el in temp_list:
                temp = el.split()[1].strip().split('/')[2]
                if temp.startswith("warrior"):
                    if "^" in temp:
                        temp = temp.split('^')[0]
                    tags_list.add(temp)
        tags_list.add(self.get_wf_version())
        return tags_list

    def _get_versions(self):
        """ Get warrior versions by running git commands. """
        current_directory = os.getcwd()
        os.chdir(get_parent_directory(self.get_katana_dir()))
        p1 = subprocess.Popen(["git", "show-ref", "--tags", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.chdir(current_directory)
        output, errors = p1.communicate()
        if p1.returncode != 0:
            print("-- An Error Occurred -- WarriorFramework versions could not be retrieved from "
                  "local repository")
            print("-- Output -- {0}".format(output.decode()))
            print("-- Errors -- {0}".format(errors.decode()))
            p2 = subprocess.Popen(["git", "ls-remote", "--tags", self.git_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = p2.communicate()
            if p2.returncode != 0:
                print("-- An Error Occurred -- WarriorFramework versions could not be retrieved "
                      "from remote repository")
                print("-- Output -- {0}".format(output.decode()))
                print("-- Errors -- {0}".format(errors.decode()))
                return False
        return output

    def search_folder_name(self, folder_name, given_dir):
        """searches for folder by name in all subdir until found or bottom level directory"""
        pass

    def get_parent_dir(self, given_dir, itter):
        """returns back the parent of given_dir and allows a user to run multipule times"""
        pass

    def get_dir_tree_json(self, start_dir_path, dir_icon=None, file_icon='jstree-file', fl=False,
                          file_a_attr=None, dir_a_attr=None, lazy_loading=False):
        """
        Takes an absolute path to a directory(start_dir_path)  as input and creates a
        json tree having the start_dir as the root.

        This json tree can be consumed as it is by the jstree library hence the default icons
        are mapped to jstree icons.

        By default the first node in the tree will be opened


        Eg of how the json tree will look like
        {
          "text" : "Root node",
          "li_attr": {'data-path': '/path/to/node'},
          "children" : [
                            { "text" : "Child file 1",
                             "icon": "jstree-file",
                             "li_attr": {'data-path': '/path/to/node'}
                             },

                            { "text" : "Child node 2",
                             "li_attr": {'data-path': '/path/to/node'}
                             },

                            { "text" : "Child node 3",
                             "li_attr": {'data-path': '/path/to/node'},
                             "children": [
                                { "text" : "file1", "icon": "jstree-file", "li_attr": {'data-path': '/path/to/node'}},
                                { "text" : "file2", "icon": "jstree-file", "li_attr": {'data-path': '/path/to/node'}},
                                { "text" : "file3", "icon": "jstree-file", "li_attr": {'data-path': '/path/to/node'}}
                                ]
                             },

                        ]
        }

        if lazy_loading is set to True, then only the first level children are read and updated
        in the children list

        """
        base_name = os.path.basename(start_dir_path)
        layout = {'text': base_name, 'data': {'path': start_dir_path},
                  'li_attr': {'data-path': start_dir_path}}

        if not fl:
            layout["state"] = {"opened": 'true'}
            fl = 'false'
        if os.path.isdir(start_dir_path):
            for x in os.listdir(start_dir_path):
                try:
                    if not lazy_loading:
                        layout['a_attr'] = dir_a_attr if dir_a_attr else {}
                        children = self.get_dir_tree_json(os.path.join(start_dir_path, x), fl=fl, file_a_attr=file_a_attr, lazy_loading=lazy_loading)
                    else:
                        children = {'text': x, 'data': {'path': os.path.join(start_dir_path, x)},
                                    'li_attr': {'data-path': os.path.join(start_dir_path, x)}}
                        if os.path.isdir(os.path.join(start_dir_path, x)):
                            layout['a_attr'] = dir_a_attr if dir_a_attr else {}
                            children.update({'icon': dir_icon, 'children': True,
                                             'a_attr': dir_a_attr if dir_a_attr else {}})
                        else:
                            children.update({'icon': file_icon,
                                             'a_attr': file_a_attr if file_a_attr else {}})
                except IOError:
                    pass
                except Exception as e:
                    print("-- An Error Occurred -- {0}".format(e))
                else:
                    if "children" in layout:
                        layout['children'].append(children)
                    else:
                        layout['children'] = [children]
        else:
            layout['icon'] = file_icon
            layout['a_attr'] = file_a_attr if file_a_attr else {}

        return layout

import os
import re
from collections import OrderedDict
from katana.utils.directory_traversal_utils import get_abs_path, join_path, get_dir_from_path
from katana.utils.file_utils import copy_dir, rm_dir, get_katana_static, get_wapp_static

from katana.utils.file_utils import list_dir, copy_dir1, rm_dir1
from katana.utils.navigator_util import Navigator

WARRIORFRAMEWORK = 'warriorframework_py3'
KATANA = 'katana'
WAPPS = 'wapps'

nav = Navigator()


def get_app_path_from_name(app_name, config_file, base_directory):
    """
    This function gets the path to the wf_config_file in the app directory

    Args:
        app_name: Name of the app (eg: default.configuration)
        config_file: Name of the config file
        base_directory: Absolute path to the base directory (/warriorframework/katana/)

    Returns:
        app_config_file_path

    """
    temp = app_name.split(".")
    app_config_file_rel_path = ""
    for el in temp:
        app_config_file_rel_path += el
        app_config_file_rel_path += os.sep

    app_config_file_rel_path += config_file

    app_config_file_path = get_abs_path(
        app_config_file_rel_path, base_directory)

    return app_config_file_path


def _get_package_name(directory_path, trailing_period=True):
    """
    This function changes directory path to a package format

    apps = apps.
    katana/default = katana.default.

    Args:
        directory_path: directory path that needs to be changed to a package format
        trailing_period: if set to False, the last period at the end of the package would be
                         remove.

    Returns:
        package_name: directory path in a package format

    """
    dir_list = directory_path.split(os.sep)
    package_name = ""
    for el in dir_list:
        package_name += el + "."
    if not trailing_period:
        package_name = package_name[:-1]
    return package_name


def validate_config_json(json_data, warrior_dir):
    """
    This function validates the config.json file and returns an ordered dictionary

    :param json_data: original unordered contents of config.json
    :param warrior_dir: path to warrior directory
    :return: Ordered Dictionary containing validated config.json data
    """
    ordered_json = OrderedDict()
    if "engineer" not in json_data:
        ordered_json["engineer"] = ""
    else:
        ordered_json["engineer"] = json_data["engineer"]

    ordered_json["pythonsrcdir"] = warrior_dir[:-1] \
        if "pythonsrcdir" not in json_data or json_data["pythonsrcdir"] == "" \
        else json_data["pythonsrcdir"]

    warrior_dir = ordered_json["pythonsrcdir"]
    ref = OrderedDict([("xmldir", "Testcases"),
                       ('testsuitedir', 'Suites'),
                       ('projdir', 'Projects'),
                       ('idfdir', 'Data'),
                       ('testdata', 'Config_files')])

    for key, value in list(ref.items()):
        if key not in json_data or json_data[key] == "":
            path = get_abs_path(join_path("Warriorspace", value), warrior_dir)
            if path is not None:
                ordered_json[key] = path
            else:
                ordered_json[key] = ""
                print(
                    "-- An Error Occurred -- Path to {0} directory could not be located".format(value))
        else:
            ordered_json[key] = json_data[key]

    if "pythonpath" not in json_data:
        ordered_json["pythonpath"] = ""
    else:
        ordered_json["pythonpath"] = json_data["pythonpath"]

    return ordered_json


def iscontainer():
    """
    iscontainer: When inside a container, control groups will match the pattern /docker/<containerid>
    :return: True if control group points to docker or False if not inside a container
    """
    with open("/proc/1/cgroup") as cgroups:
        for line in cgroups:
            line = re.findall(r'docker', line)
            # return false if outside docker
            if line.__len__() is 0:
                return False
            # else return true
            else:
                print('Warrior instance not deployed in container')
                return True


def katana_container_operations(_copy, katana_static, app_path):
    if iscontainer():
        return handle_wapp_static_container(
            app_path, katana_static, _copy)
    return False


def copy_katana_static(src, dst):
    return True if copy_dir1(src, dst) else False


def delete_katana_static(src, wapp_dir):
    output = True
    try:
        # get wapp static files
        wapp_static = get_wapp_static(wapp_dir)
        # get katana static files
        katana_static = get_katana_static(src, wapp_static)
        for file in katana_static:
            if not rm_dir1(file):
                # if unsuccessful, return
                output = False
                return output
        # if all is well, return True
        return output
    except Exception as e:
        print(e)
        output = False
        return output


def handle_wapp_static_container(app_path, katana_static, _copy):
    if _copy:
        return copy_katana_static(join_path(
            app_path, 'static'), katana_static)
    else:
        return delete_katana_static(join_path(katana_static), join_path(
            app_path, 'static'))

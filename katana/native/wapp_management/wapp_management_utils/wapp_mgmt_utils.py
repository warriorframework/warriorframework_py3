import copy
import os
import shutil
import zipfile
from katana.utils import git_utils

from distutils.version import LooseVersion

from katana.wui.core.core_utils import core_utils
from utils.directory_traversal_utils import join_path, get_sub_files, get_parent_directory, \
    create_dir, get_dir_from_path
from utils.navigator_util import Navigator
from utils.string_utils import get_repository_name
from utils.file_utils import copy_dir

nav_obj = Navigator()

# path to katana/static
# define as a global variable
katana_static = join_path(nav_obj.get_katana_dir(), 'static')


def get_version_list(versions, existing_versions):
    """
    :param versions: comma separated version list.
        Eg: warrior-3.2.0, warrior-3.1.0::warrior-3.7.0, :warrior3.6.0
    :param existing_versions: List/Set of existing versions:
        [warrior-3.1.0, warrior-3.1.1, warrior-3.2.0 ...]
    :return:
        individual: List of versions
            Eg: [warrior-3.1.0, warrior-3.1.1, warrior-3.2.0 ...]
        bounds: range of versions
            Eg: [{"upper": "warrior-3.7.0", "lower": "warrior-3.4.0"}, {"upper": "warrior-3.2.0"}]
        errors: Boolean if any errors occurred during evaluation.
    """
    bounds = []
    individual = []
    errors = False
    if not existing_versions:
        return individual, bounds, True
    version_list = [el.strip() for el in versions.split(',') if el.strip() != ""]
    err_msg = "-- An Error Occurred -- {0} is not a valid Warrior version. Valid Warrior versions are: {1}"
    for el in version_list:
        bound = {}
        if el.startswith(":"):
            el = el[1:].strip()
            if el in existing_versions:
                bound["upper"] = el
                bounds.append(copy.deepcopy(bound))
            else:
                print(err_msg.format(el, ', '.join(existing_versions)))
                errors = True
        elif "::" in el:
            el_list = el.split("::")
            if el_list[1].strip() in existing_versions:
                bound["upper"] = el_list[1]
                if el_list[0].strip() in existing_versions:
                    bound["lower"] = el_list[0]
                else:
                    print(err_msg.format(el, ', '.join(existing_versions)))
                    errors = True
            else:
                print(err_msg.format(el, ', '.join(existing_versions)))
                errors = True
            if len(list(bound.keys())) == 2:
                bounds.append(copy.deepcopy(bound))
        else:
            if el in existing_versions:
                individual.append(el)
            else:
                print(err_msg.format(el, ', '.join(existing_versions)))
                errors = True
    return individual, bounds, errors


def check_against_version_list(version, version_list, version_bounds):
    """
    :param version: version to be verified
    :param version_list: List of versions
            Eg: [warrior-3.1.0, warrior-3.1.1, warrior-3.2.0 ...]
    :param version_bounds: range of versions
            Eg: [{"upper": "warrior-3.7.0", "lower": "warrior-3.4.0"}, {"upper": "warrior-3.2.0"}]
    :return:
        status: Boolean. True if version is valid, False if not.
    """
    status = False
    for el in version_list:
        if version == el:
            status = True
            break
    if not status:
        for bound in version_bounds:
            if LooseVersion(version) <= LooseVersion(bound["upper"]):
                if "lower" in bound:
                    if LooseVersion(version) >= LooseVersion(bound["lower"]):
                        status = True
                        break
                else:
                    status = True
                    break
    return status


def extract_zip(zip_src, dst, output_data):
    """
    Extract zip source
    :param zip_src: src file
    :param dst: dst directory
    :param output_data: error message object
    :return:
    """
    try:
        zip_ref = zipfile.ZipFile(join_path(dst, zip_src), 'r')
        zip_ref.extractall(dst)
        zip_ref.close()
        return True
    except Exception as e:
        print("-- An Error Occurred -- {0}".format(e))
        output_data["message"] = "-- An Error Occurred -- {0}".format(e)
        output_data["status"] = False
        return False


def handle_error(exception_object, output_data):
    output_data["status"] = False
    output_data["message"] = "-- An Error Occurred -- {0}".format(
        exception_object)
    return output_data


def handle_path_error(app_path, output_data):
    """
    Handle path error by populating output_data dict with err message
    :param app_path: path to wapp
    :param output_data: error message object
    """
    output_data["status"] = False
    output_data["message"] = "-- An Error Occurred -- {0} does not exist".format(
        app_path)
    print(output_data["message"])


def handle_git_sources(app_path, temp_dir_path, output_data):
    """
    Handle installation of git sources
    :param app_path: path to wapp
    :param temp_dir_path: path to temp directory i.e. ../.data/temp
    :param output_data: error message object
    :return:
    """
    if git_utils.check_url_is_a_valid_repo(app_path):
        repo_name = get_repository_name(app_path)
        os.system("git clone {0} {1}".format(
            app_path, join_path(temp_dir_path, repo_name)))
        app_path = join_path(temp_dir_path, repo_name)
        # return from the git_sources
        return True, app_path
    else:
        # git details not valid, return false
        return False, app_path


def handle_zip_sources(app_path, temp_dir_path, output_data):
    """
    Handle installation of zip sources
    :param app_path: path to wapp
    :param temp_dir_path: path to temp directory i.e. ../.data/temp
    :param output_data: error message object
    :return:
    """
    if os.path.exists(app_path):
        zip_path = app_path.split(os.sep)
        zip_path_len = len(zip_path)
        # Zip file is the last element in the list
        zip_name = zip_path[zip_path_len - 1]
        shutil.copyfile(app_path, join_path(temp_dir_path, zip_name))
        if extract_zip(zip_name, temp_dir_path, output_data):
            app_path = join_path(temp_dir_path, zip_name[:-4])
            return True, app_path
        else:
            # Error if any, is already handled in extract_zip
            return False, app_path
    else:
        handle_path_error(app_path, output_data)
        return False, app_path


def handle_directory_sources(app_path, temp_dir_path, output_data):
    """
    Install wapp given a wapp directory
    :param app_path: path to wapp
    :param temp_dir_path: path to temp directory i.e. ../.data/temp
    :param output_data: error message object
    :return:
    """
    # proceed only if app is a directory structure
    if os.path.isdir(app_path):
        filename = get_dir_from_path(app_path)
        # else do a normal copy_dir inside katana/wapps
        status = copy_dir(app_path, join_path(temp_dir_path, filename))
        app_path = join_path(temp_dir_path, filename)
        return status, app_path
    else:
        handle_path_error(app_path, output_data)
        status = False
        return status, app_path


def handle_wapp_sources(app_path, dot_data_dir, temp_dir_path, output_data):
    """
    Handle all wapp sources including git, zip and directory
    :param app_path: path to wapp
    :param dot_data_dir:
    :param temp_dir_path: path to temp directory i.e. ../.data/temp
    :param output_data: error message object
    :return:
    """
    if app_path.endswith(".git"):
        return handle_git_sources(app_path, temp_dir_path, output_data)
    elif app_path.endswith(".zip"):
        return handle_zip_sources(app_path, temp_dir_path, output_data)
    return handle_directory_sources(app_path, temp_dir_path, output_data)

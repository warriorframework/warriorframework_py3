#!/usr/bin/python3
import os
import shutil
from katana.utils import user_utils

def getpath(request):
    """
    This function is to get the path of the User-data location.
    Whatever is pointed to by this path is displayed.
    Currently, a static path is read from the file in my VM and the contents are displayed.
    The file is opened and the path is read

    :return: The path to user-data space
    """
    Object = user_utils.UserData('file_manager')
    return Object.get_user_path(request)

def delete(path):
    """
    This will check if it's a file or directory and then delete them.

    :param path: Full path to File or Directory which has to be deleted.
    :return: A string saying success or error
    """
    result = False
    if (os.path.isdir(path)):
        try:
            shutil.rmtree(path)
            result = True
            # return 'success'
        except OSError:
            print(path + 'Cannot delete Directory')

    elif (os.path.isfile(path)):
        try:
            os.remove(path)
            result = True
        except OSError:
            print(path + 'Cannot delete File')
    return result

def rename(file_path, old_name, new_name):
    """
    This function will rename the file or directory.

    :param file_path: The full path of the file or directory
    :param old_name: Old Name of the file or directory
    :param new_name: New Name of file or directory
    :return: String containing success or error.
    """
    new_file_path = os.path.join(os.path.dirname(file_path), new_name)
    try:
        os.rename(file_path, new_file_path)
    except os.error as e:
        print(str(e))
        (bool,result) = False,str(e)
    (bool, result) = True,'success'
    return (bool,result)

def save(file_name, username, host, port, destdir, transfer_proto, request):
    """
    This function is to save the user-ftp-login details. Password is not stored.
    A file is created and the details are written into this file.

    :param file_name: File name
    :param username: User Input
    :param host: User Input
    :param port: User Input. Default is 21.
    :param destdir: User Input. Default is ''
    :param transfer_proto: User Input. Default is FTP
    :return: String error or list of cached files in .data directory
    """

    Object = user_utils.UserData('file_manager')
    parent_path = Object.get_dotdata_dir(request)
    try:
        result = []
        fp = open(file_name, 'w')
        write_lines = [username, host, str(port), transfer_proto, destdir]
        write_lines = '\n'.join(write_lines)
        fp.writelines(write_lines)
        fp.close()
        result = os.listdir(parent_path)
    except Exception as e:
        result = 'error : ' + str(e)
    return result

def read_cache(cache_name, request):
    """
    To read the cached details in the file cache_name

    :param cache_name: File Name
    :return: Details of the file
    """
    # parent_path = os.path.join(getpath(request),"File Manager/.data")
    Object = user_utils.UserData('file_manager')
    parent_path = Object.get_dotdata_dir(request)
    try:
        os.chdir(parent_path)
    except:
        return 'error'

    try:
        fp = open(cache_name, 'r')
        result_temp = fp.readlines()
        result = []
        for temp in result_temp:
            result.append(temp.strip('\n'))
        fp.close()
    except:
        result = 'Could not read from file'
    return result


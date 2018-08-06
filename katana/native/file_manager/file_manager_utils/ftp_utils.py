#!/usr/bin/python3
import os
import ftplib
from ftplib import FTP
from katana.native.file_manager.views import getpath

def ftpfile(host, port, username, passwd, destdir, files_path, files_name, all_files_path):
    """
    The main FTP function which takes in input details and FTPs the files.
    A FTP session is created.

    :param host: User Input (IP address)
    :param port: User Input (Default 21)
    :param username: Username of the Target machine
    :param passwd: Password of the target machine
    :param destdir: Location from the root directory in the Target Machine where the files should be FTPed into
    :param files_path: Full path of the top level files/directories selected
    :param files_name: Names of the top level files/directories selected
    :param all_files_path: List of All the files/directories selected (due to down cascading)
    :return: Error message or list of files FTPed with status.
    """
    result = []
    os.chdir(getpath())
    try:
        ftp = FTP('')
        ftp.connect(host, port)
        ftp.login(username, passwd)
        try:
            if(change_destination(ftp, destdir)):
                for path, name in zip(files_path, files_name):
                    if os.path.isfile(path):
                        result.append(transfer_file(ftp, path, name))
                    elif os.path.isdir(path):
                        result.append(name + ': Is a directory')
                        result.append(isDir(ftp, path, name, files_path, files_name, all_files_path))
                    else:
                        result.append(name + ': Is not a file or directory')
            else:
                result.append(destdir + " :Could Not Change to Destination Directory Successfully")
                return result
        except ftplib.all_errors as e:
            result.append(str(e))
        ftp.quit()
    except ftplib.all_errors as e:
        result.append(str(e))
    return result


def change_destination(ftp, destdir):
    """
    If the destiantion directory is different than the root in the target machine, then this function traverses into
    the destination directory in the target machine.

    :param ftp: FTP object
    :param destdir: Destination directory from the root directory where the files are to be FTPed.
    :return: Boolean.
    """
    try:
        if destdir != '':
            ftp.cwd(destdir)
    except:
        print('\nCould not change to destination directory')
        return False
    return True


def transfer_file(ftp, path, name):
    """
    This function FTPs the file. Some files have to be sent as binary format and some as ascii format.

    :param ftp: FTP object
    :param path: Full path to file name
    :param name: File name
    :return: Status of the file transfer
    """
    fp = open(path, 'rb')
    try:
        ext = os.path.splitext(name)[1]
        # check if the extension needs to be sent in binary mode. Default is ASCII mode.
        if ext == '.docx' or ext == '.doc':
            ftp.storbinary('STOR ' + name, fp)
        else:
            ftp.storlines('STOR ' + name, fp)
        # storlines prints new line character at the end of each line in text file
        # but it does not transfer word files.
    except:
        return name + ': Could not transfer the file.'
    fp.close()
    return name + ' :Success'


def isDir(ftp, path, name, files_path, files_name, all_files_path):
    """
    If the selected item is a directory, then this is a recursive function that FTPs all the files selected within
    the directory. If the item selected is a directory, then this function is called on that directory.

    The Directory structure is recreated in the target machine.

    This also checks if there are any broken tree files. These are files which are not associated to a parent but has
    some ancestor selected.

    :param ftp: FTP object
    :param path: Full path of the directory
    :param name: Name of the directory
    :param files_path: Full path of the items selected within the directory
    :param files_name: Names of the items selected within the directory
    :param all_files_path: all the items in the directory
    :return: Status or error
    """
    result = []
    parent_dir = ftp.pwd()
    if parent_dir == '/':
        new_folder = parent_dir + name
    else:
        new_folder = parent_dir + '/' + name
    try:
        try:
            ftp.mkd(new_folder)
            ftp.cwd(new_folder)
        except:
            print('error in creating new directory in target machine')
            result.append(new_folder + ': Such a Folder already exists')
            return result
        files_list = os.listdir(path)
        try:
            for item in files_list:
                # Need to check if the item is in the files_path
                if path == '/':
                    item_path = path + item
                else:
                    item_path = path + '/' + item
                if item_path in all_files_path:
                    try:
                        if os.path.isdir(item_path):
                            result.append(isDir(ftp, item_path, item, files_path, files_name, all_files_path))
                        elif os.path.isfile(item_path):
                            result.append(transfer_file(ftp, item_path, item))
                    except:
                        print('Error in recursive part')
                # To check if there is any broken files selected
                elif os.path.isdir(item_path):
                    broken_files = os.listdir(item_path)
                    for broken_item in broken_files:
                        broken_item_path = item_path + '/' + broken_item
                        if broken_item_path in all_files_path:
                            print('broken tree file: ' + broken_item_path)
                            result.append(broken_item_path + ' :broken tree file')
            ftp.cwd(parent_dir)
        except:
            print('Error in for loop')
    except:
        print('error somewhere else')
    return result
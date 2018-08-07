#!/usr/bin/python3
import os



def scpfile(host, port, username, passwd, destdir, files_path, all_files_path, files_name):
    """
        The main SCP function which takes in input details and SCPs the files.
        A underlying SSH session is created over which the files are SCPed.

        :param host: User Input (IP address)
        :param port: User Input (Default 22)
        :param username: Username of the Target machine
        :param passwd: Password of the target machine
        :param destdir: Location from the root directory in the Target Machine where the files should be FTPed into
        :param files_path: Full path of the top level files/directories selected
        :param files_name: Names of the top level files/directories selected
        :param all_files_path: List of All the files/directories selected (due to down cascading)
        :return: Error message or list of files FTPed with status.
        """
    try:
        import paramiko
    except ImportError:
        return 'Paramiko Package Missing! Contact System Administrator to install Paramiko 2.4.1 or up!'

    try:
        from scp import SCPClient
    except ImportError:
        return 'SCP Package Missing! Contact System Administrator to install SCP 0.11.0 or up!'

    result = []

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(host, port, username, passwd)
    except paramiko.SSHException as e:
        ssh.close()
        return str(e)
    if destdir != '' :
        result_destdir = change_destination(ssh, destdir)
        if 'Error' in result_destdir:
            return 'Error in Changing Destination'

    if not check_partial_folder(files_path, files_name, all_files_path):
        return 'Partial Folder Copy'

    try:
        scp = SCPClient(ssh.get_transport())
        for temp, temp_name in zip(files_path, files_name):
            # flag = True
            try:
                if os.path.isdir(temp):
                    # It's a directory. Check for partial directory

                    if destdir =='':
                        if ' ' in temp_name:
                            temp_name = str(temp_name)
                            temp_name = temp_name.replace(' ','_')
                        scp.put(temp, temp_name, True)
                    else:
                        scp.put(temp, destdir, True)
                else:
                    # It's a file
                    if destdir == '':
                        scp.put(temp)
                    else:
                        scp.put(temp, destdir)
                result.append(temp_name + ': Success')
            except:
                result.append((temp_name + ': Transfer Error'))
    except (RuntimeError, SystemError) as e:
        ssh.close()
        return str(e)
    ssh.close()
    return result

def ssh_connection(host, port, username, passwd):
    """
    This function sets up the ssh connection

    :param host: host ip
    :param port: port number. Default is 22
    :param username: username
    :param passwd: password
    :return: ssh object
    """
    try:
        import paramiko
    except ImportError:
        return 'Paramiko Package Missing! Contact System Administrator to install Paramiko 2.4.1 or up!'

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(host, port, username, passwd)
    except paramiko.SSHException as e:
        return str(e)
    return ssh

def change_destination(ssh, destdir):
    """
    This function changes the destination directory

    :param ssh: ssh object
    :param destdir: destination directory
    :return: success or error string
    """
    try:
        ssh.exec_command('mkdir ' + destdir)
        return 'Success'
    except:
        return 'Error in creating Destination Directory'

def check_partial_folder(files_path, files_name, all_files_path):
    """
    Checks if the top level directory contains partially selected files
    :param files_path: top level selected files path
    :param files_name: top level selected name
    :param all_files_path: all files' path which are selected
    :return: boolean
    """
    print(files_path)
    for temp, temp_name in zip(files_path, files_name):
        try:
            list = os.listdir(temp)
            for element in list:
                element_path = os.path.join(temp, element)
                # print(element_path)
                # if element_path is a directory, check for partial selection
                if os.path.isdir(element_path):
                    list_path = []
                    list_path.append(element_path)
                    list_item = []
                    list_item.append(element)
                    flag = check_partial_folder(list_path, list_item, all_files_path)
                    if flag == False:
                        return False
                elif element_path not in all_files_path:
                    return False
        except:
            print('File selected')
    return True
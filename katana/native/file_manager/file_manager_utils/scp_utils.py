#!/usr/bin/python3
import os
import paramiko
import scp
from scp import SCPClient

def scpfile(host, port, username, passwd, destdir, files_path, files_name):
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


    try:
        scp = SCPClient(ssh.get_transport())
        for temp, temp_name in zip(files_path, files_name):
            try:
                if os.path.isdir(temp):
                    # It's a directory
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
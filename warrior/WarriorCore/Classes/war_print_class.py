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

"""
This class will trap stdout and redirects the message to logfile and stdout
It takes console_logfile and write_to_stdout ( boolean flag) as arguments.

!!! Important!!!
DO NOT import any modules from warrior/Framework package that uses
warrior/Framework/Utils/print_Utils.py at module level into this module
as it will lead to cyclic imports.

"""
import sys
import re
import os
import socket
import logging
import re

def print_all(message, print_type, color_message=None, log_level="INFO", *args, **kwargs):
    if print_type == "":
        print(message)
    elif print_type != "":
        host_name = socket.gethostname()
        p_id = os.getpid()
        extra_msg = {"pid":p_id,"host_name":host_name}
        FORMAT = '%(asctime)-15s %(host_name)-8s %(pid)s %(levelname)s %(message)s'
        logging.basicConfig(format=FORMAT)
        logger = logging.getLogger()
        if log_level == "DEBUG":
            logger.setLevel(logging.DEBUG)
        elif log_level == "INFO":
            logger.setLevel(logging.INFO)
        elif log_level == "WARNING":
            logger.setLevel(logging.WARNING)
        elif log_level == "ERROR":
            logger.setLevel(logging.ERROR)
        elif log_level == "NOTSET":
            logger.setLevel(logging.NOTSET)
        elif log_level == "CRITICAL":
            logger.setLevel(logging.CRITICAL)
        if print_type == "-I-":
            matched = re.match("^=+",message) or re.match("^\++",message)
            if matched:
                print(message)
            else:
                logger.info(message, extra=extra_msg)
        elif print_type == "\x1b[1;33m-W-\x1b[0m":
            logger.warning(message, extra=extra_msg)
        elif print_type == "-E-":
            logger.error(message, extra=extra_msg)
        elif print_type == "-N-":
            logger.info(message, extra=extra_msg)
        elif print_type == "-D-":
            logger.debug(message, extra=extra_msg)

def print_main(message, print_type, color_message=None, *args, **kwargs):
    """The main print function will be called by other print functions
    """
    # import pdb; pdb.set_trace()
    arg_list = sys.argv
    if len(arg_list)>2:
        if sys.argv[2] in ["loglevel=0","loglevel=10","loglevel=20","loglevel=30","loglevel=40","loglevel=50"]:
            log_levels = {"loglevel=0":"NOTSET","loglevel=10":"DEBUG","loglevel=20":"INFO","loglevel=30":"WARNNG","loglevel=40":"ERROR","loglevel=50":"CRITICAL"}
            level = log_levels[sys.argv[2]]
            print_all(message, print_type, log_level=level, color_message=None, *args, **kwargs)
        else:
            print_all(message, print_type, color_message=None, *args, **kwargs)
    else:
        print_all(message, print_type, color_message=None, *args, **kwargs)

class RedirectPrint(object):
    """Class that has methods to redirect prints
    from stdout to correct console log files """
    def __init__(self, console_logfile):
        """Constructor"""
        self.get_file(console_logfile)
#         self.write_to_stdout = write_to_stdout
        self.stdout = sys.stdout
        self.console_full_log = None
        self.console_add = None
        self.katana_obj = None

    def katana_console_log(self, katana_obj):
        """
            set the console log object to be the katana communcation object
        """
        self.console_full_log = katana_obj["console_full_log"]
        self.console_add = katana_obj["console_add"]
        self.katana_obj = katana_obj

    def get_file(self, console_logfile):
        """If the console logfile is not None redirect sys.stdout to
        console logfile
        """
        self.file = console_logfile
        if self.file is not None:
            sys.stdout = self

    def write(self, data, logging=True):
        """
        - Writes data to the sys.stdout
        - Writes data to log file only if the logging is True
        - Removes the ansii escape chars before writing to file
        """
        self.stdout.write(data)
        ansi_escape = re.compile(r'\x1b[^m]*m')
        data = ansi_escape.sub('', data)
        # write to log file if logging is set to True
        if logging is True:
            self.file.write(data)
            self.file.flush()
        if self.katana_obj is not None and "console_full_log" in self.katana_obj\
        and "console_add" in self.katana_obj:
            self.katana_obj["console_full_log"] += data
            self.katana_obj["console_add"] += data

    def isatty(self):
        """Check if sys.stdout is a tty """
        # print self.stdout.isatty()
        return self.stdout.isatty()

    def flush(self):
        """flush logfile """
        return self.stdout.flush()

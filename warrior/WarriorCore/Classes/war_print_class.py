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
import os
import socket
import logging
import re
import io
import multiprocessing

def py_logger(message, print_type, color_message=None, log_level="INFO", *args, **kwargs):
    host_name = socket.gethostname()

    cur_process = multiprocessing.current_process().name
    extra_msg = {"cur_process": cur_process, "host_name": host_name}
    formatter = logging.Formatter('%(asctime)-15s %(host_name)s %(cur_process)-8s %(levelname)s ::%(message)s','%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setFormatter(formatter)
    logger.setLevel(logging.INFO)

    if print_type == "":
        print(message)
    elif print_type != "":
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
    logger.addHandler(ch)
    logger = logging.LoggerAdapter(logger, extra_msg)

    if print_type == "-I-":
        matched = re.match("^=+",message) or re.match("^\++",message) or re.match("^\*+",message)  or re.match("^\n<<",message) \
        or re.match("^\n\**",message)
        if matched:
            print(message.strip())
        elif message.strip() == '':
            pass
        elif message.startswith("["):
            msg = message.split()
            logger.info(" ".join(msg[2:]), extra=extra_msg)
        else:
            logger.info(message, extra=extra_msg)
    elif print_type == "\x1b[1;33m-W-\x1b[0m":
        logger.warning(message, extra=extra_msg)
    elif print_type == "-E-" or print_type == "\x1b[1;33m-E-\x1b[0m":
        logger.error(message, extra=extra_msg)
    elif print_type == "-N-":
        logger.info(message, extra=extra_msg)
    elif print_type == "-D-":
        logger.debug(message, extra=extra_msg)
    elif print_type == "-C-":
        logger.critical(message, extra=extra_msg)

    log_contents = log_capture_string.getvalue()
    if log_contents != '':
        if isinstance(sys.stdout, RedirectPrint):
            sys.stdout.write((log_contents),
                             logging=kwargs.get('logging', True))
        else:
            sys.stdout.write(log_contents)
        sys.stdout.flush()
        from warrior.Framework.Utils.testcase_Utils import TCOBJ
        if TCOBJ.pnote is False:
            TCOBJ.p_note_level(log_contents, print_type)
        return log_contents


def print_main(message, print_type, color_message=None, *args, **kwargs):
    """The main print function will be called by other print functions
    """
    # import pdb; pdb.set_trace()
    if color_message is not None:
        print_string = str(color_message)
    elif color_message is None:
        print_string = str(message)
    if args:
        print_string = str(message) + str(args)
    arg_list = sys.argv
    if len(arg_list) > 3:
        cmd =sys.argv[2].upper()+"="+sys.argv[3].upper()
        if cmd in ["-LOGLEVEL=NOTSET","-LOGLEVEL=DEBUG","-LOGLEVEL=INFO","-LOGLEVEL=WARNING","-LOGLEVEL=ERROR","-LOGLEVEL=CRITICAL"]:
            log_levels = {"-LOGLEVEL=NOTSET":"NOTSET","-LOGLEVEL=DEBUG":"DEBUG","-LOGLEVEL=INFO":"INFO","-LOGLEVEL=WARNING":"WARNING","-LOGLEVEL=ERROR":"ERROR","-LOGLEVEL=CRITICAL":"CRITICAL"}
            level = log_levels[cmd]
            py_logger(print_string, print_type, log_level=level, color_message=None, *args, **kwargs)
        else:
            py_logger(print_string, print_type, color_message=None, *args, **kwargs)
    else:
        py_logger(print_string, print_type, color_message=None, *args, **kwargs)

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

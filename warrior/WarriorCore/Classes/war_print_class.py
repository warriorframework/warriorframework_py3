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

#pylint: disable=wrong-import-position
#pylint: disable=global-statement

import sys
import re
import logging
LOG_MESSAGE = None
LOGGER = None
DEFAULT_LOGLEVEL = logging.INFO
DEFAULT_HEADER_FORMAT = None
LOGLEVEL_DICT = {'info': logging.INFO, 'debug': logging.DEBUG,
                 'warning': logging.WARNING, 'error': logging.ERROR,
                 'critical': logging.CRITICAL}
if '--loglevel' in sys.argv:
    LEVEL_INDEX = sys.argv.index('--loglevel')
    if len(sys.argv) >= LEVEL_INDEX+1:
        LEVEL_VALUE = sys.argv[LEVEL_INDEX+1]
        logging_arg_value = LEVEL_VALUE.split(':')
        if ':' in LEVEL_VALUE:
            LEVEL_VALUE = logging_arg_value[0]
            DEFAULT_HEADER_FORMAT = logging_arg_value[1]
        else:
            if LEVEL_VALUE == 'no_headers':
                DEFAULT_HEADER_FORMAT = LEVEL_VALUE
                LEVEL_VALUE = DEFAULT_LOGLEVEL

    else:
        LEVEL_VALUE = 'info'
    DEFAULT_LOGLEVEL = LOGLEVEL_DICT.get(LEVEL_VALUE, logging.INFO)

def print_main(message, print_type, color_message=None, *args, **kwargs):
    """The main print function will be called by other print functions
    """
    global DEFAULT_LOGLEVEL
    if color_message is not None:
        print_string = str(color_message)
    elif color_message is None:
        print_string = str(message)
    if args:
        print_string = (str(message) + str(args))
    print_string.strip("\n")
    # matched = re.match(r"^=+", print_string) or re.match(r"^\++", print_string)\
    #           or re.match(r"^\*+", print_string)  or re.match(r"^\n<<", print_string)\
    #           or re.match(r"^\n\**", print_string)
    # if matched:
    #     print_string = None
    if print_string.strip() == '':
        print_string = None
    elif print_string.startswith("["):
        msg = print_string.split()
        print_string = " ".join(msg[2:])
    global LOGGER
    if not LOGGER:
        LOGGER = logging.getLogger('notype')
        LOGGER.setLevel(DEFAULT_LOGLEVEL)
        formatter = logging.Formatter('%(message)s')
        hdlr = logging.StreamHandler()
        hdlr.setFormatter(formatter)
        LOGGER.addHandler(hdlr)
    if not print_type:
        LOGGER.info(print_string)
        return print_string
    global LOG_MESSAGE
    if not LOG_MESSAGE:
        console_logger = logging.getLogger('console')
        console_logger.setLevel(DEFAULT_LOGLEVEL)
        if DEFAULT_HEADER_FORMAT == "no_headers":
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter('%(asctime)-7s %(levelname)-5s:: \
%(message)s', '%H:%M:%S')
        hdlr = logging.StreamHandler()
        hdlr.setFormatter(formatter)
        console_logger.addHandler(hdlr)
        LOG_MESSAGE = {"-I-": console_logger.info, \
                       "-N-": console_logger.info, "-W-": console_logger.warning,\
                       "-E-": console_logger.error, "-D-": console_logger.debug,\
                       "-C-": console_logger.critical}
    # set logging argument default to True, to write the message in the log file
    if isinstance(sys.stdout, RedirectPrint):
        sys.stdout.print_type = print_type
        sys.stdout.log_message = LOG_MESSAGE
        log_in_file = False if print_type == "-N-" else True
        if print_string:
            sys.stdout.write(print_string,
                             log=kwargs.get('log', log_in_file))
    else:
        if print_string:
            LOG_MESSAGE[print_type](print_string)
    from warrior.Framework.Utils.testcase_Utils import TCOBJ
    if TCOBJ.pnote is False:
        TCOBJ.p_note_level(message, print_type)
    return print_string


class RedirectPrint(object):
    """Class that has methods to redirect prints
    from stdout to correct console log files """
    def __init__(self, console_logfile):
        """Constructor"""
        self.get_file(console_logfile)
        self.stdout = sys.stdout
        self.console_full_log = None
        self.console_add = None
        self.katana_obj = None
        self.log_message = None
        self.print_type = "-I-"
        self.file_logger = logging.getLogger('file')
        global DEFAULT_LOGLEVEL
        self.file_logger.setLevel(DEFAULT_LOGLEVEL)
        self.hdlr = None
        if DEFAULT_HEADER_FORMAT == "no_headers":
            self.formatter = logging.Formatter('%(message)s')
        else:
            self.formatter = logging.Formatter('%(asctime)-7s %(levelname)-5s :: \
%(message)s', '%H:%M:%S')
        self.logfile_message = {"-I-": self.file_logger.info, "-W-": self.file_logger.warning, \
                                "-E-": self.file_logger.error, "-D-": self.file_logger.debug, \
                                "-C-": self.file_logger.critical, \
                                "-N-": self.file_logger.info}

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

    def write(self, data, log=True):
        """
        - Writes data to the sys.stdout
        - Writes data to log file only if the logging is True
        - Removes the ansii escape chars before writing to file
        """
        if isinstance(data, str):
            self.log_message[self.print_type](data)
        else:
            data = data.decode('utf-8')
            # self.stdout.write(data)
            self.log_message[self.print_type](data)

        # write to log file if logging is set to True
        if log is True:
            ansi_escape = re.compile(r'\x1b[^m]*m')
            data = ansi_escape.sub('', data)
            if self.hdlr is None or (self.hdlr and self.hdlr.baseFilename != self.file.name):
                self.hdlr = logging.FileHandler(self.file.name)
                self.hdlr.setFormatter(self.formatter)
                self.file_logger.addHandler(self.hdlr)
            self.logfile_message[self.print_type](data)

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

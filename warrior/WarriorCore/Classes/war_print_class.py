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


def print_main(message, print_type, color_message=None, *args, **kwargs):
    """The main print function will be called by other print functions
    """
    if color_message is not None:
        print_string = print_type + " " + str(color_message)
    elif color_message is None:
        print_string = print_type + " " + str(message)
    if args:
        print_string = (print_type + " " + str(message) + str(args))
    # set logging argument default to True, to write the message in the log file
    if isinstance(sys.stdout, RedirectPrint):
        sys.stdout.write((print_string + '\n'),
                         logging=kwargs.get('logging', True))
    else:
        sys.stdout.write(print_string + '\n')
    sys.stdout.flush()
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

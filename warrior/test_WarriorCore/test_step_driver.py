"""
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
"""

import sys
import os
from unittest.mock import MagicMock
from os.path import abspath, dirname
import unittest
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

import datetime
import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)

from warrior.WarriorCore import step_driver
from warrior.WarriorCore.Classes.junit_class import Junit


def test_main():
    """Get a step, executes it and returns the result """
    cwd = os.getcwd()
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "step_driver_testcase.xml"))
    step_list = tree.findall('Steps/step')
    step_num = 0
    for stp in step_list:
        step = stp
        step_num = step_num + 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        wt_resultsdir = cwd
        wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit
        data_repository = {'wt_junit_object':wt_junit_object, 'wt_filename':'step_driver_testcase.xml',\
        'wt_logsdir':cwd, 'wt_kw_results_dir':cwd, 'wt_def_on_error_action':'NEXT',\
         'wt_tc_timestamp':timestamp, 'wt_resultsdir':wt_resultsdir, 'wt_name':\
         'step_driver_testcase', 'war_parallel':True, 'war_file_type':'Case', 'wt_step_type':'step'}
        system_name = None
        kw_parallel = True

    step_driver.main(step, step_num, data_repository, system_name, kw_parallel, queue=None,
         skip_invoked=True)

#   def test_execute_step():
#     """ Executes a step from the testcase xml file
#         - Parses a step from the testcase xml file
#         - Get the values of Driver, Keyword, impactsTcResult
#         - If the step has arguments, get all the arguments and store them as key/value pairs in
#           args_repository
#         - Sends the Keyword, data_repository, args_repository to the respective Driver.
#         - Reports the status of the keyword executed (obtained as return value from the respective
#           Driver)

#     Arguments:
#     1. step            = (xml element) xml element with tag <step> containing the details of the
#                          step to be executed like (Driver, Keyword, Arguments, Impact etc..)
#     2. step_num        = (int) step number being executed
#     3. data_repository = (dict) data_repository of the testcase
#     """
#     cwd = os.getcwd()
#     tree = ET.parse(os.path.join(os.path.split(__file__)[0], "step_driver_testcase.xml"))
#     step_list = tree.findall('Steps/step')
#     step_num = 0
#     for stp in step_list:
#         step = stp
#         step_num = step_num + 1
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#         wt_resultsdir = cwd
#         wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit
#         warrior.WarriorCore.Classes.junit_class.Junit.add_property = MagicMock()
#         add_property = MagicMock()
#         data_repository = {'wt_junit_object':wt_junit_object, 'wt_filename':'step_driver_testcase.xml',\
#         'wt_logsdir':cwd, 'wt_kw_results_dir':cwd, 'wt_def_on_error_action':'NEXT',\
#          'wt_tc_timestamp':timestamp, 'wt_resultsdir':wt_resultsdir, 'wt_name':\
#          'step_driver_testcase', 'war_parallel':True, 'war_file_type':'Case', 'wt_step_type':'step'}
#         system_name = None
#         kw_parallel = True
#     step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel,
#      queue=None, skip_invoked=True)

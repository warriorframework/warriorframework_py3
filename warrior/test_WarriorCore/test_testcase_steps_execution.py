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

import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
from warrior.Framework import Utils
from warrior.WarriorCore import testcase_steps_execution

def test_execute_steps():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """

    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = True
    step_num = None
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    result = testcase_steps_execution.execute_steps(step_list, data_repository, system_name,\
     parallel, queue, skip_invoked=True, step_num=None)
    assert result == ([False, False], [[], []], ['impact', 'impact'])
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository

def test_execute_steps_with_parallel_true():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """

    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None}
    system_name = 'NE1'
    parallel = True
    queue = False
    skip_invoked = True
    step_num = 0
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    testcase_steps_execution.execute_steps(step_list, data_repository, system_name, parallel,\
     queue, skip_invoked=True, step_num=None)
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository

def test_execute_steps_with_step_and_parallel_true_and_skip_invoked_false():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """

    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = False
    step_num = 1
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    result = testcase_steps_execution.execute_steps(step_list, data_repository, system_name, parallel,\
     queue, skip_invoked, step_num=None)

    assert result == ([False, False], [[], []], ['impact', 'impact'],\
     {'wt_filename': 'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
       'wt_def_on_error_action': 'NEXT', 'wt_def_on_error_value': '', 'wt_junit_object': None,\
        'step_num': 2, 'wt_driver': 'common_driver', 'wt_plugin': None, 'wt_keyword':\
         'wait_for_timeout', 'wt_step_impact': 'impact', 'wt_step_context': 'positive',\
          'wt_step_description': '*** Description not provided by user ***'})

    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository

def test_execute_steps_with_step_num():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """

    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = False
    goto_stepnum = []
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    testcase_steps_execution.execute_steps(step_list, data_repository, system_name, parallel,\
     queue, skip_invoked, step_num=[1])
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository

def test_main():
    """ Executes a testcase """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))

    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = False
    goto_stepnum = []
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)

    result = testcase_steps_execution.main(step_list, data_repository, system_name=None, parallel=False, queue=False)
    assert result == ([False, False], [[], []], ['impact', 'impact'])

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')
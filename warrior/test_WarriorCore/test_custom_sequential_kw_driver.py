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
import datetime
import xml.etree.ElementTree as ET

import sys
import os
from unittest.mock import MagicMock
from os.path import abspath, dirname
from pathlib import Path
import unittest

try:
    import warrior
except Exception:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
from warrior.WarriorCore import custom_sequential_kw_driver
from warrior.WarriorCore import testcase_steps_execution
from warrior.WarriorCore import step_driver
from warrior.Framework import Utils

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass

def test_execute_custom_sequential_positive():
    """ Takes a list of steps as input and executes"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(result_dir+ "/" +'custom_seq_resultfile.xml', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'custom_seq_resultfile.xml')
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_seq.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    step_list = root.findall("Steps")
    data_repository = {'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'jiraproj',\
     'wt_logsdir':path, 'wt_resultfile':wt_resultfile, 'wt_step_impact': 'impact',\
      'wt_kw_results_dir':result_dir, 'wt_keyword':'wait_for_timeout', 'wt_tc_timestamp':timestamp}
    Utils.data_Utils.update_datarepository = MagicMock()
    testcase_steps_execution.main = MagicMock(return_value=([True], [wt_resultfile], ['impact']))
    tc_status = False
    system_name = None
    result = custom_sequential_kw_driver.execute_custom_sequential(step_list, data_repository,\
     tc_status, system_name)
    assert result == True
    del testcase_steps_execution.main
    del Utils.data_Utils.update_datarepository

def test_execute_custom_sequential_negative():
    """ Takes a list of steps as input and executes"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(result_dir+ "/" +'custom_seq_resultfile.xml', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'custom_seq_resultfile.xml')
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_seq.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    step_list = root.findall("Steps")
    data_repository = {'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'jiraproj',\
     'wt_logsdir':path, 'wt_resultfile':wt_resultfile, 'wt_step_impact': 'impact',\
      'wt_kw_results_dir':result_dir, 'wt_keyword':'wait_for_timeout', 'wt_tc_timestamp':timestamp}
    Utils.data_Utils.update_datarepository = MagicMock()
    testcase_steps_execution.main = MagicMock(return_value=([False], [wt_resultfile], ['impact']))
    tc_status = False
    system_name = None
    result = custom_sequential_kw_driver.execute_custom_sequential(step_list, data_repository,\
     tc_status, system_name)
    assert result == False
    del testcase_steps_execution.main
    del Utils.data_Utils.update_datarepository

def test_main_pasitive():
    """Executes the list of keyword in sequential order
    Computes and returns the testcase status"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(result_dir+ "/" +'custom_seq_resultfile.xml', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'custom_seq_resultfile.xml')
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_seq.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    step_list = root.findall("Steps")
    data_repository = {'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'jiraproj',\
     'wt_logsdir':path, 'wt_resultfile':wt_resultfile, 'wt_step_impact': 'impact',\
      'wt_kw_results_dir':result_dir, 'wt_keyword':'wait_for_timeout', 'wt_tc_timestamp':timestamp}
    Utils.data_Utils.update_datarepository = MagicMock()
    testcase_steps_execution.main = MagicMock(return_value=([True], [wt_resultfile], ['impact']))
    tc_status = False
    result = custom_sequential_kw_driver.main(step_list, data_repository, tc_status,\
     system_name=None)
    assert result == True
    del testcase_steps_execution.main
    del Utils.data_Utils.update_datarepository

def test_main_negative():
    """Executes the list of keyword in sequential order
    Computes and returns the testcase status"""
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_seq.xml"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(result_dir+"/"+'custom_seq_resultfile.txt', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'custom_seq_resultfile.txt')
    step_list = tree.findall('Steps')
    tc_status = False
    data_repository = {'wt_junit_object':None, 'wt_tc_timestamp':timestamp,\
     'wt_resultfile':wt_resultfile}
    result = custom_sequential_kw_driver.main(step_list, data_repository, tc_status,\
     system_name=None)
    assert result == False

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')

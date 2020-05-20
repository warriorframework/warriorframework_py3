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

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore.multiprocessing_utils import update_tc_junit_resultfile
from warrior.WarriorCore.Classes import junit_class
sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
from warrior.WarriorCore import custom_parallel_kw_driver

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass

def test_execute_custom_parallel():
    '''testcase for execute_custom_parallel'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_par.xml"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tc_timestamp = timestamp
    with open(result_dir+'/'+'resultfile.txt', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'resultfile.txt')
    step_list = tree.findall('Steps/step')
    tc_status = False
    system_name = 'NE1'
    pj_junit_display = False
    data_repository = {'wt_name':'testcase_step_exe'}
    tc_junit_object = junit_class.Junit(filename=data_repository['wt_name'],
                                        timestamp=tc_timestamp,
                                        name="customProject_independant_testcase_execution",
                                        display=pj_junit_display)
    data_repository = {'wt_junit_object':tc_junit_object, 'wt_tc_timestamp':timestamp,\
     'wt_resultfile':wt_resultfile, 'wt_filename':'testcase_step_exe',\
      'wt_step_impact':'impact', 'wt_logsdir':result_dir}
    update_tc_junit_resultfile = MagicMock(return_value='')
    result = custom_parallel_kw_driver.execute_custom_parallel(step_list, data_repository,\
     tc_status, system_name)
    assert result == True
    del update_tc_junit_resultfile

def test_main():
    """Executes the list of steps in parallel
    Computes and returns the testcase status"""
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_par.xml"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(result_dir+'/'+'resultfile.txt', 'w'):
        pass
    wt_resultfile = os.path.join(result_dir, 'resultfile.txt')
    step_list = tree.findall('Steps/step')
    tc_status = False
    data_repository = {'wt_junit_object':None, 'wt_tc_timestamp':timestamp,\
     'wt_resultfile':wt_resultfile}
    result = custom_parallel_kw_driver.main(step_list, data_repository, tc_status,\
     system_name=None)
    assert result == False
sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')

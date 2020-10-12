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
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass

from warrior.WarriorCore import testcase_steps_execution
from warrior.WarriorCore import testcase_driver
from warrior.Framework import Utils
from warrior.WarriorCore import testsuite_driver
from warrior.WarriorCore import testsuite_utils

def test_report_testsuite_result():
    """Reports the result of the testsuite executed
    """
    with open(result_dir+'/'+'result.xml', 'w') as fp:
        pass
    junit_resultfile = result_dir+'/'+'result.xml'
    suite_repository = {'junit_resultfile': junit_resultfile, 'suite_name': 'test'}
    suite_status = 'PASS'
    testsuite_utils.pSuite_report_suite_result = MagicMock(return_value=None)
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    result = testsuite_driver.report_testsuite_result(suite_repository, suite_status)
    assert result == None
    del testsuite_utils.pSuite_report_suite_result
    del aa

def test_execute_testsuite_parallel_cases():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver5.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite', 'wt_ts_impact':'impact'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert test1 == True
    assert result1 == True, result2 == dict
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_execute_testsuite_runmode_none():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True, True], [], ['impact', 'impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver2.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert test1 == True
    assert result1 == 'ERROR', result2 == dict
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_execute_testsuite_runmode_RUF():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True, True], [], ['impact', 'impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver3.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert test1 == True
    assert result1 == True, result2 == dict
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_execute_testsuite_exetype_RUF():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver6.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action=None, queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert test1 == True
    assert result1 == True, result2 == dict
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_execute_testsuite_runmode_RMT():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True, True], [], ['impact', 'impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver4.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action=None, queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert test1 == True
    assert result1 == True, result2 == dict
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_execute_testsuite():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver1.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.execute_testsuite(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert result1 == True, result2 == dict
    assert test1 == True
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_main_positive():
    """Executes the testsuite (provided as a xml file)
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    aa = os.getenv("WAR_TOOLS_DIR")
    aa = MagicMock(return_value=tools_dir)
    Utils.testcase_Utils.pStep = MagicMock(return_value=None)
    Utils.testcase_Utils.update_step_num = MagicMock(return_value=None)
    Utils.testcase_Utils.pSubStep = MagicMock(return_value=None)
    Utils.data_Utils.update_datarepository = MagicMock(return_value=None)
    Utils.testcase_Utils.report_substep_status = MagicMock(return_value=None)
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver1.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.main(testsuite_filepath, data_repository,\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    test1 = 'suite_name' in result2
    assert result1 == True, result2 == dict
    assert test1 == True
    del aa
    del Utils.testcase_Utils.pStep
    del Utils.testcase_Utils.update_step_num
    del Utils.testcase_Utils.pSubStep
    del Utils.data_Utils.update_datarepository
    del Utils.testcase_Utils.report_substep_status
    del testcase_steps_execution.main

def test_main_negitive():
    """Executes a test suite """
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver1.xml")
    result1, result2 = testsuite_driver.main(testsuite_filepath, data_repository={},\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action='next', queue=None, ts_parallel=False)
    assert result1 == False, result2 == dict

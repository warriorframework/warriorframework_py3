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
import datetime
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
from warrior.Framework.Utils import testcase_Utils
from warrior.WarriorCore import testcase_steps_execution
from warrior.WarriorCore import exec_type_driver
from warrior.WarriorCore.Classes.junit_class import Junit
from warrior.WarriorCore import common_execution_utils
from warrior.WarriorCore import step_driver
from warrior.WarriorCore import onerror_driver

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass


class test_TestCaseStepsExecutionClass(unittest.TestCase):
    """ Step Execution Class """
    def test__execute_current_step_except(self):
        """
        UT for _execute_current_step
        """
        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None,\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        # import pdb
        # pdb.set_trace()
        testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        common_execution_utils.compute_status = MagicMock(return_value=([True, True],\
         ['impact','impact']))
        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
         system_name, parallel, queue, skip_invoked=True)
        obj. _execute_current_step()
        del testcase_Utils.get_impact_from_xmlfile
        del common_execution_utils.compute_status

    def test__execute_current_step_try(self):
        """
        UT for _execute_current_step
        """
        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None,\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        step_driver.main = MagicMock(return_value=[True, wt_logsdir, 'impact'])
        Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        common_execution_utils.compute_status = MagicMock(return_value=([True, True],\
         ['impact','impact']))
        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
         system_name, parallel, queue, skip_invoked=True)
        obj. _execute_current_step()
        del step_driver.main
        del Utils.testcase_Utils.get_impact_from_xmlfile
        del common_execution_utils.compute_status

    # def test__skip_because_of_goto(self):
    #     '''
    #     UT for __run_execute_and_resume_mode
    #     '''
    #     from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
    #     timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    #     tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    #     step_list = tree.findall('Steps/step')
    #     with open(result_dir+'/'+'myfile.log', 'w') as fp:
    #         pass
    #     wt_logsdir = os.path.join(result_dir, 'myfile.log')
    #     data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
    #     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None,\
    #     'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
    #     go_to_step_number = None
    #     system_name = 'NE1'
    #     parallel = False
    #     queue = False
    #     obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
    #      system_name, parallel, queue, skip_invoked=True)
    #     obj._skip_because_of_goto()

    def test_execute_step(self):

        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':Junit('testcase_step_exe'),\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        Utils.data_Utils.update_datarepository = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.update_count = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result = MagicMock()
        Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        common_execution_utils.compute_status = MagicMock(return_value=([True, True],\
         ['impact','impact']))
        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
            system_name, parallel, queue, skip_invoked=True)
        current_step_number = 1
        go_to_step_number = 1
        obj.execute_step(current_step_number, go_to_step_number)
        del Utils.data_Utils.update_datarepository
        del warrior.WarriorCore.Classes.junit_class.Junit.update_count
        del warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result
        del Utils.testcase_Utils.get_impact_from_xmlfile
        del common_execution_utils.compute_status

    def test_execute_steps_runmode(self):

        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':Junit('testcase_step_exe'),\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        Utils.data_Utils.update_datarepository = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.update_count = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result = MagicMock()
        Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=('RUP', True, '20'))


        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
            system_name, parallel, queue, skip_invoked=True)
        current_step_number = 1
        go_to_step_number = 1
        obj.execute_step(current_step_number, go_to_step_number)
        del Utils.data_Utils.update_datarepository
        del warrior.WarriorCore.Classes.junit_class.Junit.update_count
        del warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result
        del Utils.testcase_Utils.get_impact_from_xmlfile
        del common_execution_utils.get_runmode_from_xmlfile

    def test_execute_steps_retry_type(self):

        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':Junit('testcase_step_exe'),\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        Utils.data_Utils.update_datarepository = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.update_count = MagicMock()
        warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result = MagicMock()
        Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=(None, True, '20'))
        common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value=(True, '', '', '', ''))

        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
            system_name, parallel, queue, skip_invoked=True)
        current_step_number = 1
        go_to_step_number = 1
        obj.execute_step(current_step_number, go_to_step_number)
        del Utils.data_Utils.update_datarepository
        del warrior.WarriorCore.Classes.junit_class.Junit.update_count
        del warrior.WarriorCore.Classes.junit_class.Junit.add_keyword_result
        del Utils.testcase_Utils.get_impact_from_xmlfile
        del common_execution_utils.get_runmode_from_xmlfile
        del common_execution_utils.get_retry_from_xmlfile

    def test__execute_step_otherwise_ABORT(self):
        """
        This function will execute a step's onError functionality
        """
        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':Junit('testcase_step_exe'),\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
        onerror_driver.main = MagicMock(return_value='ABORT')
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        step_status = False
        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
            system_name, parallel, queue, skip_invoked=True)
        obj._execute_step_otherwise(step_status)
        del Utils.testcase_Utils.get_impact_from_xmlfile
        del onerror_driver.main

    def test__execute_step_otherwise_else_int(self):
        """
        This function will execute a step's onError functionality
        """
        from warrior.WarriorCore.testcase_steps_execution import TestCaseStepsExecutionClass
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
        step_list = tree.findall('Steps/step')
        with open(result_dir+'/'+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
        'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':Junit('testcase_step_exe'),\
        'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
        onerror_driver.main = MagicMock(return_value=2)
        warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
        common_execution_utils.compute_status = MagicMock(return_value=([True, True],\
         ['impact','impact']))
        input_dict = {"loop_iter_number":None}
        self.current_step_number = 3
        go_to_step_number = None
        system_name = 'NE1'
        parallel = False
        queue = False
        step_status = False
        obj = TestCaseStepsExecutionClass(step_list, data_repository, go_to_step_number,\
            system_name, parallel, queue, skip_invoked=True)
        obj._execute_step_otherwise(step_status)
        del onerror_driver.main
        del common_execution_utils.compute_status
        del warrior.Framework.Utils.data_Utils.update_datarepository

def test_execute_steps():
    """
    UT for execute_steps function
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_name':'testcase_step_exe', 'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'',\
      'wt_junit_object':None, 'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp,\
       'wt_resultsdir':result_dir}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = True
    step_num = None
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=(None, True, '20'))
    common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value=('if', '', '', '', ''))
    common_execution_utils.compute_status = MagicMock(return_value=([True, True],\
         ['impact','impact']))
    result = testcase_steps_execution.execute_steps(step_list, data_repository, system_name,\
     parallel, queue, skip_invoked=True, step_num=None)
    assert result == ([True, True], [None, None], ['impact', 'impact'])
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository
    del common_execution_utils.get_runmode_from_xmlfile
    del common_execution_utils.get_retry_from_xmlfile
    del Utils.testcase_Utils.get_impact_from_xmlfile
    del common_execution_utils.compute_status

def test_execute_steps_go_to_step_number():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None,\
     'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
    system_name = 'NE1'
    parallel = False
    queue = False
    skip_invoked = True
    step_num = None
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value=('if', '', '', '', ''))
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=(None, True, '20'))
    Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
    common_execution_utils.compute_status = MagicMock(return_value=([True],['impact']))

    result = testcase_steps_execution.execute_steps(step_list, data_repository, system_name,\
     parallel, queue, skip_invoked=True, step_num=None)
    # assert result == ([False, False], [[], []], ['impact', 'impact'])
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository
    del common_execution_utils.get_retry_from_xmlfile
    del common_execution_utils.get_runmode_from_xmlfile
    del Utils.testcase_Utils.get_impact_from_xmlfile
    del common_execution_utils.compute_status

def test_execute_steps_with_parallel_true():
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_step_exe.xml"))
    step_list = tree.findall('Steps/step')
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'myfile.log', 'w') as fp:
        pass
    wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
    data_repository = {'wt_filename':'testcase_step_exe.xml', 'wt_logsdir':wt_logsdir,\
     'wt_def_on_error_action':'NEXT', 'wt_def_on_error_value':'', 'wt_junit_object':None,\
     'wt_kw_results_dir':result_dir, 'wt_tc_timestamp':timestamp, 'wt_resultsdir':result_dir}
    system_name = 'NE1'
    parallel = True
    queue = False
    skip_invoked = True
    step_num = 0
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=(None, True, '20'))
    input_dict = {"loop_iter_number":None}
    Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value='impact')
    common_execution_utils.compute_status = MagicMock(return_value=([True],['impact']))
    common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value=('if', '', '', '', ''))
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    testcase_steps_execution.execute_steps(step_list, data_repository, system_name, parallel,\
     queue, skip_invoked=True, step_num=None)
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository
    del common_execution_utils.get_runmode_from_xmlfile
    del common_execution_utils.get_retry_from_xmlfile
    del Utils.testcase_Utils.get_impact_from_xmlfile
    del common_execution_utils.compute_status

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')
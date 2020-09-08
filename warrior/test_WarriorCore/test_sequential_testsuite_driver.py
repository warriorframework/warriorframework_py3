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
import unittest
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

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
sys.modules['warrior.WarriorCore.warrior_cli_driver'] = MagicMock(return_value=None)

from warrior.WarriorCore import testsuite_driver
from warrior.WarriorCore import onerror_driver

from warrior.WarriorCore import sequential_testsuite_driver

class test_sequential_testsuites(unittest.TestCase):
    '''UT for execute_step'''
    def setUp(self):
        '''setup function'''
        self.main = testsuite_driver.main
        self.main1 = onerror_driver.main
        testsuite_driver.main = MagicMock()
        onerror_driver.main = MagicMock()

    def tearDown(self):
        '''tearDown function'''
        testsuite_driver.main = self.main
        onerror_driver.main = self.main1

    def test_execute_sequential_testsuites(self):
        """ Executes suites in a project sequentially """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml"))
        # get root element
        root = tree.getroot()
        # getting steps
        step_list = root.findall("Testsuites/Testsuite")
        file_path = os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml")

        with open(result_dir+'/'+'pj_for_sts_driver.txt', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'pj_for_sts_driver.txt')
        testsuite_list = step_list
        testcasename = 'pj_for_sts_driver'
        wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit(
            testcasename, timestamp=timestamp, name='customProject_independant_testcase_execution',
            display=False)
        testsuite_driver.main = MagicMock(return_value=(True, {}))

        project_repository = {'title':'test', 'project_name':'pj_for_sts_driver',
        'project_execution_dir':wt_logsdir,'def_on_error_action':'next', 'def_on_error_value':'',
         'wp_results_execdir':result_dir, 'wp_logs_execdir':wt_logsdir,
         'project_filepath':file_path, 'project_title':'test'}

        data_repository = {'jiraproj':None, 'wt_ts_timestamp':timestamp,\
         'wt_junit_object':wt_junit_object}
        result = sequential_testsuite_driver.execute_sequential_testsuites(testsuite_list,
            project_repository, data_repository, auto_defects=False)

        assert result == True
        del testsuite_driver.main

    def test_execute_sequential_testsuites_skipped(self):
        """ Executes suites in a project sequentially """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver1.xml"))
        # get root element
        root = tree.getroot()
        # getting steps
        step_list = root.findall("Testsuites/Testsuite")
        file_path = os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver1.xml")

        with open(result_dir+'/'+'pj_for_sts_driver.txt', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'pj_for_sts_driver.txt')
        testsuite_list = step_list
        testcasename = 'pj_for_sts_driver'
        wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit(
            testcasename, timestamp=timestamp, name='customProject_independant_testcase_execution',
            display=False)
        testsuite_driver.main = MagicMock(return_value=(True, {}))
        onerror_driver.main = MagicMock(return_value=False)
        project_repository = {'title':'test', 'project_name':'pj_for_sts_driver',
        'project_execution_dir':wt_logsdir, 'def_on_error_action': 'next',\
        'def_on_error_value':'', 'wp_results_execdir':result_dir, 'wp_logs_execdir':wt_logsdir,\
         'project_filepath': file_path, 'project_title': 'test'}

        data_repository = {'jiraproj':None, 'wt_ts_timestamp':timestamp,\
         'wt_junit_object':wt_junit_object}
        result = sequential_testsuite_driver.execute_sequential_testsuites(testsuite_list,
            project_repository, data_repository, auto_defects=False)

        assert result == True
        del onerror_driver.main
        del testsuite_driver.main


    def test_main(self):
        """ Executes suites in a project sequentially """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml"))
        # get root element
        root = tree.getroot()
        # getting steps
        step_list = root.findall("Testsuites/Testsuite")
        file_path = os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml")

        with open(result_dir+'/'+'pj_for_sts_driver.txt', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'pj_for_sts_driver.txt')
        testsuite_list = step_list
        testcasename = 'pj_for_sts_driver'
        wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit(
            testcasename, timestamp=timestamp, name='customProject_independant_testcase_execution',
            display=False)
        testsuite_driver.main = MagicMock(return_value=(True, {}))
        project_repository = {'title':'test', 'project_name':'pj_for_sts_driver',
        'project_execution_dir':wt_logsdir, 'def_on_error_action':'next',
        'def_on_error_value':'', 'wp_results_execdir':result_dir,
        'wp_logs_execdir':wt_logsdir, 'project_filepath': file_path, 'project_title': 'test'}

        data_repository = {'jiraproj':None, 'wt_ts_timestamp':timestamp,\
         'wt_junit_object':wt_junit_object}
        result = sequential_testsuite_driver.main(testsuite_list, project_repository,
        data_repository, auto_defects=False)
        assert result == True
        del testsuite_driver.main

    def test_main_excepetion(self):
        """ Executes suites in a project sequentially """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml"))
        # get root element
        root = tree.getroot()
        # getting steps
        step_list = root.findall("Testsuites/Testsuite")
        testsuite_list = step_list[0]
        file_path = os.path.join(os.path.split(__file__)[0], "pj_for_sts_driver.xml")

        data_repository = {'jiraproj':None, 'wt_ts_timestamp':timestamp}
        project_repository = {}
        result = sequential_testsuite_driver.main(testsuite_list, project_repository,
        data_repository, auto_defects=False)

        assert result == False

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')
sys.modules.pop('warrior.WarriorCore.warrior_cli_driver')
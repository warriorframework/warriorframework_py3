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

import xml.etree.ElementTree as ET

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

sys.modules['warrior.WarriorCore.Classes.execution_summary_class'] = MagicMock(return_value=None)

from warrior.WarriorCore import parallel_testsuite_driver

def test_main_exception():
    """
    UT for main function
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_ptsd.xml"))
    testsuite_list = []
    project_repository = {}
    data_repository = {}
    result = parallel_testsuite_driver.main(testsuite_list, project_repository, data_repository,
         auto_defects=False, ts_parallel=True)
    assert result == False

def test_main_pass():
    """
    UT for main function
    """
    project_filepath = os.path.join(os.path.split(__file__)[0], "pj_for_ptsd.xml")
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_ptsd.xml"))
    suite_list = tree.findall('Testsuites/Testsuite')
    testsuite_list = suite_list
    project_repository = {'def_on_error_action':'next', 'project_filepath':project_filepath,\
     'wp_results_execdir':result_dir, 'wp_logs_execdir':result_dir, }
    data_repository = {'jiraproj':None, 'war_file_type': 'Project', 'wt_junit_object':None}

    result = parallel_testsuite_driver.main(testsuite_list, project_repository, data_repository,
         auto_defects=False, ts_parallel=True)
    assert result == True


def test_execute_parallel_testsuites():
    """
    UT for test_execute_parallel_testsuites
    """
    project_filepath = os.path.join(os.path.split(__file__)[0], "pj_for_ptsd.xml")
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "pj_for_ptsd.xml"))
    suite_list = tree.findall('Testsuites/Testsuite')
    testsuite_list = suite_list
    project_repository = {'def_on_error_action':'next', 'project_filepath':project_filepath,\
     'wp_results_execdir':result_dir, 'wp_logs_execdir':result_dir, }
    data_repository = {'jiraproj':None, 'war_file_type': 'Project', 'wt_junit_object':None}

    result = parallel_testsuite_driver.execute_parallel_testsuites(testsuite_list, \
    	project_repository, data_repository, auto_defects=False, ts_parallel=True)
    assert result == True

sys.modules.pop('warrior.WarriorCore.Classes.execution_summary_class')
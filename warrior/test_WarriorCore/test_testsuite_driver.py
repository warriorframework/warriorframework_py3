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
from unittest import TestCase
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore import testsuite_driver


def test_execute_testsuite():
    """Executes the testsuite (provided as a xml file)
            - Takes a testsuite xml file as input and
            sends each testcase to Basedriver for execution.
            - Computes the testsuite status based on the
            testcase_status and the impact value of the testcase
            - Handles testcase failures as per the default/specific onError action/value
            - Calls the function to report the testsuite status

    Arguments:
    1. testsuite_filepath   = (string) the full path of the testsuite xml file.
    2. Warrior          = (module loader) module loader object to call the Warrior
    3. execution_dir        = (string) the full path of the directory under which the testsuite
                              execution directory will be created (results for the testsuite will
                              be stored in the  testsuite execution directory.)
    """
    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver2.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}

    testsuite_driver.execute_testsuite(testsuite_filepath, data_repository, from_project=False,\
     auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None,\
      ts_onError_action=None, queue=None, ts_parallel=False)


def test_main():
    """Executes a test suite """

    testsuite_filepath = os.path.join(os.path.split(__file__)[0], "ts_for_ts_driver1.xml")
    data_repository = {'db_obj': False, 'war_file_type': 'Suite'}
    result1, result2 = testsuite_driver.main(testsuite_filepath, data_repository={},\
     from_project=False, auto_defects=False, jiraproj=None, res_startdir=None,\
      logs_startdir=None, ts_onError_action=None, queue=None, ts_parallel=False)
    assert result1 == False, result2 == dict
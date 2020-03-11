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

import sys
import os

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(WARRIORDIR)
    try:
        import warrior
    except:
        raise

from unittest.mock import MagicMock
sys.modules['warrior.Framework.Utils'] = MagicMock()
sys.modules['warrior.Framework.Utils.print_Utils'] = MagicMock()
sys.modules['warrior.WarriorCore.testcase_steps_execution'] = MagicMock()

from warrior.WarriorCore import testcase_steps_execution
from warrior.Framework import Utils
from warrior.WarriorCore import custom_sequential_kw_driver

def test_main1():
    """
    Test case for main
    Executes the list of keyword in sequential order
    Computes and returns the testcase status"""

    from warrior.WarriorCore.custom_sequential_kw_driver import main

    step_list = []
    data_repository = {}
    tc_status = False

    execute_custom_sequential = MagicMock(return_value=True)
    main(step_list, data_repository, tc_status, system_name=None)

def test_main2():
    """
    Test case for main
    Executes the list of keyword in sequential order
    Computes and returns the testcase status"""

    from warrior.WarriorCore.custom_sequential_kw_driver import main

    step_list = ''
    data_repository = {}
    tc_status = False
    execute_custom_sequential = MagicMock(return_value=True)

    main(step_list, data_repository, tc_status, system_name=None)


def test_execute_custom_sequential():
    """
    Test case for execute_custom_sequential function
    Takes a list of steps as input and executes
    them sequentially by sending then to the
    testcase_steps_execution driver Executes all the steps in custom sequential fashion """
    from warrior.WarriorCore.custom_sequential_kw_driver import execute_custom_sequential

    step_list = ''
    data_repository = {'wt_resultfile':''}
    tc_status = False
    system_name = None

    testcase_steps_execution.main = MagicMock(return_value=(['s', 'd'], ['z', 'x'], ['q', 'w']))
    Utils.testcase_Utils.compute_status_using_impact = MagicMock(return_value='True')
    Utils.testcase_Utils.append_result_files = MagicMock(return_value=None)

    execute_custom_sequential(step_list, data_repository, tc_status, system_name)

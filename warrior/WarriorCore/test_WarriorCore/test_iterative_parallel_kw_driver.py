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
    # import pdb
    # pdb.set_trace()
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

from unittest.mock import MagicMock

# from warrior.WarriorCore import iterative_parallel_kw_driver


sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
from warrior.WarriorCore import iterative_parallel_kw_driver

warrior.WarriorCore.testcase_steps_execution = MagicMock(return_value=None)
warrior.Framework.Utils.print_Utils = MagicMock(return_value=None)
warrior.WarriorCore.multiprocessing_utils = MagicMock(return_value=None)
warrior.Framework.Utils.testcase_Utils = MagicMock(return_value=None)

import warrior.WarriorCore.testcase_steps_execution as testcase_steps_execution

def test_execute_iterative_parallel():

    class get(object):
        """get method"""

        def __init__(self):
            """init method"""
            pass

        def get(self, args):
            """get method"""
            return "tc_timestamp"

    class jUnit(object):
        """Junit method"""

        def __init__(self):
            """init method"""
            pass

        class root(object):
            """root method"""

            def iter(self):
                """iter method"""
                objlist = []
                objlist.append(get())
                return objlist

    step_list = ['a', 'b']
    system_list = ['one', 'two']
    obj = jUnit()
    data_repository = {'wt_junit_object': obj, 'tc_junit_list': [], \
                       'wt_resultfile': '', 'wt_tc_timestamp': ''}
    tc_status = False
    testcase_steps_execution.main = MagicMock(return_value=(['s', 'd'], ['z', 'x'], ['q', 'w']))

    warrior.WarriorCore.multiprocessing_utils.create_and_start_process_with_queue = MagicMock(return_value=('val', [1,2], 'val'))
    warrior.WarriorCore.multiprocessing_utils.get_results_from_queue = MagicMock(return_value=['a', 'b'])
    warrior.Framework.Utils.testcase_Utils.compute_status_using_impact = MagicMock(return_value='True')
    warrior.Framework.Utils.testcase_Utils.compute_system_resultfile = MagicMock(return_value='file')
    warrior.Framework.Utils.testcase_Utils.compute_status_without_impact = MagicMock(return_value=True)
    warrior.WarriorCore.multiprocessing_utils.update_tc_junit_resultfile = MagicMock(return_value='None')

    warrior.Framework.Utils.testcase_Utils.append_result_files = MagicMock(return_value=None)

    iterative_parallel_kw_driver.execute_iterative_parallel(step_list, data_repository, tc_status, system_list)

def test_main1():
    """
    Test case for main
    Executes the list of keyword in sequential order
    Computes and returns the testcase status"""
    import warrior
    step_list = []
    data_repository = {}
    tc_status = False
    system_list = []

    execute_custom_sequential = MagicMock(return_value=True)
    iterative_parallel_kw_driver.main(step_list, data_repository, tc_status, system_list)

def test_main2():
    """
    Test case for main
    Executes the list of keyword in sequential order
    Computes and returns the testcase status"""

    step_list = ''
    data_repository = {}
    tc_status = False
    system_list = []
    execute_custom_sequential = MagicMock(return_value=True)

    iterative_parallel_kw_driver.main(step_list, data_repository, tc_status, system_list)
    iterative_parallel_kw_driver.main(step_list, data_repository, tc_status, system_list)

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

import os
import sys
from unittest.mock import MagicMock

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

try:
    from warrior.WarriorCore import custom_parallel_kw_driver, step_driver

# except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
    sys.path.append(WARRIORDIR)
    try:
        from warrior.WarriorCore import custom_parallel_kw_driver
    except:
        raise

import warrior
from warrior.WarriorCore import step_driver
from warrior.Framework import Utils
from warrior.Framework.Utils import testcase_Utils

warrior.WarriorCore.step_driver = MagicMock(return_value=None)
warrior.WarriorCore.Classes.argument_datatype_class = MagicMock(return_value=None)
warrior.WarriorCore.multiprocessing_utils = MagicMock(return_value=None)


def test_main1():
    """
    Test case for main
    Executes the list of keyword in parallel order
    Computes and returns the testcase status"""
    from warrior.WarriorCore.custom_parallel_kw_driver import main
    step_list = []
    data_repository = {}
    tc_status = True
    # custom_parallel_kw_driver = MagicMock(return_value=True)
    main(step_list, data_repository, tc_status, system_name=None)


def test_main2():
    """
    Test case for main
    Executes the list of keyword in parallel order
    Computes and returns the testcase status"""
    from warrior.WarriorCore.custom_parallel_kw_driver import main
    step_list = ''
    data_repository = {}
    tc_status = False
    main(step_list, data_repository, tc_status, system_name=None)


def test_execute_custom_sequential():
    """
    Test case for execute_custom_sequential function
    Takes a list of steps as input and executes
    them sequentially by sending then to the
    testcase_steps_execution driver Executes all the steps in custom sequential fashion """
    from warrior.WarriorCore.custom_parallel_kw_driver import execute_custom_parallel
    from warrior.WarriorCore import multiprocessing_utils

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
    obj = jUnit()
    data_repository = {'wt_junit_object': obj, 'tc_junit_list': [], \
                       'wt_resultfile': '', 'wt_tc_timestamp': ''}
    tc_status = False
    system_name = None
    step_driver.main = MagicMock(return_value=(['s', 'd'], ['z', 'x'], ['q', 'w']))
    multiprocessing_utils.create_and_start_process_with_queue = MagicMock(return_value=('', [], ''))
    multiprocessing_utils.get_results_from_queue = MagicMock(return_value=['a', 'b'])
    Utils.testcase_Utils.compute_status_using_impact = MagicMock(return_value='True')
    multiprocessing_utils.update_tc_junit_resultfile = MagicMock(return_value='')
    Utils.testcase_Utils.append_result_files = MagicMock(return_value=None)
    execute_custom_parallel(step_list, data_repository, tc_status, system_name)

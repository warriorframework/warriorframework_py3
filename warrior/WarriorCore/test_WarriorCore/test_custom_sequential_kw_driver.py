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

sys.modules['warrior.WarriorCore.common_execution_utils'] = MagicMock()
sys.modules['warrior.WarriorCore.onerror_driver'] = MagicMock()
sys.modules['warrior.WarriorCore.exec_type_driver'] = MagicMock()
sys.modules['warrior.WarriorCore.step_driver'] = MagicMock()
sys.modules['warrior.WarriorCore.testcase_steps_execution'] = MagicMock()
sys.modules['warrior.Framework.Utils.datetime_utils'] = MagicMock()

from warrior.WarriorCore import custom_sequential_kw_driver

warrior.WarriorCore.testcase_steps_execution = MagicMock(return_value=None)
warrior.Framework.Utils = MagicMock(return_value=None)
warrior.Framework.Utils.print_Utils = MagicMock(return_value=None)


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

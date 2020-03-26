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

from warrior.WarriorCore import iterative_sequential_kw_driver

warrior.WarriorCore.testcase_steps_execution = MagicMock(return_value=None)
warrior.Framework.Utils = MagicMock(return_value=None)
warrior.Framework.Utils.print_Utils = MagicMock(return_value=None)

# import traceback
from warrior.WarriorCore import testcase_steps_execution
# from warrior.Framework import Utils
# from warrior.Framework.Utils.print_Utils import print_debug, print_error
def test_main1():
    """
    Test case for main
    Executes the list of keyword in sequential order
    Computes and returns the testcase status"""

    step_list = []
    data_repository = {}
    tc_status = False
    system_list = []
    execute_custom_sequential = MagicMock(return_value=True)
    iterative_sequential_kw_driver.main(step_list, data_repository, tc_status, system_list)

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

    iterative_sequential_kw_driver.main(step_list, data_repository, tc_status, system_list)


# def test_compute_system_resultfile():
#     """Takes a list of steps as input and executes them in sequential
#     order by sending them to testcase steps execution driver """
#     import pdb
#     pdb.set_trace()

#     kw_resultfile_list = []
#     resultsdir = ''
#     system_name = 'sys name'

#     warrior.Framework.Utils.file_Utils.createDir = MagicMock(return_value="some dir")
#     warrior.Framework.Utils.file_Utils.getCustomLogFile = MagicMock(return_value='some dir')
#     warrior.Framework.Utils.testcase_Utils.append_result_files = MagicMock(return_value=None)

#     # system_results_dir = Utils.file_Utils.createDir(resultsdir,
#     # #                                                 'System_Results')
#     # system_resultfile = Utils.file_Utils.getCustomLogFile('system', system_results_dir,
#     #                                                       system_name, '.xml')
#     # Utils.testcase_Utils.append_result_files(system_resultfile,
#     #                                          kw_resultfile_list, dst_root='System')
#     # return system_resultfile
#     iterative_sequential_kw_driver.compute_system_resultfile(kw_resultfile_list, resultsdir, system_name)

# def test_execute_iterative_sequential():
#     """ Executes all the steps in iterative sequential fashion """



#     step_list = []
#     data_repository = {}
#     tc_status = False
#     system_list = ['a', 'b']

#     warrior.WarriorCore.testcase_steps_execution.main = MagicMock(return_value=([], [], []))
#     warrior.Framework.Utils.testcase_Utils.compute_status_using_impact = MagicMock(return_value=True)

#     iterative_sequential_kw_driver.compute_system_resultfile = MagicMock(return_value="some file")
#     warrior.Framework.Utils.testcase_Utils.compute_status_without_impact = MagicMock(True)
#     warrior.Framework.Utils.testcase_Utils.append_result_files = MagicMock(return_value=None)

#     iterative_sequential_kw_driver.execute_iterative_sequential(step_list, data_repository, tc_status, system_list)

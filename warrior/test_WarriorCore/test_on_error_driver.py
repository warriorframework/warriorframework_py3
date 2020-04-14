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
from unittest.mock import MagicMock
from os.path import abspath, dirname
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

# sys.modules['warrior.WarriorCore.Classes.war_cli_class'] = MagicMock()

from warrior.WarriorCore import onerror_driver
#
# warrior.Framework.Utils = MagicMock()
# warrior.Framework.Utils.print_Utils = MagicMock()
#


def test_execute_and_resume():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """

    action = 'EXECUTE_AND_RESUME'
    value = [2,3]
    error_handle = {}
    status = onerror_driver.execute_and_resume(action, value, error_handle)
    assert status["action"]  == "EXECUTE_AND_RESUME"


def test_abortAsError():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """
    action = 'abortaserror'
    value = 1
    error_handle = {}
    status = onerror_driver.abortAsError(action, value, error_handle)
    assert status["action"] ==  "ABORT_AS_ERROR"

def test_abort():
    """returns ABORT for on_error action = abort """
    action = 'abort'
    value = 1
    error_handle = {}

    status = onerror_driver.abort(action, value, error_handle)
    assert status["action"] == "ABORT"

def test_goto():
    """returns goto_step_num for on_error action = goto """
    action = 'GOTO'
    value = 3
    error_handle = {}

    status = onerror_driver.goto(action, value, error_handle)
    assert status["action"] == "GOTO"
    assert status["value"] == 3



def test_next():
    """returns 'NEXT' for on_error action = next """
    action = 'next'
    value = 2
    error_handle = {}

    status = onerror_driver.next(action, value, error_handle, skip_invoked=True)
    assert status["action"] == "NEXT"

# def test_get_failure_results1():
#     """ Returns the appropriate values based on the onError actions for failing steps.
#
#     Arguments:
#     1. error_repository    = (dict) dictionary containing the onError action, values
#     """
#
#     error_repository = {'action':'NEXT'}
#
#     onerror_driver.get_failure_results(error_repository)
#
# def test_get_failure_results2():
#     """ Returns the appropriate values based on the onError actions for failing steps.
#
#     Arguments:
#     1. error_repository    = (dict) dictionary containing the onError action, values
#     """
#
#     error_repository = {'action':'GOTO', 'value':1}
#
#     onerror_driver.get_failure_results(error_repository)
#
# def test_get_failure_results3():
#     """ Returns the appropriate values based on the onError actions for failing steps.
#
#     Arguments:
#     1. error_repository    = (dict) dictionary containing the onError action, values
#     """
#
#     error_repository = {'action':'ABORT'}
#
#     onerror_driver.get_failure_results(error_repository)
#
#
# def test_getErrorHandlingParameters():
#     """Takes a xml element at input and returns the values for on_error action , value
#     If no value is available in the node then returns the default values """
#
#     def_on_error_action = ''
#     def_on_error_value = ''
#     exec_type = 'yes'
#
#     class node(object):
#         """docstring for node"""
#         def __init__(self, arg):
#             super(node, self).__init__()
#             self.arg = arg
#
#         def find(self):
#             attrib = 'some value'
#             # return 'yes'
#     class exec_node(object):
#         """docstring for node"""
#         def __init__(self, arg):
#             super(node, self).__init__()
#             self.arg = arg
#
#         def find(self):
#             attrib = 'some value'
# # if exec_type:
# #     def_on_error_action = 'NEXT'
# #     def_on_error_value = ''
# #     ex_rule_param = exec_node.find('Rule').attrib
# #     action = ex_rule_param['Else']
# #     if ex_rule_param['Else'].upper() == 'GOTO':
# #         value = ex_rule_param['Elsevalue']
#
#     onerror_driver.getErrorHandlingParameters(node, def_on_error_action, def_on_error_value,\
#         exec_type, current_step_number=None)
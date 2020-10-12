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
import xml.etree.ElementTree as ET
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

from warrior.WarriorCore import onerror_driver

def test_execute_and_resume():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """
    action = 'EXECUTE_AND_RESUME'
    value = [2, 3]
    error_handle = {}
    status = onerror_driver.execute_and_resume(action, value, error_handle)
    assert status["action"] == "EXECUTE_AND_RESUME"

def test_abortAsError():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """
    action = 'abortaserror'
    value = 1
    error_handle = {}
    status = onerror_driver.abortAsError(action, value, error_handle)
    assert status["action"] == "ABORT_AS_ERROR"

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

def test_main():
    """Takes a xml element (steps/step codntion / testcase/ tesuite)
    as input and return the action to be performed for failure
    conditions """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "onerror_suite1.xml"))
    # get root element
    root = tree.getroot()
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    node = testcase_list[0]
    def_on_error_action = 'next'
    def_on_error_value = ''
    result = onerror_driver.main(node, def_on_error_action, def_on_error_value, exec_type=False,\
     skip_invoked=True, current_step_number=None)
    assert result == False

def test_get_failure_results_next():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': 'NEXT'}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == False
    assert test1 == True

def test_get_failure_results_goto():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': 'GOTO', 'value':1}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == 1
    assert test1 == True

def test_get_failure_results_abort():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': 'ABORT'}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == 'ABORT'
    assert test1 == True

def test_get_failure_results_execute_and_resume():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': 'EXECUTE_AND_RESUME', 'value':1}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == 1
    assert test1 == True

def test_get_failure_results_abort_as_error():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': 'ABORT_AS_ERROR'}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == 'ABORT_AS_ERROR'
    assert test1 == True

def test_get_failure_results_none():
    """ Returns the appropriate values based on the onError actions for failing steps.
    """
    error_repository = {'action': ''}
    result = onerror_driver.get_failure_results(error_repository)
    test1 = 'action' in error_repository
    assert result == False
    assert test1 == True

def test_getErrorHandlingParameters():
    """Takes a xml element at input and returns the values for on_error action , value
    If no value is available in the node then returns the default values """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "onerror_suite2.xml"))
    # get root element
    root = tree.getroot()
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    node = testcase_list[0]
    def_on_error_action = 'next'
    def_on_error_value = ''
    exec_type = 'sequential_testcases'
    result = onerror_driver.getErrorHandlingParameters(node, def_on_error_action,\
        def_on_error_value, exec_type, current_step_number=None)
    assert result == ('next', '')
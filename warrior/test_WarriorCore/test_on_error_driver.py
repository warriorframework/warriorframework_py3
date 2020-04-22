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
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore import onerror_driver

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


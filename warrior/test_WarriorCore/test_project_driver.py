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

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
sys.modules['warrior.WarriorCore.warrior_cli_driver'] = MagicMock(return_value=None)

from warrior.WarriorCore.testcase_steps_execution import main
from warrior.WarriorCore import exec_type_driver
import warrior.WarriorCore.testsuite_driver as testsuite_driver
import warrior.WarriorCore.onerror_driver as onerror_driver
from warrior.WarriorCore import testcase_steps_execution
from warrior.WarriorCore import testcase_driver
from warrior.Framework import Utils
from warrior.WarriorCore import common_execution_utils
from warrior.WarriorCore import testsuite_driver
from warrior.WarriorCore import testsuite_utils

from warrior.WarriorCore import project_driver 

def test_compute_project_status_impact_True():
    """Computes the status of the project based on the value of impact for the testsuite
    """
    project_status = True
    testsuite_status = True
    testsuite_impact = 'impact'
    result = project_driver.compute_project_status(project_status, testsuite_status, testsuite_impact)
    assert result == True

def test_compute_project_status_impact_False():
    """Computes the status of the project based on the value of impact for the testsuite
    """
    project_status = True
    testsuite_status = False
    testsuite_impact = 'impact'
    result = project_driver.compute_project_status(project_status, testsuite_status, testsuite_impact)
    assert result == False

def test_compute_project_status_noimpact_True():
    """Computes the status of the project based on the value of impact for the testsuite
    """
    project_status = True
    testsuite_status = True
    testsuite_impact = 'noimpact'
    result = project_driver.compute_project_status(project_status, testsuite_status, testsuite_impact)
    assert result == True

def test_compute_project_status_noimpact_False():
    """Computes the status of the project based on the value of impact for the testsuite
    """
    project_status = True
    testsuite_status = False
    testsuite_impact = 'noimpact'
    result = project_driver.compute_project_status(project_status, testsuite_status, testsuite_impact)
    assert result == True

def test_main_exeception():
    """ Project driver"""
    data_repository = {'db_obj': False, 'war_file_type': 'Project'}
    project_filepath = os.path.join(dirname(abspath(__file__)), 'pj_for_pj_file.xml')
    project_status, project_repository = project_driver.main(project_filepath,
     data_repository, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None)
    assert project_status == False
    assert project_repository == None

def test_main_pass():
    """ Project driver"""
    data_repository = {'db_obj': False, 'war_file_type': 'Project'}
    project_filepath = os.path.join(dirname(abspath(__file__)), 'pj_for_pj_file.xml')
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    with open(result_dir+'/'+'project_log.txt', 'w'):
        pass
    wt_logsdir = os.path.join(result_dir, 'project_log.txt')
    res_startdir = wt_logsdir
    logs_startdir = wt_logsdir
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    project_status, project_repository = project_driver.main(project_filepath,
     data_repository, auto_defects=False, jiraproj=None, res_startdir=None, logs_startdir=None)
    check1 = project_repository['project_name'] == 'pj_for_pj_file'
    check2 = project_repository['project_title'] == 'test'
    assert project_status == True
    assert check1 == True
    assert check2 == True
    del mock_tools
    del testcase_steps_execution.main

def test_execute_project():
    """
    test_execute_project
    """
    data_repository = {'db_obj': False, 'war_file_type': 'Project'}
    project_filepath = os.path.join(dirname(abspath(__file__)), 'pj_for_pj_file.xml')
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    with open(result_dir+'/'+'project_log.txt', 'w'):
        pass
    wt_logsdir = os.path.join(result_dir, 'project_log.txt')
    res_startdir = wt_logsdir
    logs_startdir = wt_logsdir
    auto_defects=False
    jiraproj=None
    res_startdir=None
    logs_startdir=None
    testcase_steps_execution.main = MagicMock(return_value=([True], [], ['impact']))
    project_status, project_repository = project_driver.execute_project(project_filepath,
     auto_defects, jiraproj, res_startdir, logs_startdir, data_repository)
    check1 = project_repository['project_name'] == 'pj_for_pj_file'
    check2 = project_repository['project_title'] == 'test'
    assert project_status == True
    assert check1 == True
    assert check2 == True
    del mock_tools
    del testcase_steps_execution.main

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class')
sys.modules.pop('warrior.WarriorCore.warrior_cli_driver')
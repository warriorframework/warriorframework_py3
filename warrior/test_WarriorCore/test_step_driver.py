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
import datetime
from pathlib import Path
try:
    import warrior
except ModuleNotFoundError:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior
try:
    from warrior.WarriorCore import step_driver
except ImportError:
    from warrior.WarriorCore import step_driver
import xml.etree.ElementTree as ET
from warrior.WarriorCore import step_driver
from warrior.WarriorCore.Classes.junit_class import Junit
from warrior.Framework import Utils
obj = step_driver.ArgumentDatatype(None, None)
sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=obj)

def test_main():
    """Get a step, executes it and returns the result """
    cwd = os.getcwd()
    tree = ET.parse(
        os.path.join(
            os.path.split(__file__)[0],
            "step_driver_testcase.xml"
            )
        )
    step_list = tree.findall('Steps/step')
    step_num = 0
    for stp in step_list:
        step = stp
        step_num = step_num + 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        wt_resultsdir = cwd
        wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit
        data_repository = {
            'wt_junit_object':wt_junit_object,
            'wt_filename':'step_driver_testcase.xml',
            'wt_logsdir':cwd,
            'wt_kw_results_dir':cwd,
            'wt_def_on_error_action':'NEXT',
            'wt_tc_timestamp':timestamp,
            'wt_resultsdir':wt_resultsdir,
            'wt_name':'step_driver_testcase',
            'war_parallel':True,
            'war_file_type':'Case',
            'wt_step_type':'step'
            }
        system_name = None
        kw_parallel = True

    result = step_driver.main(
        step,
        step_num,
        data_repository,
        system_name,
        kw_parallel,
        queue=None,
        skip_invoked=True
        )
    assert result == (False, [], 'impact', False)

def test_get_arguments():
    '''testcase for get_arguments'''
    root = ET.parse(
        os.path.join(os.path.split(__file__)[0], "step_driver_testcase.xml")).getroot()
    steps = root.find('Steps')
    step = steps.find('step')
    return_val = step_driver.get_arguments(step)
    assert type(return_val) == dict

def test_send_keyword_to_productdriver1():
    '''testcase for send_keyword_to_productdriver'''
    from warrior.WarriorCore.Classes.testcase_utils_class import TestcaseUtils
    TestcaseUtils.p_step = MagicMock()
    driver_name = 'common_driver'
    plugin_name = None
    keyword = 'wait_for_timeout'
    data_repository = {}
    data_repository['step_num'] = 1
    args_repository = {'timeout': '1', 'notify_count': '1'}
    repo_name = 'warrior'
    result = step_driver.send_keyword_to_productdriver(
        driver_name, plugin_name, keyword,
        data_repository, args_repository, repo_name)
    assert result == {'step_num': 1, 'step-1_status': True}
    del TestcaseUtils.p_step

def test_send_keyword_to_productdriver2():
    '''testcase for send_keyword_to_productdriver'''
    from warrior.WarriorCore.Classes.testcase_utils_class import TestcaseUtils
    TestcaseUtils.p_step = MagicMock()
    driver_name = 'common_driver'
    plugin_name = None
    keyword = 'wait_for_timeout'
    data_repository = {}
    data_repository['step_num'] = 1
    args_repository = {'timeout': '1', 'notify_count': '1'}
    repo_name = 'warrisor'
    result = step_driver.send_keyword_to_productdriver(
        driver_name, plugin_name, keyword,
        data_repository, args_repository, repo_name)
    assert result['step_num'] == 1
    assert result['step-1_status'] == 'ERROR'
    del TestcaseUtils.p_step

def test_get_keyword_resultfile():
    ''''testcase for get_keyword_resultfile'''
    data_repository = {}
    homepath = str(Path.home())
    testcasename = "step_driver_testcase.xml"
    data_repository['wt_kw_results_dir'] = homepath +\
        '/Warriorspace/Execution/'+ testcasename +\
        '/Results/Keyword_Results'
    system_name = None
    step_num = 1
    keyword = 'wait_for_timeout'
    result = step_driver.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
    assert result == homepath +'/Warriorspace/Execution/'+\
        testcasename +'/Results/Keyword_Results/step-1_'+\
        keyword + '.xml'

def test_execute_step():
    '''test case for execute_step'''
    homepath = str(Path.home())
    testcasename = "step_driver_testcase"
    timestr = str(datetime.datetime.now())
    #keyword = 'wait_for_timeout'
    step_driver.add_keyword_result = MagicMock()
    wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit(
        testcasename,
        timestamp='2020-04-29 17:05:11',
        name='customProject_independant_testcase_execution',
        display=False)
    root = ET.parse(os.path.join(os.path.split(__file__)[0], "step_driver_testcase.xml")).getroot()
    steps = root.find('Steps')
    step = steps.find('step')
    system_name = None
    step_num = 1
    kw_parallel = False
    queue = None
    data_repository = {}
    data_repository['wt_junit_object'] = wt_junit_object
    data_repository['wt_kw_results_dir'] = homepath +\
        '/Warriorspace/Execution/'+ testcasename +\
        '/Results/Keyword_Results'
    data_repository['wt_def_on_error_action'] = 'NEXT'
    data_repository['wt_tc_timestamp'] = timestr
    data_repository['wt_resultsdir'] = homepath +\
        '/Warriorspace/Execution/'+ testcasename +\
        "/Results"
    data_repository['wt_name'] = testcasename
    data_repository['wt_step_type'] = "step"
    data_repository['war_parallel'] = False
    result = step_driver.execute_step(
        step, step_num, data_repository,
        system_name, kw_parallel, queue)
    assert result[0] == True
    assert result[2] == 'impact'
    del step_driver.add_keyword_result

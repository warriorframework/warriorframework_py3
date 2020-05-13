# """
# Copyright 2017, Fujitsu Network Communications, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# """

# import sys
# import os
# from unittest.mock import MagicMock
# from os.path import abspath, dirname
# import datetime
# from pathlib import Path
# try:
#     import warrior
# except ModuleNotFoundError:
#     WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
#     sys.path.append(WARRIORDIR)
#     import warrior
# try:
#     from warrior.WarriorCore import step_driver
# except ImportError:
#     from warrior.WarriorCore import step_driver
# import xml.etree.ElementTree as ET
# from warrior.WarriorCore import step_driver
# from warrior.WarriorCore.Classes.junit_class import Junit
# from warrior.Framework import Utils

# import unittest
# from warrior.WarriorCore.Classes import testcase_utils_class

# temp_cwd = os.path.split(__file__)[0]
# path = os.path.join(temp_cwd, 'UT_results')

# try:
#     os.makedirs(path, exist_ok=True)
#     result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
# except OSError as error:
#     pass

# class test_execute_step(unittest.TestCase):

#     def setUp(self):
#         self.add_keyword_result = Junit.add_keyword_result
#         self.update_count = Junit.update_count
#         Junit.add_keyword_result = MagicMock(return_val= None)
#         Junit.update_count = MagicMock(return_val= None)
        

#     def tearDown(self):
#         Junit.add_keyword_result = self.add_keyword_result

#     def test_execute_step(self):
#         """Get a step, executes it and returns the result """
#         tree = ET.parse(
#             os.path.join(
#                 os.path.split(__file__)[0],
#                 "step_driver_testcase.xml"
#                 )
#             )
#         root = tree.getroot()
#         steps = root.find('Steps')
#         step = steps.find('step')
#         step_num = 1
#         testcasename = "step_driver_testcase"
#         homepath = str(Path.home())
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#         wt_junit_object = warrior.WarriorCore.Classes.junit_class.Junit(
#         testcasename,
#         timestamp = timestamp,
#         name = 'customProject_independant_testcase_execution',
#         display = False)
#         # wt_resultsdir = 
#         system_name = None
#         kw_parallel = False
#         data_repository = {
#                 'wt_junit_object':wt_junit_object,
#                 'wt_filename':'step_driver_testcase.xml',
#                 'wt_logsdir':result_dir,
#                 'wt_kw_results_dir':result_dir,
#                 'wt_def_on_error_action':'NEXT',
#                 'wt_tc_timestamp':timestamp,
#                 'wt_resultsdir':result_dir,
#                 'wt_name':'step_driver_testcase',
#                 'war_parallel':True,
#                 'war_file_type':'Case',
#                 'wt_step_type':'step'
#                 }

#         keyword = 'wait_for_timeout'
#         result = step_driver.execute_step(
#             step,
#             step_num,
#             data_repository,
#             system_name,
#             kw_parallel,
#             queue=None,
#             skip_invoked=True
#             )
#         assert result[0]== True
#         assert result[2]== 'impact'

# def test_get_arguments():
#     root = ET.parse(os.path.dirname(os.path.abspath(__file__)\
#         )+"/step_driver_testcase.xml").getroot()
#     steps = root.find('Steps')
#     step = steps.find('step')
#     return_val = step_driver.get_arguments(step)
#     assert return_val == {'timeout': '1', 'notify_count': '1'}

# def test_send_keyword_to_productdriver1():
#     from warrior.WarriorCore.Classes.testcase_utils_class import TestcaseUtils
#     TestcaseUtils.p_step = MagicMock()
#     driver_name = 'common_driver'
#     plugin_name = None
#     keyword = 'wait_for_timeout'
#     data_repository = {}
#     data_repository['step_num'] = 1
#     args_repository = {'timeout': '1', 'notify_count': '1'}
#     repo_name = 'warrior'
#     result = step_driver.send_keyword_to_productdriver(
#         driver_name, plugin_name, keyword,
#         data_repository, args_repository, repo_name)
#     assert result['step_num'] == 1
#     assert result['step-1_status'] == True

# def test_send_keyword_to_productdriver2():
#     from warrior.WarriorCore.Classes.testcase_utils_class import TestcaseUtils
#     TestcaseUtils.p_step = MagicMock()
#     warriorpath = "/".join((os.path.abspath(__file__).split('/')[:-2]))
#     driver_name = 'common_driver'
#     plugin_name = None
#     keyword = 'wait_for_timeout'
#     data_repository = {}
#     data_repository['step_num'] = 1
#     args_repository = {'timeout': '1', 'notify_count': '1'}
#     repo_name = 'warrisor'
#     result = step_driver.send_keyword_to_productdriver(
#         driver_name, plugin_name, keyword,
#         data_repository, args_repository, repo_name)
#     assert result['step_num'] == 1
#     assert result['step-1_status'] == 'ERROR'
#     check1 = warriorpath in result['step-1_exception']
#     check2 = "/WarriorCore/step_driver.py" in result['step-1_exception']
#     check3 = "driver_call = __import__(import_name, fromlist=[driver_name])" in result['step-1_exception']
#     check4 = "ModuleNotFoundError" in result['step-1_exception']
#     assert check1 == True
#     assert check2 == True
#     assert check3 == True
#     assert check4 == True

# def test_get_keyword_resultfile():
#     data_repository = {}
#     homepath = result_dir
#     testcasename = "step_driver_testcase.xml"
#     data_repository['wt_kw_results_dir'] = result_dir
#     system_name = None
#     step_num = 1
#     keyword = 'wait_for_timeout'
#     result = step_er.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
#     import pdb
#     pdb.set_trace()
#     check1 = homepath in result
#     check2 = '/Warriorspace/Execution/' in result
#     check3 = testcasename in result
#     check4 = '/Results/Keyword_Results/step-1_' in result
#     check5 = keyword in result
#     check6 = result.endswith('.xml')
#     assert check1 == True
#     # assert check2 == True
#     # assert check3 == True
#     # assert check4 == True
#     # assert check5 == True
#     # assert check6 == True
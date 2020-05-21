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
from os.path import abspath, dirname
from unittest import TestCase
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    print(WARRIORDIR)
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore.defects_driver import DefectsDriver

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass

class test_DefectsDriver(TestCase):
    """ Defects Driver Class """

    def test_get_defect_json_list(self):
        """Gets the list of defect json files for the testcase execution """
        wt_resultfile = os.path.join(os.path.split(__file__)[0], "defects_driver_results_tc.xml")
        wt_defectsdir = result_dir
        with open(result_dir+'/'+'myfile.log', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        wt_testcase_filepath = os.path.join(os.path.split(__file__)[0], "defects_driver_tc.xml")
        data_repository = {'wt_resultfile':wt_resultfile, 'wt_defectsdir':wt_defectsdir, \
        'wt_logsdir':wt_logsdir, 'wt_testcase_filepath': wt_testcase_filepath, 'jiraproj':None}
        cls_obj = DefectsDriver(data_repository)
        result = cls_obj.get_defect_json_list()
        assert type(result) == list

    def test_create_failing_kw_json_without_keywords(self):
        """Create a json file each failing keyword """

        wt_resultfile = os.path.join(os.path.split(__file__)[0], "defects_driver_results_tc1.xml")
        wt_defectsdir = result_dir
        with open(result_dir+'/'+'myfile.log', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        wt_testcase_filepath = os.path.join(os.path.split(__file__)[0], "defects_driver_tc1.xml")
        data_repository = {'wt_resultfile':wt_resultfile, 'wt_defectsdir':wt_defectsdir, \
        'wt_logsdir':wt_logsdir, 'wt_testcase_filepath': wt_testcase_filepath, 'jiraproj':None}
        cls_obj = DefectsDriver(data_repository)
        result = cls_obj.create_failing_kw_json()
        assert result == None

    def test_create_failing_kw_json_no_failed_keywords(self):
        """Create a json file each failing keyword """
        wt_resultfile = os.path.join(os.path.split(__file__)[0], "defects_driver_results_tc2.xml")
        wt_defectsdir = result_dir
        with open(result_dir+'/'+'myfile.log', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        wt_testcase_filepath = os.path.join(os.path.split(__file__)[0], "defects_driver_tc2.xml")
        data_repository = {'wt_resultfile':wt_resultfile, 'wt_defectsdir':wt_defectsdir, \
        'wt_logsdir':wt_logsdir, 'wt_testcase_filepath': wt_testcase_filepath, 'jiraproj':None}
        cls_obj = DefectsDriver(data_repository)
        result = cls_obj.create_failing_kw_json()
        assert result == False

    def test_create_failing_kw_json(self):
        """Create a json file each failing keyword """

        wt_resultfile = os.path.join(os.path.split(__file__)[0], "defects_driver_results_tc.xml")
        wt_defectsdir = result_dir
        with open(result_dir+'/'+'myfile.log', 'w'):
            pass
        wt_logsdir = os.path.join(result_dir, 'myfile.log')
        wt_testcase_filepath = os.path.join(os.path.split(__file__)[0], "defects_driver_tc.xml")
        data_repository = {'wt_resultfile':wt_resultfile, 'wt_defectsdir':wt_defectsdir, \
        'wt_logsdir':wt_logsdir, 'wt_testcase_filepath': wt_testcase_filepath, 'jiraproj':None}
        cls_obj = DefectsDriver(data_repository)
        result = cls_obj.create_failing_kw_json()
        assert result == True
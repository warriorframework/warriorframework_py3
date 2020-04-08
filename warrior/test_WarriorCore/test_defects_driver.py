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
from unittest import TestCase
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    print(WARRIORDIR)
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore import defects_driver
from warrior.WarriorCore.defects_driver import DefectsDriver

class test_DefectsDriver(TestCase):
    """ Defects Driver Class """

    def test_create_failing_kw_json(self):
        """Create a json file each failing keyword """

        wt_resultfile = os.path.join(os.path.split(__file__)[0], "defects_driver_results_tc.xml")
        wt_defectsdir = os.getcwd()

        temp_logs_dir = os.getcwd()
        with open(temp_logs_dir+'myfile.log', 'w') as fp:
            pass
        wt_logsdir = os.path.join(temp_logs_dir, 'myfile.log')
        wt_testcase_filepath = os.path.join(os.path.split(__file__)[0], "defects_driver_tc.xml")
        data_repository = {'wt_resultfile':wt_resultfile, 'wt_defectsdir':wt_defectsdir, \
        'wt_logsdir':wt_logsdir, 'wt_resultfile':wt_resultfile, 'wt_testcase_filepath':\
        wt_testcase_filepath, 'jiraproj':None}
        cls_obj = DefectsDriver(data_repository)
        result = cls_obj.create_failing_kw_json()
        assert result == True
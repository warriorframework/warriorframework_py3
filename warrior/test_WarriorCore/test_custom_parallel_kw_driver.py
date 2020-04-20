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
import datetime
import xml.etree.ElementTree as ET

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

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)

from warrior.WarriorCore.multiprocessing_utils import update_tc_junit_resultfile

from warrior.WarriorCore import custom_parallel_kw_driver

def test_main():
    """Executes the list of steps in parallel
    Computes and returns the testcase status"""

    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "testcase_custom_par.xml"))

    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    temp_logs_dir = os.getcwd()

    with open(temp_logs_dir+'resultfile.txt', 'w') as fp:
        pass
    wt_resultfile = os.path.join(temp_logs_dir, 'resultfile.txt')

    step_list = tree.findall('Steps/step')
    tc_status = False
    data_repository = {'wt_junit_object':None, 'wt_tc_timestamp':timestamp,\
     'wt_resultfile':wt_resultfile}

    result = custom_parallel_kw_driver.main(step_list, data_repository, tc_status,\
     system_name=None)
    assert result == False


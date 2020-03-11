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

'''
UT for defects_driver
'''
import sys, os
from os.path import abspath, dirname
from argparse import Namespace

# import pdb
# pdb.set_trace()
try:
    from warrior.WarriorCore import defects_driver
#except ModuleNotFoundError as error:
except:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(WARRIORDIR)
    try:
        from warrior.WarriorCore import defects_driver
    except:
        raise

from unittest.mock import patch, sentinel
from unittest.mock import MagicMock, Mock

class temp():
    def __init__(self):
        self.matching_method_list = [1,2]
        self.matching_function_list = []
    def execute_method_for_keyword(self):
        return "sd"
sys.modules['warrior.WarriorCore.Classes.kw_driver_class.ModuleOperations'] = MagicMock(return_value = temp())
sys.modules['warrior.WarriorCore.Classes.kw_driver_class.KeywordOperations'] = MagicMock(return_value = temp())
sys.modules['warrior.WarriorCore.Classes.kw_driver_class.skip_and_report_status'] = MagicMock(return_value = None)
from warrior.WarriorCore.Classes import kw_driver_class
from warrior.WarriorCore import kw_driver
from warrior.Actions import CommonActions
from warrior.WarriorCore.Classes import kw_driver_class# import ModuleOperations
from warrior.Framework import Utils




def test_execute_keyword1():
    kw_driver.get_package_name_list = MagicMock(return_value = [1])
    Utils.testcase_Utils.get_wdesc_string = MagicMock(return_value = None)
    Utils.testcase_Utils.pStep = MagicMock(return_value = None)
    keyword = 'some keyword'
    data_repository = {}
    args_repository = {'timeout': '1'}
    package_list = [1,2,3,4]
    result = kw_driver.execute_keyword(keyword, data_repository, args_repository, package_list)
    assert result == None
    sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.ModuleOperations')
    sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.KeywordOperations')
    sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.skip_and_report_status')

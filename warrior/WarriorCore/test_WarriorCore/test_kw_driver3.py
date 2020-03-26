import sys
import os
from os.path import abspath, dirname
from unittest.mock import patch, sentinel
from unittest.mock import MagicMock, Mock

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    sys.path.append('/'.join(__file__.split('/')[:-4]))

class temp():
    def __init__(self):
        self.matching_method_list = []
        self.matching_function_list = [1]
    def execute_method_for_keyword(self):
        return "sd"
    def execute_function_for_keyword(self):
        return "pq"
sys.modules['warrior.WarriorCore.Classes.kw_driver_class'] = MagicMock(return_value=temp())
sys.modules['warrior.Framework.Utils'] = MagicMock(return_value = None)
sys.modules['warrior.Framework.Utils.print_Utils'] = MagicMock(return_value = None)

from warrior.WarriorCore import kw_driver

from warrior.Framework import Utils
from warrior.WarriorCore.Classes.kw_driver_class import ModuleOperations, KeywordOperations,\
skip_and_report_status
from warrior.Framework.Utils.print_Utils import print_info




def test_execute_keyword1():
    kw_driver.get_package_name_list = MagicMock(return_value = [1])
    Utils.testcase_Utils.get_wdesc_string = MagicMock(return_value = None)
    Utils.testcase_Utils.pStep = MagicMock(return_value = None)
    keyword = 'some keyword'
    data_repository = {}
    args_repository = {'timeout': '1'}
    package_list = [1,2,3,4]

    result = kw_driver.execute_keyword(keyword, data_repository, args_repository, package_list)
    # assert result == "pq"
    # sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.ModuleOperations')
    # sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.KeywordOperations')
    # sys.modules.pop('warrior.WarriorCore.Classes.kw_driver_class.skip_and_report_status')

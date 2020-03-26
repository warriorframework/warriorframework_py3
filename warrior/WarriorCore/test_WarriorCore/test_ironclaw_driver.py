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
from unittest.mock import MagicMock


try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

sys.modules['warrior.WarriorCore.Classes.kw_driver_class'] = MagicMock(return_value=None)
sys.modules['warrior.WarriorCore.Classes.execution_files_class'] = MagicMock(return_value=None)
sys.modules['warrior.WarriorCore.Classes.ironclaw_class'] = MagicMock(return_value=None)
from warrior.WarriorCore import ironclaw_driver

warrior.Framework.Utils.print_Utils = MagicMock(return_value=None)
warrior.Framework.Utils.xml_Utils = MagicMock(return_value=None)
warrior.Framework.Utils.file_Utils = MagicMock(return_value=None)
warrior.Framework.Utils.testcase_Utils = MagicMock(return_value=None)

from warrior.WarriorCore.Classes.ironclaw_class import IronClaw
# from warrior.Framework.Utils.print_Utils import print_info, print_error
# from warrior.Framework.Utils import xml_Utils, file_Utils, testcase_Utils
# from xml.etree import ElementTree
# from warrior.Framework.Utils.print_Utils import print_info, print_error
# from warrior.Framework.Utils import xml_Utils, file_Utils, testcase_Utils

def test_main1():
    from warrior.WarriorCore.ironclaw_driver import main

    parameter_list = ['/home/tony/dummy.xml']
    valid = True
    print_info = MagicMock(return_value=None)
    from warrior.WarriorCore import ironclaw_driver
    ironclaw_driver.iron_claw_warrior_xml_files = MagicMock(reutn_value="")
    warrior.Framework.Utils.file_Utils.get_extension_from_path = MagicMock(return_value=".xml")
    warrior.Framework.Utils.file_Utils.getAbsPath = MagicMock(return_value="")
    warrior.Framework.Utils.testcase_Utils.convertLogic = MagicMock(return_value="")
    filepath = "/home/tony/dummy.xml"
    # abs_filepath = ""
    # res = ""
    # result = ""
    # valid &= res
    main(parameter_list)

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

import time
import os
import sys
import platform
import re
import getpass
import subprocess


try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    sys.path.append('/'.join(__file__.split('/')[:-4]))

from unittest.mock import MagicMock
sys.modules['warrior.Framework.Utils'] = MagicMock(return_value=None)
sys.modules['warrior.Framework.Utils.file_Utils'] = MagicMock(return_value=None)
sys.modules['warrior.Framework.Utils.testcase_Utils'] = MagicMock(return_value=None)
sys.modules['warrior.Framework.Utils.print_Utils'] = MagicMock(return_value=None)

from warrior.Framework.Utils.print_Utils import print_info, print_notype
from warrior.Framework.Utils import file_Utils
from warrior.Framework.Utils.testcase_Utils import pNote

def test_warrior_banner():
	"""
	UT for warrior banner
	"""
	from warrior.WarriorCore.framework_detail import warrior_banner
	warrior_banner()

def test_warrior_framework_details():
	"""
	UT for warrior_framework_details
	"""
	from warrior.WarriorCore.framework_detail import warrior_framework_details

	file_Utils.fileExists = MagicMock(return_value=True)
	warrior_framework_details()

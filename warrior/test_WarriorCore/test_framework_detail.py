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
from os.path import abspath, dirname
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore import framework_detail

def test_warrior_banner():
    """This prints banner of warrior. The font is standard
    """
    framework_detail.warrior_banner()

def test_warrior_framework_details():
    """This gets framework details such the executing framework path, release
        & version details.
    """
    result = framework_detail.warrior_framework_details()
    assert result == None

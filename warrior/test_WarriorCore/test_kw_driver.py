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

import os, sys
from unittest.mock import MagicMock
from os.path import abspath, dirname
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et

from warrior.WarriorCore import kw_driver
import warrior.Actions.CommonActions

def test_execute_keyword():
    """ Executes the keyword provided by product driver
    1. searches for class methods in the package list
    2. searches for independent functions in the package list
    3. If class method matching the keyword is found in the actions package executes it
        else searches for independent fucntions matching the keyword name and executes it
    """
    keyword = 'store_in_repo'
    data_repository = {'db_obj': False, 'war_file_type': 'Case', 'wt_results_execdir': None,\
     'wt_logs_execdir': None, 'wt_name': 'test', 'step_num':None}
    args_repository = {'datavar': 'a', 'datavalue': 'b'}
    warrior.Framework.Utils.testcase_Utils.pStep = MagicMock(return_value=None)

    package_list = [warrior.Actions.CommonActions]
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    result = kw_driver.execute_keyword(keyword, data_repository, args_repository, package_list)
    assert result == {'db_obj': False, 'war_file_type': 'Case', 'wt_results_execdir': None,\
    'wt_logs_execdir': None, 'wt_name': 'test', 'step_num': None, 'step-None_status': True}
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository
    del warrior.Framework.Utils.testcase_Utils.pStep

def test_execute_keyword_empty_package_list():
    """ Executes the keyword provided by product driver
    1. searches for class methods in the package list
    2. searches for independent functions in the package list
    3. If class method matching the keyword is found in the actions package executes it
        else searches for independent fucntions matching the keyword name and executes it
    """
    keyword = ''
    data_repository = {'db_obj': False, 'war_file_type': 'Case', 'wt_results_execdir': None,\
     'wt_logs_execdir': None, 'wt_name': 'test', 'step_num':None}
    args_repository = {'datavar': 'a', 'datavalue': 'b'}
    warrior.Framework.Utils.testcase_Utils.pStep = MagicMock(return_value=None)

    package_list = []
    warrior.Framework.Utils.data_Utils.update_datarepository = MagicMock()
    input_dict = {"loop_iter_number":None}
    warrior.Framework.Utils.config_Utils.data_repository = MagicMock(return_value=data_repository)
    result = kw_driver.execute_keyword(keyword, data_repository, args_repository, package_list)
    assert result == {'db_obj': False, 'war_file_type': 'Case', 'wt_results_execdir': None,\
    'wt_logs_execdir': None, 'wt_name': 'test', 'step_num': None, 'step-None_status': 'ERROR'}
    del warrior.Framework.Utils.data_Utils.update_datarepository
    del warrior.Framework.Utils.config_Utils.data_repository

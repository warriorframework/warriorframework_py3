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
import datetime
import pytest
from unittest.mock import MagicMock
from os.path import abspath, dirname
import unittest
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

import xml.dom.minidom
import xml.etree.ElementTree as ET

from warrior.WarriorCore import exec_type_driver

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class.ArgumentDatatype'] = MagicMock()

from warrior.Framework.Utils.data_Utils import get_object_from_datarepository, verify_data
from warrior.Framework.Utils import config_Utils

def test_main():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[1]
    data_repository = {'step_1_result': 'PASS'}
    config_Utils.data_repository = MagicMock(return_value=data_repository)
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == None
    assert result2 == 'next'
    del config_Utils.data_repository

def test_main_exec_type_NO():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[3]
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == False
    assert result2 == 'SKIP'

def test_main_exec_type_YES():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[0]
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == True
    assert result2 == None

def test_main_exec_type_INVOKED():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[4]
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == False
    assert result2 == 'SKIP_INVOKED'

def test_main_exec_type_invalid():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[5]
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == False
    assert result2 == None

def test_main_logical_decision():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[1]
    data_repository = {'step_1_result': 'PASS'}
    config_Utils.data_repository = MagicMock(return_value=data_repository)
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result1 == None
    assert result2 == 'next'
    del config_Utils.data_repository

def test_main_expression_parser():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc2_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[3]
    data_repository = {'step_1_result': 'PASS'}
    exec_type_driver.rule_parser = MagicMock()
    config_Utils.data_repository = MagicMock(return_value=data_repository)
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result2 == 'next'
    del config_Utils.data_repository
    del exec_type_driver.rule_parser

def test_main_expression_parser1():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc2_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[4]
    data_repository = {'step_1_result': 'PASS'}
    exec_type_driver.rule_parser = MagicMock()
    config_Utils.data_repository = MagicMock(return_value=data_repository)
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result2 == 'next'
    del config_Utils.data_repository
    del exec_type_driver.rule_parser

def test_main_expression_parser_if_not():
    """
    UT for main
    """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "tc1_exec_type_driver.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[6]
    data_repository = {'step_1_result': 'PASS'}
    exec_type_driver.rule_parser = MagicMock()
    config_Utils.data_repository = MagicMock(return_value=data_repository)
    result1, result2 = exec_type_driver.main(sstep, skip_invoked=True)
    assert result2 == 'next'
    del config_Utils.data_repository
    del exec_type_driver.rule_parser

sys.modules.pop('warrior.WarriorCore.Classes.argument_datatype_class.ArgumentDatatype')
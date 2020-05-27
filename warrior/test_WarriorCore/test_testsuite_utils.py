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
    sys.path.append(WARRIORDIR)
    import warrior

import datetime
import xml.etree.ElementTree as ET
from warrior.WarriorCore import testsuite_utils
from warrior.Framework.Utils import xml_Utils

def test_report_testsuite_result():
    """Reports the result of the testsuite executed"""
    suite_repository = {'suite_name':'exmp_suite_file'}
    suite_status = True
    result = testsuite_utils.report_testsuite_result(suite_repository, suite_status)
    assert result == 'PASS'

def test_get_suite_timestamp():
    """Returns the date-time stamp for the start of testsuite execution in JUnit format """
    date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    result = testsuite_utils.get_suite_timestamp()
    assert result == date_time

def test_get_path_from_xmlfile():
    """Gets the testcase/testsuite path  from the testsuite.xml/project.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    testcases = root.find("Testcases")
    for tc in testcases.findall('Testcase'):
        element = tc
        result = testsuite_utils.get_path_from_xmlfile(element)
        assert result == "exmp_testcase_file.xml"

def test_get_path_from_xmlfile_path_none():
    """Gets the testcase/testsuite path  from the testsuite.xml/project.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file1.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[2]
    result = testsuite_utils.get_path_from_xmlfile(element)
    assert result == None

def test_get_data_file_at_suite_step_with_data_file():
    """Gets the testcase/testsuite path  from the testsuite.xml/project.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml"))
    # get root element
    root = tree.getroot()
    data_file = os.getcwd()
    # getting steps
    suite_repository = {'suite_exectype':'iterative_parallel', 'data_file':data_file}
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[1]
    result = testsuite_utils.get_data_file_at_suite_step(element, suite_repository)
    assert result == data_file

def test_get_data_file_at_suite_step():
    """Gets the testcase/testsuite path  from the testsuite.xml/project.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    suite_repository = {'suite_exectype':'sequential_testcases'}
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[0]
    result = testsuite_utils.get_data_file_at_suite_step(element, suite_repository)
    assert result == None

def test_get_jiraids_from_xmlfile():
    """Gets the jiraid value of a testcase from the testsuite.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file1.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[3]
    result = testsuite_utils.get_jiraids_from_xmlfile(element)
    assert result == ['WAR-123']

def test_compute_testsuite_status():
    """Computes the status of the testsuite based on the impact value for the testcase"""
    suite_status = True
    tc_status = True
    tc_impact = "impact"
    result = testsuite_utils.compute_testsuite_status(suite_status, tc_status, tc_impact)
    assert result == True

def test_compute_testsuite_status_noimpact():
    """Computes the status of the testsuite based on the impact value for the testcase"""
    suite_status = True
    tc_status = True
    tc_impact = "noimpact"
    result = testsuite_utils.compute_testsuite_status(suite_status, tc_status, tc_impact)
    assert result == True

def test_get_runtype_from_xmlfile():
    """Gets the runtype value of a testcase from the testsuite.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml"))
    # get root element
    root = tree.getroot()
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[0]
    result = testsuite_utils.get_runtype_from_xmlfile(element)
    assert result == 'sequential_keywords'

def test_get_runtype_from_xmlfile_runtype_none():
    """Gets the runtype value of a testcase from the testsuite.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file1.xml"))
    # get root element
    root = tree.getroot()
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[0]
    result = testsuite_utils.get_runtype_from_xmlfile(element)
    assert result == 'sequential_keywords'

def test_get_runtype_from_xmlfile_unsuported_type():
    """Gets the runtype value of a testcase from the testsuite.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file1.xml"))
    # get root element
    root = tree.getroot()
    testcases = root.find("Testcases")
    testcase_list = testcases.findall('Testcase')
    element = testcase_list[1]
    result = testsuite_utils.get_runtype_from_xmlfile(element)
    assert result == 'sequential_keywords'

def test_get_exectype_from_xmlfile():
    """Gets the exectype values for testcases from the testsuite.xml file """

    filepath = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    exectype = xml_Utils.getChildAttributebyParentTag(filepath, 'Details', 'type', 'exectype')
    result = testsuite_utils.get_exectype_from_xmlfile(filepath)
    assert result == exectype

def test_get_exectype_from_xmlfile_with_unsupported_type():
    """Gets the exectype values for testcases from the testsuite.xml file """

    filepath = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    exectype = xml_Utils.getChildAttributebyParentTag = MagicMock(return_value='junk_value')
    result = testsuite_utils.get_exectype_from_xmlfile(filepath)
    assert result == 'sequential_testcases'
    del xml_Utils.getChildAttributebyParentTag

def test_get_exectype_from_xmlfile_none():
    """Gets the exectype values for testcases from the testsuite.xml file """

    filepath = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    exectype = xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=None)
    result = testsuite_utils.get_exectype_from_xmlfile(filepath)
    assert result == 'sequential_testcases'
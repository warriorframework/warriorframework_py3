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

def test_pSuite_root():
    """ Get the root element and assign it to current pointer"""
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'psuite_root.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'psuite_root.xml'
    testsuite_utils.pSuite_root(resultfile)

def test_pSuite_testsuite():
    """ set the attributes of test suite """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    name = 'test'
    errors = '0'
    tests = '2'
    failures = '0'
    time = '0'
    skipped = '0'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    testsuite_utils.pSuite_testsuite(resultfile, name, errors, skipped, tests, failures, time,\
     timestamp)

def test_pSuite_report_suite_requirements():
    """Reports the requirements of the suite to the suite result xml file """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    requirement_id = 0
    testsuite_utils.pSuite_report_suite_requirements(resultfile, requirement_id)

def test_pSuite_testcase():
    """ set the attributes of test case """
    name = 'test'
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    requirement_id = 0
    classname = ''
    time = 0
    testsuite_utils.pSuite_testcase(resultfile, classname, name, time)

def test_pSuite_testcase_failure():
    """  Computes failed case status with message and update on case duration in
         test suite """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    time = 10
    msg = 'test failure'
    testCaseText = 'allpassed'
    testsuite_utils.pSuite_testcase_failure(resultfile, msg, time,\
     testCaseText)

def test_pSuite_testcase_skip():
    """ Computes skipped case status in test suite """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    testsuite_utils.pSuite_testcase_skip(resultfile)

def test_pSuite_testcase_error():
    """ Computes error case status with message and update on case duration in
        suite """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    time = 10
    msg = 'test error'
    testCaseText = 'error'
    testsuite_utils.pSuite_testcase_error(resultfile, msg, time, testCaseText)

def test_update_suite_duration():
    """ Updates the suite duration """
    time = 0
    testsuite_utils.update_suite_duration(time)

def test_pSuite_update_suite_attributes():
    """ Updates the suite attributes """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile = temp_logs_dir+'tsjunit.xml'
    errors = '0'
    skipped = '0'
    tests = '1'
    failures = '0'
    time = 10
    testsuite_utils.pSuite_update_suite_attributes(resultfile, errors, skipped, tests,\
     failures, time='0')

def test_pSuite_update_suite_tests():
    """ Updates the suite tests"""
    tests = 'testcase'
    testsuite_utils.pSuite_update_suite_tests(tests)

def test_get_suite_timestamp():
    """Returns the date-time stamp for the start of testsuite execution in JUnit format """
    testsuite_utils.get_suite_timestamp()

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

def test_get_data_file_at_suite_step_with_data_file():
    """Gets the testcase/testsuite path  from the testsuite.xml/project.xml file """
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml"))
    # get root element
    root = tree.getroot()
    data_file = os.getcwd()
    # getting steps
    suite_repository = {'suite_exectype':'iterative_parallel', 'data_file':data_file}
    testcases = root.find("Testcases")
    for tc in testcases.findall('Testcase'):
        element = tc
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
    for tc in testcases.findall('Testcase'):
        element = tc
        result = testsuite_utils.get_data_file_at_suite_step(element, suite_repository)
        assert result == None

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

def test_get_exectype_from_xmlfile_none():
    """Gets the exectype values for testcases from the testsuite.xml file """

    filepath = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    exectype = xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=None)
    result = testsuite_utils.get_exectype_from_xmlfile(filepath)
    assert result == 'sequential_testcases'
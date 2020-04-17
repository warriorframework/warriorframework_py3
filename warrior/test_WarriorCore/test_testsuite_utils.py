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
    resultfile =  temp_logs_dir+'psuite_root.xml'
    testsuite_utils.pSuite_root(resultfile)


def test_pSuite_testsuite():
    """ set the attributes of test suite """


    ROOT = ET.Element("testsuites")
    CURRENT_POINTER = ET.Element("testsuites")
    CURRENT_TESTSUITE_POINTER = None
    CURRENT_PROPERTIES_POINTER = None
    CURRENT_TESTCASE_POINTER = None

    G_TESTSUITE = {}
    G_TESTSUITE_LOOP = 0

    G_PROPERTIES = {}
    G_PROPERTIES_LOOP = 0

    G_PROPERTY = {}
    G_PROPERTY_LOOP = 0

    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0

    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'

    name = 'test'
    errors = '0'
    tests = '2'
    failures = '0'
    time = '0'
    skipped = '0'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    testsuite_utils.pSuite_testsuite(resultfile, name, errors, skipped, tests, failures, time, timestamp)

def test_pSuite_report_suite_requirements():
    """Reports the requirements of the suite to the suite result xml file """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'
    requirement_id = 0

    CURRENT_PROPERTIES_POINTER = None
    G_PROPERTIES = {}
    G_PROPERTIES_LOOP = 0
    G_PROPERTY = {}
    G_PROPERTY_LOOP = 0
    name = 'test'
    value = 0

    testsuite_utils.pSuite_report_suite_requirements(resultfile, requirement_id)

def test_pSuite_testcase():
    """ set the attributes of test case """

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    CURRENT_TESTSUITE_POINTER = ET.Element("testsuites")
    CURRENT_TESTCASE_POINTER = ET.SubElement(ET.Element("testsuites"), "testcase")

    G_TESTSUITE = {}
    G_TESTSUITE_LOOP = 0
    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0

    name = 'test'
    value = 0
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'
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
    resultfile =  temp_logs_dir+'tsjunit.xml'

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    CURRENT_TESTCASE_POINTER = root
    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0
    time = 10
    msg='test failure'
    testCaseText='allpassed'
    testCaseStatus = ET.SubElement(CURRENT_TESTCASE_POINTER, "failure")
    testCaseStatus.set('message', msg)
    testCaseStatus.text = testCaseText
    testsuite_utils.pSuite_testcase_failure(resultfile, msg='test failure', time='0', testCaseText='')

def test_pSuite_testcase_skip():
    """ Computes skipped case status in test suite """

    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'
    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    CURRENT_TESTCASE_POINTER = root
    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0

    testsuite_utils.pSuite_testcase_skip(resultfile)

def test_pSuite_testcase_error():
    """ Computes error case status with message and update on case duration in
        suite """
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    CURRENT_TESTCASE_POINTER = root
    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0
    time = 10
    msg='test error'
    testCaseText='error'
    testCaseStatus = ET.SubElement(CURRENT_TESTCASE_POINTER, "error")
    testCaseStatus.set('message', msg)
    testCaseStatus.text = testCaseText
    testsuite_utils.pSuite_testcase_error(resultfile, msg='test error', time='0', testCaseText='')

def test_update_suite_duration():
    """ Updates the suite duration """

    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    CURRENT_TESTSUITE_POINTER = root

    G_TESTCASE = {}
    G_TESTCASE_LOOP = 0
    time = 0

    CURRENT_TESTSUITE_POINTER.set('time', time)

    testsuite_utils.update_suite_duration(time)

def test_pSuite_update_suite_attributes():
    """ Updates the suite attributes """
    # import pdb
    # pdb.set_trace()
    temp_logs_dir = os.getcwd()
    with open(temp_logs_dir+'tsjunit.xml', 'w') as fp:
        pass
    resultfile =  temp_logs_dir+'tsjunit.xml'

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()
    errors = '0'
    skipped = '0'
    G_TESTSUITE = {}
    ROOT = root
    tests = '1'
    failures = '0'
    time = 10
    CURRENT_TESTSUITE_POINTER = root
    G_TESTSUITE_LOOP = 1
    G_TESTSUITE[G_TESTSUITE_LOOP] = root

    testsuite_utils.pSuite_update_suite_attributes(resultfile, errors, skipped, tests, failures, time='0')

def test_pSuite_update_suite_tests():
    """ Updates the suite tests"""

    path = os.path.join(os.path.split(__file__)[0], "exmp_suite_file.xml")
    tree = ET.parse(path)
    root = tree.getroot()
    ROOT = root
    CURRENT_TESTSUITE_POINTER = root
    G_TESTSUITE = {}
    G_TESTSUITE_LOOP = 1
    G_TESTSUITE[G_TESTSUITE_LOOP] = root
    tests = 'testcase'
    CURRENT_TESTSUITE_POINTER.set('tests', tests)
    testsuite_utils.pSuite_update_suite_tests(tests)

def test_get_suite_timestamp():
    """Returns the date-time stamp for the start of testsuite execution in JUnit format """
    testsuite_utils.get_suite_timestamp()

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
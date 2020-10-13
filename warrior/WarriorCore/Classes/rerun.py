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

from xml.etree import ElementTree as et
from os.path import abspath, dirname
import xml.dom.minidom
import os
import sys

def execute_failedsuite(datafile):
    '''   Searches the given xml file to get the status of the testcase  '''
    tree = et.parse(datafile)
    root = tree.getroot()
    failed_testcase_list = []
    for testsuite in root.iter("testsuite"):
        status = testsuite.get("status")
        suite_location = testsuite.get("suite_location")
        suite_name = testsuite.get("name")
        suite_title = testsuite.get("title")
        if status == "FAIL":
            print("Testsuite has failed....................We can now RERUN for failed testcase")
        else:
            print("Testsuite is passed.No need of rerun")
            sys.exit(0)
    for testcase in root.iter('testcase'):
        status = testcase.get("status")
        if status == "FAIL":
            file_path = testcase.get("testcasefile_path")
            file_name = os.path.basename(file_path)
            failed_testcase_list.append(file_name)
            print("The failed testcase path is {}".format(file_path))

        else:
            print("The testcase is passed. REREUN NOT REQUIRED")
        tree = et.parse(suite_location)
        root = tree.getroot()
        list = []
        for child in root:
            list.append(child.tag)
        if "Requirements" in list:
            new_root = root[2]
        else:
            new_root = root[1]
        for Testcase in new_root.findall('Testcase'):
            path = Testcase.find("path").text
            testcase_name = os.path.basename(path)
            if testcase_name not in failed_testcase_list:
                new_root.remove(Testcase)
        save_path_file = os.path.split(suite_location)[0] + os.sep + suite_name + "_failed.xml"
        tree.write(save_path_file)

    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))


    ''' Executing the new suite file created'''
    os.system("{} {}".format(os.path.join(WARRIORDIR,"Warrior"),save_path_file))







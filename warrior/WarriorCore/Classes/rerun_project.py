from xml.etree import ElementTree as ET
from os.path import abspath, dirname
from warrior.Framework.Utils.print_Utils import print_error, print_info
import os
import sys
import datetime

def execute_failedproject(datafile):
    tree = ET.parse(datafile)
    root = tree.getroot()
    '''Fetching the location of the project file'''
    project_loc = root[1].attrib.get("value")
    proj_name = os.path.basename(project_loc)
    proj_status = root.attrib.get("status")
    if proj_status == "PASS":
        print_info("No need of rerun...exiting !!")
        sys.exit()
    '''Creating a separate folder'''
    path = os.getcwd()
    file = "New_rerun"
    try:
        if not os.path.isdir(file):
            date = datetime.datetime.now()
            filename = file + str(date)
            filename = filename.replace(" ", "_")
            os.mkdir(filename)
        new_path = os.path.join(path, filename)
    except Exception as e:
        print_error("The file already exist")
        print_error(e)
    try:
        input_file = root[2][1].attrib.get("data_file")
    except Exception as e:
        print("Input file does not exist")
        print(e)

    failed_testsuite_list = []
    testsuite_list = []
    for testsuite in root.iter("testsuite"):
        testsuite_status = testsuite.get("status")
        suite_loc = testsuite.get("suite_location")
        suite_title = testsuite.get("title")
        name_suite = testsuite.get("name")
        suite_name = os.path.basename(suite_loc)
        if testsuite_status == "FAIL":
            failed_testsuite_list.append(suite_name)
            testsuite_list.append(suite_loc)
    failed_testcase_list = []
    failed_testcase_location = []
    for testcase in root.iter('testcase'):
        status = testcase.get("status")
        if status == "FAIL":
            testcase_loc = testcase.get("testcasefile_path")
            testcase_name = os.path.basename(testcase_loc)
            failed_testcase_list.append(testcase_name)
            failed_testcase_location.append(testcase_loc)
    setup_root = root[2]
    wrapper_list = []
    for child in setup_root:
        wrapper_list.append(child.tag)
    if "Setup" in wrapper_list:
        wrapper_file = setup_root[1].attrib.get("testcasefile_path")

    '''Removing the failed testsuite from the Junit file'''
    tree = ET.parse(project_loc)
    root = tree.getroot()
    details = root[0]
    new_root1 = root[1]
    for child in details:
        if child.tag == 'TestWrapperFile':
            child.text = wrapper_file
        elif child.tag == "InputDataFile":
            child.text = input_file

    for Testsuite in new_root1.findall('Testsuite'):
        path = Testsuite.find("path").text
        org_suite_name = os.path.basename(path)
        if org_suite_name not in failed_testsuite_list:
            new_root1.remove(Testsuite)
    for j in testsuite_list:
        for path in root.iter("path"):
            filename1 = path.text
            rel_path1 = os.path.basename(filename1)
            abs_path1 = os.path.basename(j)
            if rel_path1 == abs_path1:
                path.text = abs_path1
    save_path_file = new_path + os.sep + proj_name
    tree.write(save_path_file)
    for i in range(len(testsuite_list)):
        tree = ET.parse(testsuite_list[i])
        root = tree.getroot()
        name = os.path.basename(testsuite_list[i])
        details = root[0]
        for child in details:
            if child.tag == 'TestWrapperFile':
                child.text = wrapper_file
            elif child.tag == 'InputDataFile':
                child.text = input_file
        details_list = []
        for child in root:
            details_list.append(child.tag)
        if "Requirements" in details_list:
            new_root = root[2]
        else:
            new_root = root[1]

        for Testcase in new_root.findall('Testcase'):
            old_path = Testcase.find("path").text
            testcase_name = os.path.basename(old_path)
            if testcase_name not in failed_testcase_list:
                new_root.remove(Testcase)

        for k in failed_testcase_location:
            for path in root.iter("path"):
                filename = path.text
                rel_path = os.path.basename(filename)
                abs_path = os.path.basename(k)
                if rel_path == abs_path:
                    path.text = k

        save_path_suite_file = new_path + os.sep + name
        tree.write(save_path_suite_file)

    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))

    ''' Executing the new suite file created'''
    os.system("{} {}".format(os.path.join(WARRIORDIR, "Warrior"), save_path_file))


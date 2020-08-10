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

"""Class which generates the consolidated test cases result in console at the
end of Test Suite or Project Execution """
import os
from warrior.Framework import Utils
from warrior.Framework.Utils import xml_Utils, file_Utils, config_Utils
from warrior.Framework.Utils.print_Utils import print_info
from warrior.WarriorCore import testsuite_utils, common_execution_utils, warrior_cli_driver


class ExecutionSummary():
    """Warrior execution summary class"""
    def __init__(self, junit_file=None):
        """ Constructor """
        self.junit_file = junit_file

    def project_summary(self, junit_file):
        """To get the project name, project status and it's location"""
        tree = xml_Utils.get_tree_from_file(self.junit_file)
        project_list = []
        for names in tree.iter('testsuites'):
            proj_detail = names.attrib
            proj_name = proj_detail.get('name')
            file_type = self.get_file_type(junit_file)
            project_status = proj_detail.get('status')
            proj_loc = []
            for properties in tree.iter('property'):
                project_details = properties.attrib
                if project_details.get('name') == 'location':
                    proj_loc.append(project_details.get('value'))
                    proj_location = proj_loc[0]
            project_list.append([file_type, proj_name, project_status, proj_location])
        return project_list

    def suite_summary(self, junit_file):
        """ To get the name, status and location of both test suite and test case"""
        tree = xml_Utils.get_tree_from_file(self.junit_file)
        suite_tc_list = []
        for values in tree.iter('testsuite'):
            suite_detail = values.attrib
            suite_name = suite_detail.get('name')
            suite_status = suite_detail.get('status')
            suite_location = suite_detail.get('suite_location')
            suite_result_dir = suite_detail.get('resultsdir')
            if suite_location is not None:
                suite_tc_list.append(["Suites", suite_name, suite_status, suite_location])

            #to add Setup results in suite summary
            for value in tree.iter('Setup'):
                setup_details = value.attrib
                setup_status = setup_details.get('status')
                setup_name = setup_details.get('name')+".xml"
                setup_location = setup_details.get('testcasefile_path')
                case_result_dir_with_tc_name = setup_details.get('resultsdir')
                if case_result_dir_with_tc_name is not None:
                    case_result_dir = os.path.dirname(case_result_dir_with_tc_name)
                    # suite junit element will not have resultsdir attrib for case execution
                    if suite_result_dir is None or suite_result_dir == case_result_dir:
                        suite_tc_list.append(["Setup", setup_name, setup_status, setup_location])
            for value in tree.iter('testcase'):
                testcase_details = value.attrib
                testcase_status = testcase_details.get('status')
                testcase_name = testcase_details.get('name')+".xml"
                testcase_location = testcase_details.get('testcasefile_path')
                case_result_dir_with_tc_name = testcase_details.get('resultsdir')
                if case_result_dir_with_tc_name is not None:
                    case_result_dir = os.path.dirname(case_result_dir_with_tc_name)
                    # suite junit element will not have resultsdir attrib for case execution
                    if suite_result_dir is None or suite_result_dir == case_result_dir:
                        suite_tc_list.append(["Testcase", testcase_name, testcase_status,
                                              testcase_location])
            #to add debug results in suite summary
            for value in tree.iter('Debug'):
                debug_details = value.attrib
                debug_status = debug_details.get('status')
                debug_name = debug_details.get('name')+".xml"
                debug_location = debug_details.get('testcasefile_path')
                case_result_dir_with_tc_name = debug_details.get('resultsdir')
                if case_result_dir_with_tc_name is not None:
                    case_result_dir = os.path.dirname(case_result_dir_with_tc_name)
                    # suite junit element will not have resultsdir attrib for case execution
                    if suite_result_dir is None or suite_result_dir == case_result_dir:
                        suite_tc_list.append(["Debug", debug_name, debug_status, debug_location])
            #to add Cleanup results in suite summary
            for value in tree.iter('Cleanup'):
                cleanup_details = value.attrib
                cleanup_status = cleanup_details.get('status')
                cleanup_name = cleanup_details.get('name')+".xml"
                cleanup_location = cleanup_details.get('testcasefile_path')
                case_result_dir_with_tc_name = cleanup_details.get('resultsdir')
                if case_result_dir_with_tc_name is not None:
                    case_result_dir = os.path.dirname(case_result_dir_with_tc_name)
                    # suite junit element will not have resultsdir attrib for case execution
                    if suite_result_dir is None or suite_result_dir == case_result_dir:
                        suite_tc_list.append(["Cleanup", cleanup_name, cleanup_status, cleanup_location])
                        
        # suite_tc_list appends suites and test cases as per execution order
        return suite_tc_list

    def get_file_type(self, junit_file):
        """To get the file type which is given for execution"""
        tree = xml_Utils.get_tree_from_file(self.junit_file)
        for names in tree.iter('testsuites'):
            file_detail = names.attrib
            file_val = file_detail.get('name')
            if file_val == "customProject_independant_testcase_execution":
                file_type = "Suites"
            else:
                file_type = "Project"
        return file_type

    def print_result_in_console(self, junit_file):
        """To print the consolidated test cases result in console at the end of Test Case/Test
           Suite/Project Execution"""
        file_type = self.get_file_type(junit_file)
        # Formatting execution summary as project_summary and suite_summary returns the list values
        print_info("+++++++++++++++++++++++++++++++++++++++++++++++++ Execution Summary +++++++++++++++++++++++++++++++++++++++++++++++++")
        print_info("{0:10}{1:50}{2:10}{3:50}".format('Type', 'Name [DataFile]', 'Status', 'Path'))
        if file_type == "Project":
            project_exec = self.project_summary(junit_file)
            for proj in project_exec:
                print_info(("{0:10}{1:50}{2:10}{3:30}"
                            .format(proj[0], proj[1], proj[2], proj[3])))
            suite_tc_exec = self.suite_summary(junit_file)
            self.print_execution_summary_details(suite_tc_exec)
        elif file_type == "Suites":
            suite_tc_exec = self.suite_summary(junit_file)
            self.print_execution_summary_details(suite_tc_exec)
        print_info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def print_execution_summary_details(self, suite_tc_exec):
        """To print the consolidated test cases result in console at the end of
           Test Case/Test Suite/Project Execution"""
        data_repositery = config_Utils.data_repository
        for suite_tc in suite_tc_exec:
            path = suite_tc[3]
            name = suite_tc[1]
            if suite_tc_exec[0][0] == 'Suites' and file_Utils.fileExists(path):
                if suite_tc[0] == 'Suites':
                    testsuite_filepath = suite_tc[3]
                    from_project = {'db_obj': False, 'war_file_type': 'Suite'}
                    suite_repository = warrior_cli_driver.testsuite_driver. \
                        get_suite_details(testsuite_filepath, from_project,
                                          False, None, None)
                    testsuite_dir = os.path.dirname(testsuite_filepath)

                    testcase_list = common_execution_utils.get_step_list(
                        suite_tc[3], "Testcases", "Testcase", randomize=False)
                    suite_datafile = xml_Utils.getChildTextbyParentTag(
                        suite_tc[3], 'Details', 'InputDataFile')
                    if suite_datafile is None or suite_datafile is False or \
                            str(suite_datafile).strip() == "":
                        suite_datafile = "NO_DATA"
                    datafile_dict = {}
                    for tests in testcase_list:
                        tc_rel_path = testsuite_utils.get_path_from_xmlfile(tests)
                        if tc_rel_path is not None:
                            tc_path = Utils.file_Utils.getAbsPath(
                                tc_rel_path, testsuite_dir)
                        else:
                            tc_path = str(tc_rel_path)
                        if suite_repository["suite_exectype"].upper() == "ITERATIVE_SEQUENTIAL" \
                                or suite_repository["suite_exectype"].upper() == "ITERATIVE_PARALLEL":
                            suite_step_data_file = suite_repository["data_file"]
                        else:
                            suite_step_data_file = xml_Utils.get_text_from_direct_child(
                                tests, 'InputDataFile')
                        if suite_step_data_file is None or suite_step_data_file is False:
                            suite_step_data_file = None
                        elif suite_step_data_file is not None and suite_step_data_file is not False:
                            suite_step_data_file = str(suite_step_data_file).strip()
                        if suite_step_data_file is not None:
                            data_file = Utils.file_Utils.getAbsPath(
                                suite_step_data_file, testsuite_dir)
                            datafile_dict[tc_path] = data_file
                if suite_tc[0] == 'Testcase':
                    if data_repositery is not None and 'ow_datafile' in data_repositery:
                        name = name + ' [' + os.path.basename(data_repositery['ow_datafile']) + ']'
                    elif path in datafile_dict:
                        name = name + ' [' + os.path.basename(datafile_dict[path]) + ']'
                    elif str(suite_datafile).strip().upper() != 'NO_DATA' and \
                            file_Utils.fileExists(suite_datafile):
                        suite_datafile_rel = str(suite_datafile).strip()
                        suite_datafile = file_Utils.getAbsPath(
                            suite_datafile_rel, os.path.dirname(path))
                        name = name + ' [' + os.path.basename(suite_datafile) + ']'
                    else:
                        datafile = xml_Utils.getChildTextbyParentTag(
                            path, 'Details', 'InputDataFile')
                        if datafile is None or datafile is False or \
                                str(datafile).strip() == "":
                            datafile = "NO_DATA"
                        if str(datafile).strip().upper() != 'NO_DATA' and \
                                datafile is not False and \
                                file_Utils.fileExists(datafile):
                            datafile_rel = str(datafile).strip()
                            datafile = file_Utils.getAbsPath(
                                datafile_rel, os.path.dirname(path))
                            name = name + ' [' + os.path.basename(datafile) + ']'

            print_info(("{0:10}{1:50}{2:10}{3:30}"
                        .format(suite_tc[0], name, suite_tc[2], suite_tc[3])))

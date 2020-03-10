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

import sys
import os
import shutil

try:
    from warrior.WarriorCore import testcase_driver
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(WARRIORDIR)
    try:
        from warrior.WarriorCore import testcase_driver
    except:
        raise
from unittest.mock import MagicMock
from warrior.WarriorCore import testcase_driver
from warrior.Framework.Utils import config_Utils, xml_Utils, \
    testcase_Utils, file_Utils, string_Utils
from warrior.WarriorCore import framework_detail, defects_driver
from warrior.WarriorCore.Classes import hybrid_driver_class, execution_files_class
from warrior.Framework.ClassUtils.database_utils_class import WMongodb
from warrior.WarriorCore.Classes import junit_class
from warrior.Framework import Utils

string_Utils.strip_white_spaces = MagicMock(return_value=[1, 2, 3, 4, "a", 6, 7, 8, 9])
config_Utils.set_datarepository = MagicMock(return_value=None)
config_Utils.debug_file = MagicMock(returDocn_value=None)
config_Utils.set_resultfile = MagicMock(return_value=None)
config_Utils.set_datafile = MagicMock(return_value=None)
config_Utils.set_logsdir = MagicMock(return_value=None)
config_Utils.set_filename = MagicMock(return_value=None)
config_Utils.set_logfile = MagicMock(return_value=None)
config_Utils.set_testcase_path = MagicMock(return_value=None)
xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
xml_Utils.getChildTextbyParentTag = MagicMock(return_value=False)
xml_Utils.getRoot = MagicMock(return_value=None)
testcase_Utils.get_defonerror_fromxml_file = MagicMock(return_value='None')
testcase_Utils.pTestcase = MagicMock(return_value=None)
testcase_Utils.pCustomTag = MagicMock(return_value=None)
os.path.basename = MagicMock(return_value=None)
os.path.dirname = MagicMock(return_value=None)
shutil.copy2 = MagicMock(return_value=None)
file_Utils.getNameOnly = MagicMock(return_value=None)
file_Utils.createDir = MagicMock(return_value=None)
file_Utils.getCustomLogFile = MagicMock(return_value=None)
testcase_Utils.pReportRequirements = MagicMock(return_value=None)
testcase_Utils.pTestResult = MagicMock(return_value=None)
framework_detail.warrior_framework_details = MagicMock(return_value=None)
defects_driver.DefectsDriver.create_failing_kw_json = MagicMock(return_value=True)
defects_driver.DefectsDriver.connect_warrior_jira = MagicMock(return_value=True)
# testcase_driver.create_defects = MagicMock(return_value = None)
# testcase_driver.execute_custom = MagicMock(return_value = True)
xml_Utils.getRoot = MagicMock(return_value=None)
# testcase_driver.get_testcase_details = MagicMock(return_value = None)
# testcase_driver.junit_requirements = MagicMock(return_value = None)
# testcase_driver.report_testcase_result = MagicMock(return_value = None)
# testcase_driver.check_robot_wrapper_case = MagicMock(return_value = False)
# testcase_driver.print_testcase_details_to_console = MagicMock(return_value = None)
junit_class.Junit.add_jobid = MagicMock(return_value='mocked')
junit_class.Junit.create_testcase = MagicMock(return_value=None)
junit_class.Junit.add_property = MagicMock(return_value=None)
junit_class.Junit.update_attr = MagicMock(return_value=None)
junit_class.Junit.update_count = MagicMock(return_value=None)
junit_class.Junit.output_junit = MagicMock(return_value=None)
junit_class.Junit.add_testcase_message = MagicMock(return_value=None)
WMongodb.add_html_result_to_mongodb = MagicMock(return_value=None)
WMongodb.add_xml_result_to_mongodb = MagicMock(return_value=None)
Utils.datetime_utils.get_current_timestamp = MagicMock(return_value=None)
Utils.datetime_utils.get_time_delta = MagicMock(return_value='2')
Utils.file_Utils.fileExists = MagicMock(return_value=True)


def test_get_testcase_details():
    """get_testcase_details"""

    class temp(object):
        """temp"""

        def __init__(self):
            """init"""
            self.resultfile = "resultfile"
            self.resultsdir = "resultfile"
            self.logfile = "resultfile"
            self.logsdir = "resultfile"

        def get_defect_files(self):
            """get_defect_files"""
            return "string"

        def check_get_datatype(self, a):
            """check_get_datatype"""
            return "string"

    obj = temp()
    execution_files_class.ExecFilesClass = MagicMock(return_value=obj)
    testcase_filepath = "some path of testcase"
    data_repository = {
        'db_obj': False,
        'war_file_type': 'Case',

        'wt_results_execdir': "sdfsd",
        'ow_resultdir': 'sdf',

        'wt_logs_execdir': 'ssdf',
        'ow_logdir': 'ewf',
        'ow_datafile': 'sadf',
    }
    jiraproj = None
    result = testcase_driver.get_testcase_details(testcase_filepath, data_repository, jiraproj)
    assert result['db_obj'] is False
    assert result['war_file_type'] == 'Case'
    assert result['wt_results_execdir'] == 'sdfsd'
    assert result['ow_resultdir'] == 'sdf'
    assert result['wt_logs_execdir'] == 'ssdf'
    assert result['ow_logdir'] == 'ewf'
    assert result['ow_datafile'] == 'sadf'
    assert result['wt_name'] == 1
    assert result['wt_testcase_filepath'] == 'some path of testcase'
    assert result['wt_title'] == 2
    assert result['wt_filename'] is None
    assert result['wt_filedir'] is None
    assert result['wt_datafile'] == 4
    assert result['wt_data_type'] == 'A'
    assert result['wt_resultsdir'] == 7
    assert result['wt_resultfile'] == 'resultfile'
    assert result['wt_logsdir'] == 6
    assert result['wt_kw_results_dir'] is None
    assert result['wt_defectsdir'] == 8
    assert result['wt_console_logfile'] is None
    assert result['wt_expResults'] == 9
    assert result['wt_operating_system'] == 'LINUX'
    assert result['wt_def_on_error_action'] == 'NONE'
    assert result['wt_def_on_error_value'] is None
    assert result['jiraproj'] is None
    del xml_Utils.getRoot


def test_report_testcase_requirements():
    """report test case requirements"""
    testcase_Utils.get_requirement_id_list = MagicMock(return_value=[1, 2, 3, 4])
    testcase_filepath = "file path"
    testcase_driver.report_testcase_requirements(testcase_filepath)


def test_compute_testcase_status1():
    """test_compute_testcase_status1"""
    step_status = None
    tc_status = True
    result = testcase_driver.compute_testcase_status(step_status, tc_status)
    assert result is True


def test_compute_testcase_status2():
    """test_compute_testcase_status2"""
    step_status = True
    tc_status = False
    result = testcase_driver.compute_testcase_status(step_status, tc_status)
    assert result is False


def test_report_testcase_result(capsys):
    """test_report_testcase_result"""

    class temp3(object):
        """temp"""

        def values(self):
            """values"""
            return 'text'

        def __init__(self):
            """init"""
            self.text = "text"

    class temp2(object):
        """temp2"""

        def __init__(self):
            """init"""
            self.attrib = temp3()

        def find(self, a):
            """find"""
            obj2 = temp3()
            return obj2

    class temp(object):
        """temp"""
        def __init__(self):
            """init"""
            pass

        def findall(self, a):
            """findall"""
            obj = temp2()
            return 5 * [obj]

    obj2 = temp()
    xml_Utils.getRoot = MagicMock(return_value=obj2)
    tc_status = True
    data_repository = {
        'wt_name': "asdas",
        'wt_resultfile': 'sdfsd'
    }
    testcase_driver.report_testcase_result(tc_status, data_repository)
    captured = capsys.readouterr()
    assert captured.out == '-I- \n**** Testcase Result ***\n-I- TESTCASE:asdas  STATUS:PASS\n-I- \n\n-I- ++++++++++++++++++++++++ Summary of Failed Keywords ++++++++++++++++++++++++\n-I- StepNumber      KeywordName                                   Status    \n-I- t,e,x,t         Steps-text                                    text      \n-I- t,e,x,t         Steps-text                                    text      \n-I- t,e,x,t         Steps-text                                    text      \n-I- t,e,x,t         Steps-text                                    text      \n-I- t,e,x,t         Steps-text                                    text      \n-I- =================== END OF TESTCASE ===========================\n'

    del xml_Utils.getRoot

# this case I am not able make it work we need to check the source code
# def test_get_system_list():
#     class temp3():
#         def get(self, a):
#             return 'yes'
#         def __init__(self):
#             self.text = "text"
#
#     class temp2():
#         def __init__(self):
#             self.attrib = temp3()
#         def get(self, a):
#             return 'yes'
#         def findall(self, a):
#             obj2 = temp3()
#             return 5*[obj2]
#     class temp():
#         def findall(self,a):
#             obj= temp2()
#             return 5*[obj]
#     obj2 = temp()
#     xml_Utils.getRoot = MagicMock(return_value = obj2)
#     tc_status = True
#     datafile = "data file"
#     result = testcase_driver.get_system_list(datafile)



def test_get_system_list():
    """test_get_system_list"""

    class temp3(object):
        """temp3"""

        def get(self, a):
            """get"""
            return 'yes'

        def __init__(self):
            """init"""
            self.text = "text"

    class temp2(object):
        """temp2"""

        def __init__(self):
            """init"""
            self.attrib = temp3()

        def get(self, a):
            """get"""
            return 'system'

        def findall(self, a):
            """findall"""
            obj2 = temp3()
            return []

    class temp(object):
        """temp"""
        def __init__(self):
            """init"""
            pass

        def findall(self, a):
            """findall"""
            obj = temp2()
            return 5 * [obj]
            # return [1,2,3,4]

    obj2 = temp()
    xml_Utils.getRoot = MagicMock(return_value=obj2)
    tc_status = True
    datafile = "data file"
    result = testcase_driver.get_system_list(datafile, node_req=True)
    assert result[0] == ['system', 'system', 'system', 'system', 'system']
    for obj in result[1]:
        assert obj.__class__.__name__ == 'temp2'
    result = testcase_driver.get_system_list(datafile, iter_req=True)
    assert result == ['system', 'system', 'system', 'system', 'system']


def test_print_testcase_details_to_console(capsys):
    """test_print_testcase_details_to_console"""
    testcase_filepath = "b"
    data_repository = {
        'wt_title': 'tittle',
        'wt_resultsdir': 'reult dir',
        'wt_logsdir': 'log dir',
        'wt_defectsdir': 'defects dir',
        'wt_datafile': 'datafile',
        'wt_testwrapperfile': True,
        'wt_expResults': 'exp results',
    }
    testcase_driver.print_testcase_details_to_console(testcase_filepath, data_repository, steps_tag="Step")
    captured = capsys.readouterr()
    result = captured.out
    assert result == '-I- \n===============================  TC-DETAILS  ==================================================\n-I- Title: tittle\n-I- Results directory: reult dir\n-I- Logs directory: log dir\n-I- Defects directory: defects dir\n-I- Datafile: datafile\n-I- Testwrapperfile: True\n-I- Expected Results: exp results\n-I- ================================================================================================\n'


def test_create_defects(capsys):
    """test_create_defects"""
    data_repository = {
        'wt_resultfile': '1',
        'wt_defectsdir': 'some dir',
        'wt_logsdir': '2',
        'wt_testcase_filepath': '4',
        'jiraproj': '5'
    }
    defects_driver.DefectsDriver.get_defect_json_list = MagicMock(return_value=[1, 2, 3, 4])
    # defects_driver.DefectsDriver.get_defect_json_list = MagicMock(return_value = [1,2,3,4])
    # defects_driver.DefectsDriver.connect_warrior_jira = MagicMock(return_value = False)
    auto_defects = True
    # auto_defects= False
    testcase_driver.create_defects(auto_defects, data_repository)
    captured = capsys.readouterr()
    result = captured.out


def test_check_and_create_defects():
    """test_check_and_create_defects"""
    tc_status = True
    # tc_status = False
    # tc_status = 'EXCEPTION'
    # tc_status = 'ERROR'
    auto_defects = ""
    data_repository = ""
    tc_junit_object = ""
    # this function is not using tc_junit_object argument
    testcase_driver.check_and_create_defects(tc_status, auto_defects, data_repository, tc_junit_object)


def test_execute_steps():
    """test_execute_steps"""

    # testcase_driver.execute_custom = MagicMock(return_value = False)
    class temp(object):
        """temp"""
        def __init__(self):
            """init"""
            pass

        def remove_html_obj(self):
            """remove html onj"""
            return None

        def execute_hybrid_mode(self):
            """execuet hybrid mode"""
            return True
            # return False
        # def findall(self):
        #    return None

    hybrid_driver_class.HybridDriver = MagicMock(return_value=temp())
    testcase_driver.get_system_list = MagicMock(return_value=[1, 2])
    # data_type="custom"
    # data_type="iterative"
    data_type = "hybrid"
    # data_type="ustom"
    runtype = 'parallel_keywords'
    # runtype = 'sequence_keywords'
    # runtype = 'hululu'
    data_repository = {'wt_datafile': 'hdf'}
    step_list = []
    tc_junit_object = temp()
    iter_ts_sys = ""
    testcase_driver.execute_steps(data_type, runtype, data_repository, step_list, tc_junit_object, iter_ts_sys)


def test_get_testwrapper_file_details():
    """test_get_testcase_details"""
    xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    xml_Utils.nodeExists = MagicMock(return_value=True)
    # xml_Utils.nodeExists = MagicMock(return_value = False)
    testcase_Utils.get_setup_on_error = MagicMock(return_value=None)

    class temp(object):
        """temp"""

        def __init__(self):
            """init"""
            self.resultfile = "resultfile"
            self.resultsdir = "resultfile"
            self.logfile = "resultfile"
            self.logsdir = "resultfile"

        def get_defect_files(self):
            """defect files"""
            return "string"

        def check_get_datatype(self, a):
            """check get datatype"""
            return "string"

        def check_get_runtype(self):
            """check get runtype"""
            return None

    obj = temp()
    execution_files_class.ExecFilesClass = MagicMock(return_value=obj)
    file_Utils.getAbsPath = MagicMock(return_value=None)
    testcase_filepath = "some file path"
    for x in ['ow_testwwrapperfile', 'suite_testwrapper_file', "else"]:
        data_repository = {
            x: 'some dir',
            'wt_datafile': 'data file'
        }
        testcase_driver.get_testwrapper_file_details(testcase_filepath, data_repository)


# def test_execute_testcase():
#    testcase_driver.get_testcase_details = MagicMock(return_value = None)
#    xml_Utils.getChildTextbyParentTag = MagicMock(return_value = "draft")
#    testcase_driver.get_testwrapper_file_details = MagicMock(return_value = ['A', 'B', 'C', 'D'])
#    testcase_driver.check_robot_wrapper_case = MagicMock(return_value = True)
#    common_execution_utils.get_step_list = MagicMock(return_value = [1,2,3,4,5] )
#    os.path.join = MagicMock(return_value = "sfds")
#    testcase_filepath = ""
#    obj = WMongodb()
#    # data_repository = {'wt_name': 'name'}
#    data_repository = {
#            #'wt_junit_object':'junit object',
#            'jobid':'ajshgd',
#            'wt_name': 'name',
#            'wt_filedir': 'sjdf',
#            'wt_testcase_filepath': 'zxc',
#            'wt_data_type': 'dfk',
#            'wt_resultsdir':'asd',
#            'wt_console_logfile': 'ew',
#            'wt_title': 'sdf',
#            'war_file_type': 'Case',
#            'wt_defectsdir': 'jsfdj',
#            'wt_logsdir': 'asd',
#            'wt_datafile': 'ewrew',
#            'wt_resultfile': 'askj',
#            'db_obj':obj,
#            'wt_expResults': 'asdas'
#            }
#    tc_context = ""
#    runtype = ""
#    tc_parallel = ""
#    queue = ""
#    auto_defects = ""
#    suite = ""
#    jiraproj = ""
#    tc_onError_action = ""
#    iter_ts_sys = ""
#    steps_tag = "Steps"
#    testcase_driver.execute_testcase(testcase_filepath, data_repository, tc_context, runtype, tc_parallel, queue, auto_defects, suite, jiraproj, tc_onError_action, iter_ts_sys, steps_tag="Steps")

def test_execute_custom(capsys):
    """test_execute_custom"""
    datatype = 'CUSTOM'
    runtype = 'SEQUENTIAL_KEYWORDS'
    driver = 'some driver'
    data_repository = {
        'suite_exectype': 'iterative',
    }
    step_list = ["obj"]
    testcase_driver.execute_custom(datatype, runtype, driver, data_repository, step_list)
    captured = capsys.readouterr()
    result = captured.out
    assert result == '-I- CUSTOM SEQUENTIAL_KEYWORDS\n-I- Testsuite execute type=iterative but the testcase datatype=custom. All testcases in a iterative testsuite should have datatype=iterative, Hence this testcase will be marked as failure.\n'


def test_check_robot_wrapper_case():
    """test_check_robot_wrapper_case"""

    class temp(object):
        """temp"""
        def __init__(self):
            """init"""
            pass

        def get(self, a):
            """get"""
            return 'plugin_robot_wrapper'

    obj = temp()
    xml_Utils.getElementListWithSpecificXpath = MagicMock(return_value=3 * [obj])
    testcase_filepath = 'file path'
    result = testcase_driver.check_robot_wrapper_case(testcase_filepath)
    assert result is True


def test_main():
    """main"""
    testcase_driver.execute_testcase = MagicMock(return_value=(True, {}))
    result = testcase_driver.main("some path")
    assert result == (True, '2', {})
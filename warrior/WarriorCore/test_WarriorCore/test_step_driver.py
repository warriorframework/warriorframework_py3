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

'''
UT for Step_driver
'''

import os
import sys
from unittest.mock import patch, sentinel
from unittest.mock import MagicMock, Mock

try:
    from warrior.WarriorCore import warrior_cli_driver

#except ModuleNotFoundError as error:
except:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(WARRIORDIR)
    try:
        from warrior.WarriorCore import warrior_cli_driver
    except:
        raise

from warrior.Framework.Utils import testcase_Utils
from xml.etree.ElementTree import Element

sys.modules['warrior.Framework.Utils.data_Utils'] = MagicMock()
sys.modules['warrior.Framework.Utils.testcase_Utils'] = MagicMock()
sys.modules['warrior.Framework.Utils.file_Utils'] = MagicMock()
sys.modules['warrior.Framework.Utils.xml_Utils'] = MagicMock()
sys.modules['warrior.Framework.Utils.config_Utils'] = MagicMock()
sys.modules['warrior.Framework.ClassUtils.ssh_utils_class'] = MagicMock()
sys.modules['warrior.Framework.Utils.print_Utils.print_error'] = MagicMock()
sys.modules['warrior.Framework.Utils.csv_utils'] = MagicMock()
sys.modules['warrior.Framework.OSS.bottle'] = MagicMock()
from warrior.Framework.Utils import data_Utils
from warrior.WarriorCore import step_driver
from warrior.WarriorCore.Classes.argument_datatype_class import ArgumentDatatype
from warrior.Framework.Utils import config_Utils
from warrior.Framework.Utils import xml_Utils
from warrior.Framework.Utils import datetime_utils
from warrior.Framework.Utils import testcase_Utils
from warrior.ProductDrivers import common_driver
from warrior.Framework.Utils import file_Utils
from warrior.WarriorCore import step_driver
from warrior.Framework.OSS import bottle
from warrior.WarriorCore.Classes.war_cli_class import WarriorCliClass


def test_get_arguments():
    ArgumentDatatype.convert_arg_to_datatype = MagicMock(return_value = "sfd")
    data_Utils.sub_from_env_var = MagicMock(return_value = "safd${REPO.")
    Element = MagicMock(return_value = None)
    class tem2:
        def __init__(self):
            self.text = "some text having ${ENV."
        def get(self, a):
            if a== 'value':
                return None
            if a== 'name':
                return "fdj"
    obj2 = tem2()
    class tem1:
        def findall(self, a):
            return 5*[obj2]
    obj1 = tem1()
    Element.find = MagicMock(return_value = obj1)
    obj = Element
    result = step_driver.get_arguments(obj)
    assert result == {'fdj': 'sfd'}
   

def test_send_keyword_to_productdriver1():
    common_driver.main = MagicMock(return_value = "output")
    driver_name = 'common_driver'
    plugin_name = None
    keyword = 'wait_for_timeout'
    data_repository = {'step_num':'1'}
    args_repository = {'timeout': '1'}
    repo_name = 'warrior'
    result = step_driver.send_keyword_to_productdriver(driver_name, plugin_name, keyword, data_repository, args_repository, repo_name)
    assert result == "output"
def test_get_keyword_resultfile1():
    file_Utils.getCustomLogFile = MagicMock(return_value = "expected")
    data_repository ={'wt_kw_results_dir':"some address"}
    system_name = None
    step_num = '1'
    keyword = "some keyword"
    result = step_driver.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
    result == "expected"



def test_get_keyword_resultfile2():
    file_Utils.getCustomLogFile = MagicMock(return_value = "expected")
    data_repository ={'wt_kw_results_dir':"some address"}
    system_name = "some system"
    step_num = '1'
    keyword = "some keyword"
    result = step_driver.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
    result == "expected"




def test_execute_step1():
    testcase_Utils.get_context_from_xmlfile = MagicMock(return_value= "negative")
    testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value= "noimpact")
    testcase_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    testcase_Utils.pKeyword = MagicMock(return_value= None)
    testcase_Utils.update_arguments = MagicMock(return_value= None)
    testcase_Utils.update_kw_resultfile = MagicMock(return_value= None)
    testcase_Utils.update_step_num = MagicMock(return_value= None)
    testcase_Utils.reportKeywordStatus = MagicMock(return_value= None)
    testcase_Utils.pNote_level = MagicMock(return_value= None)
    #xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= "goto")
    xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= "abort_as_error")
    step_driver.get_keyword_resultfile = MagicMock(return_value= "working")
    step_driver.get_step_console_log = MagicMock(return_value= "working")
    config_Utils.set_resultfile = MagicMock(return_value= "working")
    config_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.get_arguments = MagicMock(return_value= {})
    step_driver.send_keyword_to_productdriver = MagicMock(return_value= "oo")
    step_driver.add_keyword_result = MagicMock(return_value= "oo")
    datetime_utils.get_current_timestamp = MagicMock(return_value= None)
    datetime_utils.get_time_delta = MagicMock(return_value= None)
    datetime_utils.get_hms_for_seconds = MagicMock(return_value= None)
    bottle.put = MagicMock(return_value= None)
    queue = bottle()
    class temp:
        def get(self, a):
            return 1
    class temp2:
        def get(self, a):
            #return "fdj"
            return False
        def find(self, a):
            return temp()
    obj = temp2()
    step = obj
    step_num= '1'
    data_repository= {'wt_junit_object':'obj2',
            'wt_filename': 'somefilename',
            'wt_logsdir': 'some add',
            'step_num': '1',
            'wt_driver': 'some driver',
            'wt_plugin': 'some plugin',
            'wt_keyword': 'some keyword',
            'wt_step_impact': 'step impact',
            'wt_step_context': 'context',
            'step-1_status': True,
            'wt_def_on_error_action': "abort_as_error",
            'wt_tc_timestamp': "saj",
            'step-1_exception':'Exception',
            'wt_resultsdir': "result",
            'wt_name': "name",
            'wt_step_type': "step",
            'war_parallel': False,
            'wt_step_description': 'description'}
    system_name= "sys name"
    kw_parallel= True
    queue= queue
    skip_invoked=True
    result = step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel, queue, skip_invoked=True)
    # assert result[0] == False
    assert result[0] == 'ERROR'
    assert result[1] == 'working'
    # assert result[2] == 'impact'
    assert result[2] == 'noimpact'



def test_execute_step2():
    testcase_Utils.get_context_from_xmlfile = MagicMock(return_value= "negative")
    testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value= "impact")
    testcase_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    testcase_Utils.pKeyword = MagicMock(return_value= None)
    testcase_Utils.update_arguments = MagicMock(return_value= None)
    testcase_Utils.update_kw_resultfile = MagicMock(return_value= None)
    testcase_Utils.update_step_num = MagicMock(return_value= None)
    testcase_Utils.reportKeywordStatus = MagicMock(return_value= None)
    testcase_Utils.pNote_level = MagicMock(return_value= None)
    xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= False)
    step_driver.get_keyword_resultfile = MagicMock(return_value= "working")
    step_driver.get_step_console_log = MagicMock(return_value= "working")
    config_Utils.set_resultfile = MagicMock(return_value= "working")
    config_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.get_arguments = MagicMock(return_value= {})
    step_driver.send_keyword_to_productdriver = MagicMock(return_value= "oo")
    step_driver.add_keyword_result = MagicMock(return_value= "oo")
    datetime_utils.get_current_timestamp = MagicMock(return_value= None)
    datetime_utils.get_time_delta = MagicMock(return_value= None)
    datetime_utils.get_hms_for_seconds = MagicMock(return_value= None)
    bottle.put = MagicMock(return_value= None)
    WarriorCliClass.mock = True
    queue = bottle()
    class temp:
        def get(self, a):
            return 1
    class temp2:
        def get(self, a):
            return "fdj"
        def find(self, a):
            return temp()
    obj = temp2()
    step = obj
    step_num= '1'
    data_repository= {'wt_junit_object':'obj2',
            'wt_filename': 'somefilename',
            'wt_logsdir': 'some add',
            'step_num': '1',
            'wt_driver': 'some driver',
            'wt_plugin': 'some plugin',
            'wt_keyword': 'some keyword',
            'wt_step_impact': 'step impact',
            'wt_step_context': 'context',
            'step-1_status': True,
            'wt_def_on_error_action': "goto",
            'wt_tc_timestamp': "saj",
            'wt_resultsdir': "result",
            'wt_name': "name",
            'wt_step_type': "sdf",
            'war_parallel': False,
            'wt_def_on_error_value': None,
            'wt_step_description': 'description'}
    system_name= "sys name"
    kw_parallel= True
    queue= queue
    skip_invoked=True
    result = step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel, queue, skip_invoked=True)
    assert result[0] == 'RAN'
    assert result[1] == 'working'
    assert result[2] == 'impact'



def test_execute_step3():
    testcase_Utils.get_context_from_xmlfile = MagicMock(return_value= "negative")
    testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value= "impact")
    testcase_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    testcase_Utils.pKeyword = MagicMock(return_value= None)
    testcase_Utils.update_arguments = MagicMock(return_value= None)
    testcase_Utils.update_kw_resultfile = MagicMock(return_value= None)
    testcase_Utils.update_step_num = MagicMock(return_value= None)
    testcase_Utils.reportKeywordStatus = MagicMock(return_value= None)
    testcase_Utils.pNote_level = MagicMock(return_value= None)
    xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= False)
    step_driver.get_keyword_resultfile = MagicMock(return_value= "working")
    step_driver.get_step_console_log = MagicMock(return_value= "working")
    config_Utils.set_resultfile = MagicMock(return_value= "working")
    config_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.get_arguments = MagicMock(return_value= {})
    step_driver.send_keyword_to_productdriver = MagicMock(return_value= "oo")
    step_driver.add_keyword_result = MagicMock(return_value= "oo")
    datetime_utils.get_current_timestamp = MagicMock(return_value= None)
    datetime_utils.get_time_delta = MagicMock(return_value= None)
    datetime_utils.get_hms_for_seconds = MagicMock(return_value= None)
    bottle.put = MagicMock(return_value= None)
    WarriorCliClass.mock = False
    queue = bottle()
    class temp:
        def get(self, a):
            return 1
    class temp2:
        def get(self, a):
            return "fdj"
        def find(self, a):
            return temp()
    obj = temp2()
    step = obj
    step_num= '1'
    data_repository= {'wt_junit_object':'obj2',
            'wt_filename': 'somefilename',
            'wt_logsdir': 'some add',
            'step_num': '1',
            'wt_driver': 'some driver',
            'wt_plugin': 'some plugin',
            'wt_keyword': 'some keyword',
            'wt_step_impact': 'step impact',
            'wt_step_context': 'context',
            'step-1_status': "skip",
            #1 'step-1_status': True,
            'wt_def_on_error_action': "abort_as_error",
            'wt_tc_timestamp': "saj",
            'wt_resultsdir': "result",
            'wt_name': "name",
            'wt_step_type': "sdf",
            'war_parallel': False,
            'wt_def_on_error_value': None,
            'wt_step_description': 'description'}
    system_name= "sys name"
    kw_parallel= True
    queue= queue
    skip_invoked=True
    result = step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel, queue, skip_invoked=True)
    #1 assert result[0] == 'ERROR'
    assert result[0] == None
    assert result[1] == 'working'
    assert result[2] == 'impact'


def test_execute_step4():
    testcase_Utils.get_context_from_xmlfile = MagicMock(return_value= "negative")
    testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value= "impact")
    testcase_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    testcase_Utils.pKeyword = MagicMock(return_value= None)
    testcase_Utils.update_arguments = MagicMock(return_value= None)
    testcase_Utils.update_kw_resultfile = MagicMock(return_value= None)
    testcase_Utils.update_step_num = MagicMock(return_value= None)
    testcase_Utils.reportKeywordStatus = MagicMock(return_value= None)
    testcase_Utils.pNote_level = MagicMock(return_value= None)
    xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= "goto")
    step_driver.get_keyword_resultfile = MagicMock(return_value= "working")
    config_Utils.set_resultfile = MagicMock(return_value= "working")
    config_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.get_arguments = MagicMock(return_value= "oo")
    step_driver.send_keyword_to_productdriver = MagicMock(return_value= "oo")
    step_driver.add_keyword_result = MagicMock(return_value= "oo")
    datetime_utils.get_current_timestamp = MagicMock(return_value= None)
    datetime_utils.get_time_delta = MagicMock(return_value= None)
    datetime_utils.get_hms_for_seconds = MagicMock(return_value= None)
    class temp:
        def get(self, a):
            return 1
    class temp2:
        def output_junit(self, a, print_summary):
            return None
        def get(self, a):
            return "fdj"
        def find(self, a):
            return temp()
    obj = temp2()
    step = obj
    step_num= '1'
    data_repository= {'wt_junit_object':obj,
            'wt_filename': 'somefilename',
            'wt_logsdir': 'some add',
            'step_num': '1',
            'wt_driver': 'some driver',
            'wt_plugin': 'some plugin',
            'wt_keyword': 'some keyword',
            'wt_step_impact': 'step impact',
            'wt_step_context': 'context',
            'step-1_status': "asdwasdsad",
            'wt_def_on_error_action': "bla",
            'wt_tc_timestamp': "saj",
            'wt_name': "name",
            'wt_step_type': "sdf",
            'war_parallel': False,
            'wt_results_execdir': "suit dir",
            'wp_results_execdir': "project dir",
            # 'wt_results_execdir':'suite directory',
            'wt_resultsdir': "Case directory",
            # 'war_file_type': 'Case',
            # 'war_file_type': 'Suite',
            'war_file_type': 'Project',
            'wt_step_description': 'description'}
    system_name= None
    kw_parallel= False
    queue= None
    skip_invoked=True
    result = step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel, queue, skip_invoked=True)
    assert result[0] == 'asdwasdsad'
    assert result[1] == 'working'
    assert result[2] == 'impact'

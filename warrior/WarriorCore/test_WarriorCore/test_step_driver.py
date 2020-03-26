import sys
# sys.path.append('/home/test/workingdirectory/warriorframework_py3')
from unittest.mock import patch, sentinel
from unittest.mock import MagicMock, Mock

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class.ArgumentDatatype'] = MagicMock(return_value = None)
sys.modules['warrior.Framework.OSS.bottle'] = MagicMock()
sys.modules['warrior.WarriorCore.kw_driver'] = MagicMock()
sys.modules['warrior.WarriorCore.defects_driver'] = MagicMock()

from warrior.WarriorCore import step_driver

def test_get_arguments():
    step_driver.ArgumentDatatype.convert_arg_to_datatype = MagicMock(return_value = "sfd")
    step_driver.Utils.data_Utils.sub_from_env_var = MagicMock(return_value = "safd${REPO.")
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
    del step_driver.ArgumentDatatype.convert_arg_to_datatype
    del step_driver.Utils.data_Utils.sub_from_env_var
   

def test_send_keyword_to_productdriver1():
    # from warrior.WarriorCore import step_driver
    from warrior.ProductDrivers import common_driver
    common_driver.main = MagicMock(return_value = 'output')
    driver_name = 'common_driver'
    plugin_name = None
    keyword = 'wait_for_timeout'
    data_repository = {'step_num':'1'}
    args_repository = {'timeout': '1'}
    repo_name = 'warrior'
    result = step_driver.send_keyword_to_productdriver(driver_name, plugin_name, keyword, data_repository, args_repository, repo_name)
    del common_driver.main


def test_get_keyword_resultfile1():
    # from warrior.WarriorCore import step_driver
    step_driver.Utils.file_Utils.getCustomLogFile = MagicMock(return_value = "expected")
    data_repository ={'wt_kw_results_dir':"some address"}
    system_name = None
    step_num = '1'
    keyword = "some keyword"
    result = step_driver.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
    result == "expected"
    del step_driver.Utils.file_Utils.getCustomLogFile



def test_get_keyword_resultfile2():
    # from warrior.WarriorCore import step_driver
    step_driver.Utils.file_Utils.getCustomLogFile = MagicMock(return_value = "expected")
    data_repository ={'wt_kw_results_dir':"some address"}
    system_name = "some system"
    step_num = '1'
    keyword = "some keyword"
    result = step_driver.get_keyword_resultfile(data_repository, system_name, step_num, keyword)
    result == "expected"
    del step_driver.Utils.file_Utils.getCustomLogFile




def test_execute_step1():
    # from warrior.WarriorCore import step_driver
    from warrior.Framework.OSS import bottle
    step_driver.Utils.testcase_Utils.get_context_from_xmlfile = MagicMock(return_value= "negative")
    step_driver.Utils.testcase_Utils.get_impact_from_xmlfile = MagicMock(return_value= "noimpact")
    step_driver.Utils.testcase_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.Utils.testcase_Utils.pKeyword = MagicMock(return_value= None)
    step_driver.Utils.testcase_Utils.update_arguments = MagicMock(return_value= None)
    step_driver.Utils.testcase_Utils.update_kw_resultfile = MagicMock(return_value= None)
    step_driver.Utils.testcase_Utils.update_step_num = MagicMock(return_value= None)
    step_driver.Utils.testcase_Utils.reportKeywordStatus = MagicMock(return_value= None)
    step_driver.Utils.testcase_Utils.pNote_level = MagicMock(return_value= None)
    step_driver.Utils.xml_Utils.get_attributevalue_from_directchildnode = MagicMock(return_value= "abort_as_error")
    step_driver.get_keyword_resultfile = MagicMock(return_value= "working")
    step_driver.get_step_console_log = MagicMock(return_value= "working")
    step_driver.Utils.config_Utils.set_resultfile = MagicMock(return_value= "working")
    step_driver.Utils.config_Utils.get_description_from_xmlfile = MagicMock(return_value= "working")
    step_driver.get_arguments = MagicMock(return_value= {})
    step_driver.send_keyword_to_productdriver = MagicMock(return_value= "oo")
    step_driver.add_keyword_result = MagicMock(return_value= "oo")
    step_driver.Utils.datetime_utils.get_current_timestamp = MagicMock(return_value= None)
    step_driver.Utils.datetime_utils.get_time_delta = MagicMock(return_value= None)
    step_driver.Utils.datetime_utils.get_hms_for_seconds = MagicMock(return_value= None)
    bottle.put = MagicMock(return_value= None)
    queue = bottle()
    class temp:
        def get(self, a):
            return 1
    class temp2:
        def get(self, a):
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
    skip_invoked=True
    result = step_driver.execute_step(step, step_num, data_repository, system_name, kw_parallel, queue, skip_invoked=True)

    del step_driver.Utils.testcase_Utils.get_context_from_xmlfile
    del step_driver.Utils.testcase_Utils.get_impact_from_xmlfile
    del step_driver.Utils.testcase_Utils.get_description_from_xmlfile
    del step_driver.Utils.testcase_Utils.pKeyword
    del step_driver.Utils.testcase_Utils.update_arguments
    del step_driver.Utils.testcase_Utils.update_kw_resultfile
    del step_driver.Utils.testcase_Utils.update_step_num
    del step_driver.Utils.testcase_Utils.reportKeywordStatus
    del step_driver.Utils.testcase_Utils.pNote_level
    del step_driver.Utils.xml_Utils.get_attributevalue_from_directchildnode
    del step_driver.get_keyword_resultfile
    del step_driver.get_step_console_log
    del step_driver.Utils.config_Utils.set_resultfile
    del step_driver.Utils.config_Utils.get_description_from_xmlfile
    del step_driver.get_arguments
    del step_driver.send_keyword_to_productdriver
    del step_driver.add_keyword_result
    del step_driver.Utils.datetime_utils.get_current_timestamp
    del step_driver.Utils.datetime_utils.get_time_delta
    del step_driver.Utils.datetime_utils.get_hms_for_seconds
    del bottle.put
    del sys.modules['warrior.Framework.OSS.bottle']



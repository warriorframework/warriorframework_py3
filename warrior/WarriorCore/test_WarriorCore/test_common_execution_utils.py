import sys
from unittest.mock import MagicMock

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

sys.modules['warrior.WarriorCore.defects_driver'] = MagicMock()
sys.modules['warrior.WarriorCore.kw_driver'] = MagicMock()
from warrior.WarriorCore import common_execution_utils
warrior.Framework.Utils.xml_Utils = MagicMock()
import json

# sys.modules['warrior.Framework.Utils'] = MagicMock()
from warrior.Framework.Utils import data_Utils
def test_append_step_list():
    import copy
    class temp1():
        def set(self, a, b):
            return None
    class temp():
        def find(self, a):
            return temp1()
    copy.deepcopy= MagicMock(return_value = temp())
    step_list = []
    step = ""
    value = 2
    go_next = ""
    mode = ""
    tag = ""
    result = common_execution_utils.append_step_list(step_list, step, value, go_next, mode, tag)
    for x in result:
        assert x.__class__.__name__ == 'temp'
    del copy.deepcopy, copy



def test_get_retry_from_xmlfile1():
    common_execution_utils.print_warning = MagicMock(return_value = None)
    class temp1():
        def get(self, a):
            if a == 'type':
                return "if"
            if a == 'Condition':
                return "asjkd"
            if a == 'Condvalue':
                return "if"
            if a == 'count':
                return "if"
            if a == 'interval':
                return "if"
    class temp():
        def find(self, a):
            return temp1()
    common_execution_utils.get_retry_from_xmlfile(temp())


def test_get_retry_from_xmlfile2():
    common_execution_utils.print_warning = MagicMock(return_value = None)
    class temp1():
        def get(self, a):
            if a == 'type':
                return "if"
            if a == 'Condition':
                return None
            if a == 'Condvalue':
                return "if"
            if a == 'count':
                return "if"
            if a == 'interval':
                return "if"
    class temp():
        def find(self, a):
            return temp1()
    common_execution_utils.get_retry_from_xmlfile(temp())



def test_get_retry_from_xmlfile3():
    common_execution_utils.print_warning = MagicMock(return_value = None)
    class temp1():
        def get(self, a):
            return "retry_tag"
    class temp():
        def find(self, a):
            return temp1()
    common_execution_utils.get_retry_from_xmlfile(temp())


def test_get_runmode_from_xmlfile1():
    from warrior.WarriorCore import common_execution_utils
    common_execution_utils.print_warning = MagicMock(return_value = None)
    class temp1():
        def get(self, a):
            if a== 'type':
                return "RUF"
            if a== 'value':
                return 0.5
            if a== 'runmode_timer':
                return None
    
    class temp():
        def find(self, a):
            return temp1()
    element = temp()
    result = common_execution_utils.get_runmode_from_xmlfile(element)

def test_get_runmode_from_xmlfile2():
    from warrior.WarriorCore import common_execution_utils
    class temp1():
        def get(self, a):
            if a== 'type':
                return "sd"
            if a== 'value':
                return "rt_value"
            if a== 'runmode_timer':
                return '1'
    
    class temp():
        def find(self, a):
            return temp1()
    element = temp()
    result = common_execution_utils.get_runmode_from_xmlfile(element)


def test_get_step_list1():
    class temp1():
        def __init__(self):
            self.tag = 'Loop'
        def findall(self, a):
            return 'str'
        def get(self,a):
            if a== "id":
                return "loop count"
            if a== "file":
                return "json_file"
            return None
    class temp():
        def __init__(self):
            self.tag = 'just tag'
        def find(self, a):
            #return None
            return 5*[temp1()]
    common_execution_utils.print_info = MagicMock(return_value = 'sucess')
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = temp())
    data_Utils.sub_from_env_var = MagicMock(return_value = "json_file")
    data_Utils.update_datarepository = MagicMock(return_value = {})
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = (None, None, None))
    common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value = (None, None, None, None, None ))
    common_execution_utils.get_object_from_datarepository = MagicMock(return_value = "testcase file")
    common_execution_utils.update_datarepository = MagicMock(return_value = None)
    json.load = MagicMock(return_value = "testcase file")
    filepath = "some file path"
    step_tag = 'some tag'
    sub_step_tag = 'some sub tag'
    result = common_execution_utils.get_step_list(filepath, step_tag, sub_step_tag)

def test_get_step_list2():
    class temp1():
        def __init__(self):
            self.tag = 'some sub tag'
        def find(self, a):
            return 'none'
        def remove(self, a):
            return 'remove'
    class temp():
        def __init__(self):
            self.tag = 'just tag'
        def find(self, a):
            return 5*[temp1()]
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = temp())
    common_execution_utils.append_step_list = MagicMock(return_value = [1,2,3])
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = ('None', 5, None))
    common_execution_utils.get_retry_from_xmlfile = MagicMock(return_value = (5, None, None, 5, None ))
    common_execution_utils.get_object_from_datarepository = MagicMock(return_value = "testcase file")
    filepath = "some file path"
    step_tag = 'some tag'
    sub_step_tag = 'some sub tag'
    result = common_execution_utils.get_step_list(filepath, step_tag, sub_step_tag)
    #del common_execution_utils.get_runmode_from_xmlfile



def test_compute_runmode_status1():
    class temp1():
        def find(self):
            return 'last_instance'
        def set(self, a, b):
            return True
        def get(self, a):
            return True
    class temp():
        def find(self, a):
            return temp1()
    runmode = 'RMT'
    global_xml = temp()
    for x in ['FALSE','RAN','ERROR', 'else']:
        global_status_list = [x]
        common_execution_utils.compute_runmode_status(global_status_list, runmode, global_xml)



def test_compute_runmode_status2():
    class temp1():
        def set(self, a, b):
            return True
        def get(self, a):
            #return 'expected'
            return 'last_instance'
    class temp():
        def find(self, a):
            return temp1()
    global_status_list = [True, True]
    for x in ['rup', 'ruf']:
        runmode = x
        global_xml = temp()
        common_execution_utils.compute_runmode_status(global_status_list, runmode, global_xml)

def test_compute_runmode_status3():
    class temp1():
        def set(self, a, b):
            return True
        def get(self, a):
            return 'expected'
            return 'last_instance'
    class temp():
        def find(self, a):
            return temp1()
    global_status_list = [True, True]
    for x in ['rup', 'ruf']:
        runmode = x
        global_xml = temp()
        common_execution_utils.compute_runmode_status(global_status_list, runmode, global_xml)


def test_compute_status1():
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = (None, None, None))
    element = ''
    status_list = []
    impact_list = []
    status = ''
    impact = ''
    common_execution_utils.compute_status(element, status_list, impact_list, status, impact)
    del common_execution_utils.get_runmode_from_xmlfile



def test_compute_status2():
    class temp1():
        def get(self, a):
            return None
        def set(self, a, b):
            return None
        
    class temp():
        def find(self, a):
            return temp1()

    common_execution_utils.print_warning = MagicMock(return_value = None)
    for x in ['rmt', 'rup', 'ruf']:
        common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = (x , None, None))
        element = temp()
        status_list = []
        impact_list = []
        status = ''
        impact = ''
        common_execution_utils.compute_status(element, status_list, impact_list, status, impact)
        del common_execution_utils.get_runmode_from_xmlfile



def test_compute_status3():
    class temp1():
        def get(self, a):
            return 'last_instance'
        def set(self, a, b):
            return None
        
    class temp():
        def find(self, a):
            return temp1()

    common_execution_utils.print_warning = MagicMock(return_value = None)
    for x in ['rmt', 'rup', 'ruf']:
        common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = (x , None, None))
        element = temp()
        status_list = []
        impact_list = []
        status = ''
        impact = ''
        common_execution_utils.compute_status(element, status_list, impact_list, status, impact)
        del common_execution_utils.get_runmode_from_xmlfile


def test_compute_status4():
    class temp1():
        def get(self, a):
            return 'expected'
        def set(self, a, b):
            return None
        
    class temp():
        def find(self, a):
            return temp1()

    common_execution_utils.print_warning = MagicMock(return_value = None)
    for x in ['rmt', 'rup', 'ruf']:
        common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value = (x , None, None))
        element = temp()
        status_list = []
        impact_list = []
        status = ''
        impact = ''
        common_execution_utils.compute_status(element, status_list, impact_list, status, impact)
        del common_execution_utils.get_runmode_from_xmlfile

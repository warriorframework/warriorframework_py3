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

sys.modules['warrior.WarriorCore.Classes.war_cli_class'] = MagicMock()

from warrior.WarriorCore import onerror_driver

warrior.Framework.Utils = MagicMock()
warrior.Framework.Utils.print_Utils = MagicMock()

def test_execute_and_resume():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """

    action = 'some value'
    value = [1,2]
    error_handle = {}
    onerror_driver.execute_and_resume(action, value, error_handle)


def test_abortAsError():
    """returns ABORT_AS_ERROR for on_error action = abort_as_error """
    action = 'some value'
    value = [1,2]
    error_handle = {}
    onerror_driver.abortAsError(action, value, error_handle)    

def test_abort():
    """returns ABORT for on_error action = abort """
    action = 'some value'
    value = [1,2]
    error_handle = {}

    onerror_driver.abort(action, value, error_handle)

def test_goto():
    """returns goto_step_num for on_error action = goto """
    action = 'some value'
    value = [1,2]
    error_handle = {}

    onerror_driver.goto(action, value, error_handle)

def test_next():
    """returns 'NEXT' for on_error action = next """
    action = 'some value'
    value = [1,2]
    error_handle = {}

    onerror_driver.next(action, value, error_handle, skip_invoked=True)

def test_get_failure_results1():
    """ Returns the appropriate values based on the onError actions for failing steps.

    Arguments:
    1. error_repository    = (dict) dictionary containing the onError action, values
    """

    error_repository = {'action':'NEXT'}

    onerror_driver.get_failure_results(error_repository)

def test_get_failure_results2():
    """ Returns the appropriate values based on the onError actions for failing steps.

    Arguments:
    1. error_repository    = (dict) dictionary containing the onError action, values
    """

    error_repository = {'action':'GOTO', 'value':1}

    onerror_driver.get_failure_results(error_repository)

def test_get_failure_results3():
    """ Returns the appropriate values based on the onError actions for failing steps.

    Arguments:
    1. error_repository    = (dict) dictionary containing the onError action, values
    """

    error_repository = {'action':'ABORT'}

    onerror_driver.get_failure_results(error_repository)


def test_getErrorHandlingParameters():
    """Takes a xml element at input and returns the values for on_error action , value
    If no value is available in the node then returns the default values """

    def_on_error_action = ''
    def_on_error_value = ''
    exec_type = 'yes'

    class node(object):
        """docstring for node"""
        def __init__(self, arg):
            super(node, self).__init__()
            self.arg = arg

        def find(self):
            attrib = 'some value'
            # return 'yes'

   
    # if exec_type:
    #     exec_node = node.find('Execute')
    #     def_on_error_action = 'NEXT'
    #     def_on_error_value = ''
    #     ex_rule_param = exec_node.find('Rule').attrib
    #     action = ex_rule_param['Else']
    #     if ex_rule_param['Else'].upper() == 'GOTO':
    #         value = ex_rule_param['Elsevalue']

    onerror_driver.getErrorHandlingParameters(node, def_on_error_action, def_on_error_value,\
    	exec_type, current_step_number=None)
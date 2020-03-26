import os
import sys
from unittest.mock import MagicMock

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    # import warrior
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

sys.modules['warrior.WarriorCore.Classes.argument_datatype_class'] = MagicMock(return_value=None)
from warrior.WarriorCore import exec_type_driver

warrior.Framework.Utils.data_Utils = MagicMock(return_value=None)
warrior.Framework.Utils.print_Utils = MagicMock(return_value=None)
warrior.Framework.Utils.testcase_Utils = MagicMock(return_value=None)

def test_math_decision():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.get_object_from_datarepository = MagicMock( return_value= 13)
    exec_condition = None
    exec_cond_var = 12
    for operator in ['ge', 'g']:
        class temp():
            def lower(self):
                return operator
        operator = temp()
        result = exec_type_driver.math_decision(exec_condition, exec_cond_var, operator)

def test_logical_decision1():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.get_object_from_datarepository = MagicMock( return_value= 13)
    exec_condition = 1
    exec_cond_var = 12
    for operator in [
            'eq',
            'ne',
            ]:
        result = exec_type_driver.logical_decision(exec_condition, exec_cond_var, operator)


def test_logical_decision2():
    from warrior.WarriorCore import exec_type_driver
    exec_type_driver.get_object_from_datarepository = MagicMock( return_value= '13')
    exec_type_driver.pNote = MagicMock( return_value= None)
    exec_condition = 1
    exec_cond_var = 12
    for operator in [
            'eq',
            ]:
        result = exec_type_driver.logical_decision(exec_condition, exec_cond_var, operator)


# def test_logical_decision3():
    from warrior.WarriorCore import exec_type_driver
    exec_type_driver.get_object_from_datarepository = MagicMock( return_value= 13)
    exec_type_driver.pNote = MagicMock( return_value= None)
    exec_condition = '1'
    exec_cond_var = 12
    for operator in [
            'gt',
            ]:
        result = exec_type_driver.logical_decision(exec_condition, exec_cond_var, operator)


def test_int_split():
    # from warrior.WarriorCore import exec_type_driver
    expression_str = '2423 234 32 423 4 shs sdf sdf4'
    result = exec_type_driver.int_split(expression_str)

def test_simple_exp_parser1():
    # from warrior.WarriorCore import exec_type_driver
    expression_str = ''
    rules = {}
    try:
        result = exec_type_driver.simple_exp_parser(expression_str, rules)
    except Exception:
        pass

def test_simple_exp_parser2():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.rule_parser = MagicMock(return_value = "status")
    expression_str = '1'
    rules = {1: 'Pass'}
    result = exec_type_driver.simple_exp_parser(expression_str, rules)

def test_simple_exp_parser3():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.rule_parser = MagicMock(return_value = True)
    exec_type_driver.int_split = MagicMock(return_value = ["or", "and", "else", "or", "and", "else", "else"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    try:
        exec_type_driver.simple_exp_parser(expression_str, rules)
    except Exception:
        pass
    del exec_type_driver.int_split

def test_special_exp_parser1():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.int_split = MagicMock(return_value = ["or", "and", 'and', 'and', "and"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    status_first = True
    status_last = False
    exec_type_driver.special_exp_parser(expression_str, rules, status_first, status_last)
    del exec_type_driver.int_split

def test_special_exp_parser2():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.int_split = MagicMock(return_value = ["or", "or", 'or', 'or', "or"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    status_first = True
    status_last = False
    exec_type_driver.special_exp_parser(expression_str, rules, status_first, status_last)
    del exec_type_driver.int_split

def test_special_exp_parser3():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.int_split = MagicMock(return_value = ["or"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    status_first = True
    status_last = False
    try:
        exec_type_driver.special_exp_parser(expression_str, rules, status_first, status_last)
    except Exception:
        pass
    del exec_type_driver.int_split

def test_special_exp_parser4():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.int_split = MagicMock(return_value = ["else", "else", "else", "else", "else", "else"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    status_first = True
    status_last = False
    try:
        exec_type_driver.special_exp_parser(expression_str, rules, status_first, status_last)
    except Exception:
        pass
    del exec_type_driver.int_split

def test_special_exp_parser5():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.int_split = MagicMock(return_value = ["or", "or", 'or', 'else', "else"])
    expression_str = 'and'
    rules = {'or': 'Pass', 'and': 'Pass', 'else': 'Pass'}
    status_first = True
    status_last = False
    try:
        exec_type_driver.special_exp_parser(expression_str, rules, status_first, status_last)
    except Exception:
        pass
    del exec_type_driver.int_split

def test_expression_split():
    # from warrior.WarriorCore import exec_type_driver
    src = '(1)'
    result = exec_type_driver.expression_split(src)

def test_expression_parser1():
    # from warrior.WarriorCore import exec_type_driver
    src = '(1'
    rules = None
    try:
        result = exec_type_driver.expression_parser(src, rules)
    except Exception:
        pass

def test_expression_parser2():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    src = '1'
    rules = None
    result = exec_type_driver.expression_parser(src, rules)

def test_expression_parser3():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [[1,1]])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    exec_type_driver.special_exp_parser = MagicMock(return_value = True)
    src = '1'
    rules = None
    result = exec_type_driver.expression_parser(src, rules)

def test_expression_parser4():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [[1,-1], [4,1]])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    exec_type_driver.special_exp_parser = MagicMock(return_value = True)
    rules = None
    for x in ['and', 'or']:
        src = x
        result = exec_type_driver.expression_parser(src, rules)

def test_expression_parser5():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [[1,-1], [4,1]])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    exec_type_driver.special_exp_parser = MagicMock(return_value = True)
    rules = None
    src = '1'
    result = exec_type_driver.expression_parser(src, rules)

def test_expression_parser6():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [[1,-1], [4,1]])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    exec_type_driver.special_exp_parser = MagicMock(return_value = True)
    src = 'else'
    rules = None
    try:
        exec_type_driver.expression_parser(src, rules)
    except Exception:
        pass

def test_expression_parser7():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_split = MagicMock(return_value = [[1,1], [-1,4]])
    exec_type_driver.simple_exp_parser = MagicMock(return_value = True)
    exec_type_driver.special_exp_parser = MagicMock(return_value = True)
    src = 'else'
    rules = None
    exec_type_driver.expression_parser(src, rules)

def test_decision_maker():
    # from warrior.WarriorCore import exec_type_driver
    exec_type_driver.expression_parser = MagicMock(return_value = True)
    class temp():
        def get(self, a, b= None):
            if a == 'ExecType':
                return 'if not'
            if a == 'Expression':
                return ''
            if a == 'Else':
                return 'else'
            if a == 'Elsevalue':
                return 'elsevalue'
        def findall(self, a):
            return ['findall']
    exec_node = temp()
    result = exec_type_driver.decision_maker(exec_node)

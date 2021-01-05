import sys
import os
from unittest.mock import MagicMock
from os.path import abspath, dirname
import re
from configobj import ConfigObj
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior
from warrior.Framework.Utils import data_Utils


r_dict = {'file': '{FILENAME}'}
u_dict = {}
variable_dict = {'FILENAME': 'bc.DBS'}
user_dict = {'FILENAME': 'def.DBS'}
v_dict = {'FILENA': 'abc.DBS'}
v = {}
data_repository = {'system_name': 'confD'}

def test_get_the_cred_dict():
   assert data_Utils.get_connection('CREDENTIALS', 'data.cfg', 'device1') == (True, {'ip': '167.254.218.113', 'nc_port': '16029', 'username': 'fujitsu', 'password': '1finity', 'hostkey_verify': 'False'})

def test_get_map_section():
   assert  data_Utils.get_connection('MAP', 'data.cfg') == (True, {'MATCH_STRING': '\nNOT\nComplete to\n'})

def test_checkwith_wrong_section():
   assert  data_Utils.get_connection('sample', 'data.cfg') == (False, None)

def test_checkwith_wrong_file():
   assert data_Utils.get_connection('MAP', 'nothing') == (False, None)

def test_get_the_cred_section():
   assert  data_Utils.get_connection('CREDENTIALS', 'test_data.cfg') == (True, {'DEFAULT': 'device1', 'device1': {'ip': '167.254.218.113', 'nc_port': '16029', 'username': 'fujitsu', 'password': '1finity', 'hostkey_verify': 'False'}, 'device2': {'ip': '167.254.218.113', 'nc_port': '16029', 'username': 'fujitsu', 'password': '1finity', 'hostkey_verify': 'False'}})

def test_with_different_section():
    assert data_Utils.get_connection('Map', 'test_data.cfg') == (False, None)

def test_with_lowercase_section():
    assert  data_Utils.get_connection('map', 'test_data.cfg') == (False, None)

def test_with_no_file():
    assert  data_Utils.get_connection('MAP', 'none') == (False, None)

# unit testcases for replace_var method

def test_with_different_key_value():
    assert data_Utils.replace_var(r_dict, u_dict, v_dict) == (False, {'file': '{FILENAME}'})

def test_with_no_substitution():
    assert data_Utils.replace_var(r_dict, {}, {}) == (False, {'file': '{FILENAME}'})

def test_with_correct_substitution():
    assert data_Utils.replace_var(r_dict, user_dict, v) == (True, {'file': 'def.DBS'})

def test_the_priority_of_substution():
    assert data_Utils.replace_var(r_dict, user_dict, variable_dict) == (True, {'file': 'def.DBS'})

def test_checking_other_options_for_substitution():
     assert data_Utils.replace_var(r_dict, u_dict, variable_dict) == (True, {'file': 'def.DBS'})


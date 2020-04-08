"""
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
"""

import sys
import os
from unittest.mock import MagicMock
from os.path import abspath, dirname
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    print(WARRIORDIR)
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.WarriorCore import common_execution_utils
import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et


def test_append_step_list():
    '''test_append_step_list'''
    import os
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps  = root.find("Steps")
    sstep = steps[0]
    value = 4
    go_next = 5
    mode = 'runmode'
    tag = 'value'

    new_step_list_12 = common_execution_utils.append_step_list(step_list=[], step=sstep,\
     value=value, go_next=go_next, mode=mode, tag=tag)
    assert len(new_step_list_12) == 4

# def test_get_step_list_for_no_steps():
#     file_path = os.path.join(os.path.split(__file__)[0], "new_sample.xml")
#     common_execution_utils.get_step_list(filepath=file_path,  step_tag="", sub_step_tag="step")

def test_get_step_list_for_steps():
    '''test_get_step_list_for_steps'''

    file_path = os.path.join(os.path.split(__file__)[0], "sample.xml")
    common_execution_utils.get_step_list(filepath=file_path, step_tag="Steps", sub_step_tag="step")

def test_get_step_list_for_loop_tag_without_loop_id():
    '''test_get_step_list_for_loop_tag_without_loop_id'''

    file_path = os.path.join(os.path.split(__file__)[0], "test_loop_datatype_without_loop_id.xml")
    #common_execution_utils.get_object_from_datarepository = MagicMock(return_value=file_path)
    status = common_execution_utils.get_step_list(filepath=file_path, step_tag="Steps",\
     sub_step_tag="step")
    assert status == False

def test_get_step_list_for_loop_tag_without_file_tag():
    '''test_get_step_list_for_loop_tag_without_file_tag'''

    file_path = os.path.join(os.path.split(__file__)[0], "test_loop_datatype_without_file_tag.xml")
    #common_execution_utils.get_object_from_datarepository = MagicMock(return_value=file_path)
    status = common_execution_utils.get_step_list(filepath=file_path,  step_tag="Steps",\
     sub_step_tag="step")
    assert status == False

def test_get_step_list_for_loop_tag_with_invalid_json():
    '''test_get_step_list_for_loop_tag_with_invalid_json'''

    file_path = os.path.join(os.path.split(__file__)[0], "test_loop_datatype.xml")
    json_file_path = os.path.join(os.path.split(__file__)[0], "wrong_1j_loop_datatype.json")
    common_execution_utils.get_object_from_datarepository = MagicMock(return_value=file_path)
    common_execution_utils.getAbsPath = MagicMock(return_value=json_file_path)
    common_execution_utils.get_step_list(filepath=file_path,  step_tag="Steps", sub_step_tag="step" )

    del common_execution_utils.get_object_from_datarepository
    del common_execution_utils.getAbsPath

def test_get_step_list_for_loop_tag_with_json_file_not_found():
    '''test_get_step_list_for_loop_tag_with_json_file_not_found'''

    file_path = os.path.join(os.path.split(__file__)[0], "test_loop_datatype.xml")
    json_file_path = os.path.join(os.path.split(__file__)[0], "wrong_1j_loop_datatype2.json")
    # common_execution_utils.update_datarepository = MagicMock(return_value={})
    common_execution_utils.get_object_from_datarepository = MagicMock(return_value=file_path)
    common_execution_utils.getAbsPath = MagicMock(return_value=json_file_path)

    common_execution_utils.get_step_list(filepath=file_path,  step_tag="Steps", sub_step_tag="step" )
    del common_execution_utils.get_object_from_datarepository
    del common_execution_utils.getAbsPath


# def test_get_step_list_for_loop_tag():
#     #data_Utils.update_datarepository = MagicMock(return_value={})

#     file_path = os.path.join(os.path.split(__file__)[0], "test_loop_datatype.xml")
#     json_file_path = os.path.join(os.path.split(__file__)[0], "1j_loop_datatype.json")
#     common_execution_utils.update_datarepository = MagicMock(return_value={})
#     common_execution_utils.get_object_from_datarepository = MagicMock(return_value=file_path)
#     common_execution_utils.getAbsPath = MagicMock(return_value=json_file_path)
#     common_execution_utils.getAbsPath = MagicMock(return_value=json_file_path)
#     common_execution_utils.get_step_list(filepath=file_path,  step_tag="Steps", sub_step_tag="step", randomize=True )

def test_get_runmode_from_xmlfile():
    '''test_get_runmode_from_xmlfile'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[0]
    value = 4
    go_next = 5
    mode = 'runmode'
    tag = 'value'

    common_execution_utils.get_runmode_from_xmlfile(element=sstep)

def test_get_runmode_from_xmlfile_no_runmode_timer():
    '''test_get_runmode_from_xmlfile_no_runmode_timer'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[1]
    common_execution_utils.get_runmode_from_xmlfile(element=sstep)

def test_get_runmode_from_xmlfile_invalid_runmode_timer():
    '''test_get_runmode_from_xmlfile_invalid_runmode_timer'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[2]
    common_execution_utils.get_runmode_from_xmlfile(element=sstep)

def test_get_runmode_from_xmlfile_invalid_runmode_type():
    '''test_get_runmode_from_xmlfile_invalid_runmode_type'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[3]
    status = common_execution_utils.get_runmode_from_xmlfile(element=sstep)
    assert status[0] == None

def test_get_runmode_from_xmlfile_runmode_value_as_zero():
    '''test_get_runmode_from_xmlfile_runmode_value_as_zero'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[4]
    status = common_execution_utils.get_runmode_from_xmlfile(element=sstep)
    assert status[0] == "RMT"

def test_get_runmode_from_xmlfile_invalid_runmode_value():
    '''test_get_runmode_from_xmlfile_invalid_runmode_value'''
    tree = ET.parse(os.path.join(os.path.split(__file__)[0], "sample.xml"))
    # get root element
    root = tree.getroot()
    # getting steps
    steps = root.find("Steps")
    sstep = steps[5]
    status = common_execution_utils.get_runmode_from_xmlfile(element=sstep)
    #assert status[0] == RMT
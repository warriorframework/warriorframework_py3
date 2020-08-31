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
import shutil
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from os.path import abspath, dirname
from unittest import TestCase
import multiprocessing
try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    WARRIORDIR = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(WARRIORDIR)
    import warrior

from warrior.Framework.Utils import config_Utils, file_Utils, xml_Utils
from warrior.Framework.Utils.data_Utils import get_credentials
import warrior.Framework.Utils.encryption_utils as Encrypt
from warrior.WarriorCore.Classes import war_cli_class
from warrior.WarriorCore import testcase_steps_execution, common_execution_utils
from warrior.WarriorCore import testcase_driver
from warrior.WarriorCore import sequential_testcase_driver
from warrior.WarriorCore import parallel_testcase_driver
from warrior.WarriorCore import testsuite_driver
from warrior.WarriorCore import project_driver
from warrior.Framework import Utils
from argparse import Namespace

from warrior.WarriorCore import warrior_cli_driver

temp_cwd = os.path.split(__file__)[0]
path = os.path.join(temp_cwd, 'UT_results')

try:
    os.makedirs(path, exist_ok=True)
    result_dir = os.path.join(dirname(abspath(__file__)), 'UT_results')
except OSError as error:
    pass

def test_update_jira_by_id1():
    '''
    Test case for update jira by id.
    '''
    jiraproj = None
    jiraid = False
    exec_dir = result_dir
    status = True
    result = warrior_cli_driver.update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    assert result == None

def test_update_jira_by_id2():
    '''
    Test case for update jira by id.
    '''
    import shutil
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.status = "Closed"
    warrior.WarriorCore.Classes.jira_rest_class.Jira.get_jira_issue_status = \
    MagicMock(return_value="Closed")
    warrior.WarriorCore.Classes.jira_rest_class.Jira.set_jira_issue_status = \
    MagicMock(return_value=None)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.upload_logfile_to_jira_issue = \
    MagicMock(return_value=None)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.update_jira_issue = \
    MagicMock(return_value=None)
    shutil.make_archive = MagicMock(return_value="name.zip")
    jiraproj = None
    jiraid = "war-123"
    exec_dir = result_dir
    status = True
    result = warrior_cli_driver.update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.get_jira_issue_status
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.set_jira_issue_status
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.upload_logfile_to_jira_issue
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.update_jira_issue
    del shutil.make_archive
    del mock_tools

def test_update_jira_by_id3(capsys):
    '''
    Test case for update jira by id.
    '''
    import shutil
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.get_jira_issue_status = \
    MagicMock(return_value="Clsdosed")
    warrior.WarriorCore.Classes.jira_rest_class.Jira.set_jira_issue_status = \
    MagicMock(return_value=None)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.upload_logfile_to_jira_issue = \
    MagicMock(return_value=None)
    warrior.WarriorCore.Classes.jira_rest_class.Jira.update_jira_issue = \
    MagicMock(return_value=None)
    shutil.make_archive = MagicMock(return_value="name.zip")
    jiraproj = None
    jiraid = "war-123"
    exec_dir = result_dir
    status = True
    result = warrior_cli_driver.update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.get_jira_issue_status
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.set_jira_issue_status
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.upload_logfile_to_jira_issue
    del warrior.WarriorCore.Classes.jira_rest_class.Jira.update_jira_issue
    del shutil.make_archive
    del mock_tools

def test_decide_overwrite_var_full_path_datafile():
    """options provided in cli get preference over the ones provided inside tests
    """
    overwrite = {}
    temp_dir1 = os.path.join(os.path.split(__file__)[0], "war_test1.xml")
    namespace = Namespace(datafile=temp_dir1, random_tc_execution=False, wrapperfile=None,\
         resultdir=None, logdir=None, outputdir=None, jobid=None, pythonpath=None,\
          genericdatafile=None, gen_select_rows=None, gen_no_of_samples=None,\
           gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_datafile'] == temp_dir1

def test_decide_overwrite_var_dynamic_path_datafile():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir1 = os.path.join(os.getcwd(), "war_test1.xml")
    namespace = Namespace(datafile='war_test1.xml', random_tc_execution=False, wrapperfile=None,\
         resultdir=None, logdir=None, outputdir=None, jobid=None, pythonpath=None,\
         genericdatafile=None, gen_no_of_samples=None, gen_select_rows=None,\
         gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_datafile'] == temp_dir1

def test_decide_overwrite_var_full_path_wrapperfile():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir1 = os.path.join(os.path.split(__file__)[0], "war_test1.xml")
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=temp_dir1, resultdir=None, logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, gen_no_of_samples=None, gen_select_rows=None,\
       genericdatafile=None, gen_shuffle_columns=None, gen_purge_db=None,\
        gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_testwrapperfile'] == temp_dir1

def test_decide_overwrite_var_dynamic_path_dynamic_path_wrapperfile():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir = os.path.join(os.getcwd(), "war_test1.xml")
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile='war_test1.xml', resultdir=None, logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_select_rows=None,\
       gen_no_of_samples=None, gen_shuffle_columns=None, gen_purge_db=None,\
        gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_testwrapperfile'] == temp_dir

def test_decide_overwrite_var_random_tc_execution_true():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir = os.path.join(os.path.split(__file__)[0], "war_test3.xml")
    namespace = Namespace(datafile=None, random_tc_execution=True,\
     wrapperfile=None, resultdir=None, logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_select_rows=None,\
       gen_no_of_samples=None, gen_shuffle_columns=None, gen_purge_db=None,\
        gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['random_tc_execution'] == True

def test_decide_overwrite_var_full_path_resultdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir = os.path.join(os.path.split(__file__)[0], "war_test3.xml")
    resultdir = os.path.split(__file__)[0]

    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=resultdir, logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_select_rows=None, gen_no_of_samples=None,\
       gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_resultdir'] == resultdir

def test_decide_overwrite_var_dynamic_path_resultdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir = os.path.join(os.getcwd(), 'test_WarriorCore')
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir='test_WarriorCore', logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_select_rows=None,\
       gen_no_of_samples=None, gen_shuffle_columns=None, gen_purge_db=None,\
        gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_resultdir'] == temp_dir

def test_decide_overwrite_var_full_path_logdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    temp_dir = os.path.join(os.path.split(__file__)[0], "war_test3.xml")
    resultdir = os.path.split(__file__)[0]
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=None, logdir=resultdir, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_no_of_samples=None, gen_select_rows=None,\
       gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_logdir'] == resultdir

def test_decide_overwrite_var_dynamic_path_logdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    logdir = result_dir
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=None, logdir=logdir, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_no_of_samples=None, gen_select_rows=None,\
       gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_logdir'] == logdir

def test_decide_overwrite_var_full_path_outputdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    outputdir = result_dir
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=None, logdir=None, outputdir=outputdir, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_no_of_samples=None, gen_select_rows=None,\
       gen_shuffle_columns=None, gen_purge_db=None, gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_resultdir'] == outputdir
    assert result['ow_logdir'] == outputdir

def test_decide_overwrite_var_dynamic_path_outputdir():
    """options provided in cli get preference over the ones provided inside tests
    """
    outputdir = result_dir
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=None, logdir=None, outputdir=outputdir, jobid=None,\
      pythonpath=None, genericdatafile=None, gen_no_of_samples=None,\
       gen_shuffle_columns=None, gen_select_rows=None, gen_purge_db=None,\
        gen_exec_tag=None, gen_report=None)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    assert result['ow_resultdir'] == outputdir
    assert result['ow_logdir'] == outputdir

def test_decide_overwrite_var_gen():
    """options provided in cli get preference over the ones provided inside tests
    """
    outputdir = result_dir
    namespace = Namespace(datafile=None, random_tc_execution=False,\
     wrapperfile=None, resultdir=None, logdir=None, outputdir=None, jobid=None,\
      pythonpath=None, genericdatafile=True, gen_no_of_samples=True,\
       gen_shuffle_columns=True, gen_select_rows=True, gen_purge_db=True,\
        gen_exec_tag=True, gen_report=True)
    result = warrior_cli_driver.decide_overwrite_var(namespace)
    test1 = 'genericdatafile' in result
    test2 = 'gen_no_of_samples' in result
    test3 = 'gen_shuffle_columns' in result
    assert test1 == True
    assert test2 == True
    assert test3 == True

def test_decide_action():
    """Prepare filepath and other arguments for Warrior main to use"""
    args = ['war_test1.xml']
    w_cli_obj = war_cli_class.WarriorCliClass()
    parsed_args = w_cli_obj.parser(args)
    result = warrior_cli_driver.decide_action(w_cli_obj, parsed_args)
    assert result[0] == args

def test_main():
    """init a Warrior Cli Class object, parse its arguments and run it"""
    args = ['war_test1.xml']
    result = warrior_cli_driver.main(args)
    assert result[0] == args

def test_append_path():
    """Append appropriate paths for testcase/suite/project in test folder
    """
    abs_filepath = os.path.join(os.path.split(__file__)[0], "war_test1.xml")
    filepath = [abs_filepath]
    path_list = [result_dir]
    path = result_dir
    result = warrior_cli_driver.append_path(filepath, path_list, path)
    assert result[0] == abs_filepath

def test_file_execution_for_testcase():
    """
        Call the corresponded driver of each file type
    """
    abs_filepath = os.path.join(os.path.split(__file__)[0], "war_test1.xml")
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    cli_args = Namespace(ad=False, jiraproj=None, jiraid=False,)
    warrior.WarriorCore.warrior_cli_driver.update_jira_by_id = MagicMock()
    warrior.Framework.Utils.email_utils.compose_send_email = MagicMock()
    Utils.data_Utils.get_object_from_datarepository = MagicMock(return_value=False)
    data_repository = {'wt_resultsdir':result_dir, 'wt_logsdir':result_dir}
    testcase_driver.main = MagicMock(return_value=(True,7.0, data_repository))
    testcase_steps_execution.main = MagicMock(return_value=([True], [abs_filepath], ['impact']))
    common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=('RUF', 1, None))
    default_repo =  {'db_obj': False, 'wt_resultsdir':result_dir, 'wt_logsdir':result_dir,\
    'wt_filename':'war_test1.xml'}
    result = warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)
    assert result == True
    assert default_repo['war_file_type'] == 'Case'
    assert default_repo['wt_filename'] == 'war_test1.xml'
    del mock_tools
    del testcase_steps_execution.main
    del testcase_driver.main
    del common_execution_utils.get_runmode_from_xmlfile
    del warrior.WarriorCore.warrior_cli_driver.update_jira_by_id
    del warrior.Framework.Utils.email_utils.compose_send_email
    del Utils.data_Utils.get_object_from_datarepository

def test_file_execution_for_testsuite():
    """
        Call the corresponded driver of each file type
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    cli_args = Namespace(ad=False, jiraproj=None, jiraid=False)
    suite_repository = {'suite_execution_dir':result_dir, 'ws_logs_execdir':result_dir,\
     'ws_results_execdir':result_dir}
    warrior.WarriorCore.warrior_cli_driver.update_jira_by_id = MagicMock()
    warrior.Framework.Utils.email_utils.compose_send_email = MagicMock()
    abs_filepath = os.path.join(os.path.split(__file__)[0], "war_suite.xml")
    testsuite_driver.main = MagicMock(return_value=(True, suite_repository))
    # common_execution_utils.get_runmode_from_xmlfile = MagicMock(return_value=('RUF', 1, None))
    testcase_steps_execution.main = MagicMock(return_value=([True], [abs_filepath], ['impact']))
    default_repo =  {'db_obj': False, 'wt_resultsdir':result_dir, 'wt_logsdir':result_dir,\
     'wt_filename':'war_test1.xml'}
    result = warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)
    assert result == True
    assert default_repo['war_file_type'] == 'Suite'
    assert default_repo['wt_filename'] == 'war_test1.xml'
    del mock_tools
    del testcase_steps_execution.main
    del testsuite_driver.main
    del warrior.WarriorCore.warrior_cli_driver.update_jira_by_id
    del warrior.Framework.Utils.email_utils.compose_send_email

def test_file_execution_for_project():
    """
        Call the corresponded driver of each file type
    """
    tools_dir = dirname(dirname(abspath(__file__))) + os.sep + "Tools"
    os.environ["WAR_TOOLS_DIR"] = tools_dir
    mock_tools = os.getenv("WAR_TOOLS_DIR")
    mock_tools = MagicMock(return_value=mock_tools)
    cli_args = Namespace(ad=False, jiraproj=None, jiraid=False,)
    abs_filepath = os.path.join(os.path.split(__file__)[0], "war_project.xml")
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior.WarriorCore.warrior_cli_driver.update_jira_by_id = MagicMock()
    warrior.Framework.Utils.email_utils.compose_send_email = MagicMock()
    project_repository = {'project_execution_dir':result_dir, 'wp_logs_execdir':result_dir,\
    'wp_results_execdir':result_dir}
    project_driver.main = MagicMock(return_value=(True, project_repository))
    testcase_steps_execution.main = MagicMock(return_value=([True], [abs_filepath], ['impact']))
    default_repo =  {'db_obj': False, 'wt_resultsdir':result_dir, 'wt_logsdir':result_dir,\
    'execution_type':'sequential_suites', 'wt_filename':'war_test1.xml'}
    result = warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)
    assert result == True
    assert default_repo['war_file_type'] == 'Project'
    assert default_repo['wt_filename'] == 'war_test1.xml'
    del mock_tools
    del testcase_steps_execution.main
    del Utils.xml_Utils.getChildAttributebyParentTag
    del project_driver.main
    del warrior.WarriorCore.warrior_cli_driver.update_jira_by_id
    del warrior.Framework.Utils.email_utils.compose_send_email

def test_group_execution():
    """
        Process the parameter list and prepare environment for file_execution
    """
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    warrior_cli_driver.file_execution = MagicMock(return_value=True)
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
    dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
    headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
    kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
    proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
    secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
    tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
    version=False, wrapperfile=None)
    db_obj = False
    overwrite = {}
    livehtmlobj = None
    result = warrior_cli_driver.group_execution(parameter_list, cli_args, db_obj, overwrite,\
     livehtmlobj)
    assert result == True
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.file_execution

def test_group_execution_negative():
    """
        Process the parameter list and prepare environment for file_execution
    """
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior_cli_driver.file_execution = MagicMock(return_value=False)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
    dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
    headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
    kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
    proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
    secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
    tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
    version=False, wrapperfile=None)
    db_obj = False
    overwrite = {}
    livehtmlobj = None
    result = warrior_cli_driver.group_execution(parameter_list, cli_args, db_obj, overwrite,\
     livehtmlobj)
    assert result == False
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.file_execution

def test_execution():
    '''testcase for execution method'''
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior_cli_driver.group_execution = MagicMock(return_value=True)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
        dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
        headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
        kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
        proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
        secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
        tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
        version=False, wrapperfile=None)
    overwrite = {}
    livehtmlobj = None
    result = warrior_cli_driver.execution(parameter_list, cli_args, overwrite, livehtmlobj)
    assert result == True
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.group_execution

def test_execution_negative():
    '''testcase for execution method'''
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior_cli_driver.group_execution = MagicMock(return_value=False)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
        dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
        headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
        kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
        proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
        secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
        tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
        version=False, wrapperfile=None)
    overwrite = {}
    livehtmlobj = None
    result = warrior_cli_driver.execution(parameter_list, cli_args, overwrite, livehtmlobj)
    assert result == False
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.group_execution

def test_execution_livehtmlobj():
    '''testcase for execution method'''
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    config_Utils.redirect_print.katana_console_log = MagicMock(return_value=None)
    warrior_cli_driver.group_execution = MagicMock(return_value=True)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
        dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
        headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
        kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
        proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
        secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
        tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
        version=False, wrapperfile=None)
    overwrite = {}
    livehtmlobj = True
    # with pytest.raises(SystemExit):
    result = warrior_cli_driver.execution(parameter_list, cli_args, overwrite, livehtmlobj)
    assert result == True
    del Utils.xml_Utils.getChildAttributebyParentTag
    del config_Utils.redirect_print.katana_console_log
    del warrior_cli_driver.group_execution

def test_execution_version():
    '''testcase for execution method'''
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior_cli_driver.group_execution = MagicMock(return_value=True)
    parameter_list = [os.path.join(os.path.split(__file__)[0], "war_project.xml")]
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
        dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
        headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
        kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
        proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
        secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
        tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
        version=True, wrapperfile=None)
    overwrite = {}
    livehtmlobj = None
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.execution(parameter_list, cli_args, overwrite, livehtmlobj)
        assert result == True
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.group_execution

def test_execution_parameter_list():
    '''testcase for execution method'''
    Utils.xml_Utils.getChildAttributebyParentTag = MagicMock(return_value=False)
    warrior_cli_driver.group_execution = MagicMock(return_value=True)
    parameter_list = None
    cli_args = Namespace(RMT=0, RUF=0, ad=False, cat=None, create=False, datafile=None,\
        dbsystem=None, ddir=None, decrypt=None, djson=None, encrypt=None, filepath=parameter_list,\
        headless=False, ironclaw=False, jiraid=False, jiraproj=None, jobid=None, kwparallel=False,\
        kwsequential=False, livehtmllocn=None, logdir=None, mock=False, outputdir=None,\
        proj_name=None, pythonpath=None, random_tc_execution=False, resultdir=None, runcat=None,\
        secretkey=False, sim=False, suite_dest=None, suitename=None, target_time=None, tc_gen=None,\
        tc_name=None, tcdir=None, tcparallel=False, tcsequential=False, ts_name=None, ujd=False,\
        version=False, wrapperfile=None)
    overwrite = {}
    livehtmlobj = None
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.execution(parameter_list, cli_args, overwrite, livehtmlobj)
        assert result == True
    del Utils.xml_Utils.getChildAttributebyParentTag
    del warrior_cli_driver.group_execution

def test_decide_action_runcat1():
    '''
    Test case for decide_action.
    '''
    args = ['war_test1.xml']
    w_cli_obj = war_cli_class.WarriorCliClass()
    parameter_list = os.path.join(os.path.split(__file__)[0], "war_project.xml")
    w_cli_obj.check_tag = MagicMock(return_value=[])
    namespace = Namespace(target_time=None, kwparallel=None, kwsequential=None, tcparallel=None,\
        tcsequential=None, RMT=None, RUF=None, filepath=None, runcat=[True], create=None,\
        encrypt=None, decrypt=None, ujd=None, tc_name=None, suitename=None, proj_name=None,\
         tcdir=None, suite_dest=None, ts_name=None)
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.decide_action(w_cli_obj, namespace)
        test1 = namespace in result
        assert type(result) == tuple
        assert test1 == True
        assert result[0] == ['war_test1.xml']
    del w_cli_obj.check_tag

def test_decide_action_create():
    '''
    Test case for decide_action.
    '''
    args = ['war_test1.xml']
    w_cli_obj = war_cli_class.WarriorCliClass()
    parameter_list = os.path.join(os.path.split(__file__)[0], "war_project.xml")
    namespace = Namespace(target_time=None, kwparallel=None, kwsequential=None, tcparallel=None,\
        tcsequential=None, RMT=None, RUF=None, filepath=None, runcat=None, create=True,\
        encrypt=None, decrypt=None, ujd=None, tc_name='war_test1', suitename=None,\
        proj_name=None, tcdir=None, cat=None)
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.decide_action(w_cli_obj, namespace)
        test1 = namespace in result
        assert type(result) == tuple
        assert test1 == True
        assert result[0] == ['war_test1.xml']

def test_decide_action_ujd():
    '''
    Test case for decide_action.
    '''
    w_cli_obj = war_cli_class.WarriorCliClass()
    w_cli_obj.manual_defects = MagicMock(return_value=None)
    namespace = Namespace(target_time=None, kwparallel=None, kwsequential=None, tcparallel=None,\
        tcsequential=None, RMT=None, RUF=None, filepath=None, runcat=None, create=None,\
        encrypt=None, decrypt=None, ujd=True, tc_name='war_test1', suitename=None,\
        proj_name=None, tcdir=None, cat=None, ddir=True, djson=None, jiraproj=None)
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.decide_action(w_cli_obj, namespace)
        test1 = namespace in result
        assert type(result) == tuple
        assert test1 == True
        assert result[0] == ['war_test1.xml']
    del w_cli_obj.manual_defects

def test_decide_action_ujd1():
    '''
    Test case for decide_action.
    '''
    w_cli_obj = war_cli_class.WarriorCliClass()
    w_cli_obj.manual_defects = MagicMock(return_value=None)
    namespace = Namespace(target_time=None, kwparallel=None, kwsequential=None, tcparallel=None,\
        tcsequential=None, RMT=None, RUF=None, filepath=None, runcat=None, create=None,\
        encrypt=None, decrypt=None, ujd=True, tc_name='war_test1', suitename=None, proj_name=None,\
        tcdir=None, cat=None, ddir=None, djson=True, jiraproj=None)
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.decide_action(w_cli_obj, namespace)
        test1 = namespace in result
        assert type(result) == tuple
        assert test1 == True
        assert result[0] == ['war_test1.xml']
    del w_cli_obj.manual_defects

def test_decide_action_ujd2():
    '''
    Test case for decide_action.
    '''
    w_cli_obj = war_cli_class.WarriorCliClass()
    w_cli_obj.manual_defects = MagicMock(return_value=None)
    namespace = Namespace(target_time=None, kwparallel=None, kwsequential=None, tcparallel=None,\
        tcsequential=None, RMT=None, RUF=None, filepath=None, runcat=None, create=None,\
        encrypt=None, decrypt=None, ujd=True, tc_name='war_test1', suitename=None, proj_name=None,\
        tcdir=None, cat=None, ddir=True, djson=True, jiraproj=None)
    with pytest.raises(SystemExit):
        result = warrior_cli_driver.decide_action(w_cli_obj, namespace)
        test1 = namespace in result
        assert type(result) == tuple
        assert test1 == True
        assert result[0] == ['war_test1.xml']
    del w_cli_obj.manual_defects

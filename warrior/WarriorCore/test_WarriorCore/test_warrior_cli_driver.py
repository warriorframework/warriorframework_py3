import sys, os
import pytest
from unittest import mock
from os.path import abspath, dirname
from argparse import Namespace
from unittest.mock import patch, sentinel
from unittest.mock import MagicMock

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

def test_update_jira_by_id1(capsys):
    from warrior.WarriorCore.warrior_cli_driver import update_jira_by_id

    jiraproj= None
    jiraid= False
    exec_dir= "some address"
    status= True
    update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    out, err = capsys.readouterr()
    assert out == "-I- jiraid not provided, will not update jira issue\n"

def test_update_jira_by_id2(capsys):
    from warrior.WarriorCore.warrior_cli_driver import update_jira_by_id
    from warrior.WarriorCore.Classes.jira_rest_class import Jira
    import shutil

    jira = Jira(None)
    jira = MagicMock()
    Jira.status = "Closed"
    Jira.get_jira_issue_status = MagicMock(return_value= "Closed")
    Jira.set_jira_issue_status= MagicMock(return_value= None)
    Jira.upload_logfile_to_jira_issue= MagicMock(return_value= None)
    Jira.update_jira_issue = MagicMock(return_value= None)
    shutil.make_archive = MagicMock(return_value= "name.zip")
    jiraproj= None
    jiraid= "adasdsa"
    exec_dir= "some address"
    status= True
    update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    out, err = capsys.readouterr()
    assert out == "-I- Reopening Jira issue 'adasdsa' to upload warrior execution logs\n-I- Closing Jira issue 'adasdsa' which was reopened earlier\n"

def test_update_jira_by_id3(capsys):
    import shutil
    from warrior.WarriorCore.warrior_cli_driver import update_jira_by_id
    from warrior.WarriorCore.Classes.jira_rest_class import Jira

    jira = Jira(None)
    Jira.get_jira_issue_status = MagicMock(return_value= "Clsdosed")
    Jira.set_jira_issue_status= MagicMock(return_value= None)
    Jira.upload_logfile_to_jira_issue= MagicMock(return_value= None)
    Jira.update_jira_issue = MagicMock(return_value= None)
    shutil.make_archive = MagicMock(return_value= "name.zip")
    jiraproj= None
    jiraid= "adasdsa"
    exec_dir= "some address"
    status= True
    update_jira_by_id(jiraproj, jiraid, exec_dir, status)
    out, err = capsys.readouterr()
    assert out == ""

def test_file_execution1():
    import warrior
    from argparse import Namespace
    from xml.etree.ElementTree import Element
    from warrior.WarriorCore import testcase_driver
    from warrior.Framework.Utils import email_utils as email

    Namespace = MagicMock()
    Element = MagicMock()
    email.compose_send_email = MagicMock(return_value = None)
    warrior_cli_driver.update_jira_by_id = MagicMock(return_value = None)
    Element.tag = 'Testcase'
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = Element)
    testcase_driver.main = MagicMock(return_value = (True,7.0,{'wt_resultsdir':"some path", 'wt_logsdir':"some path", 'wt_resultsdir': "some dir"}))
    jiraproj= None
    default_repo= {'db_obj': False}
    abs_filepath = "xml"
    status= True
    cli_args = Namespace
    cli_args.ad = False
    cli_args.jiraproj = None
    cli_args.jiraid = False
    warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)

def test_file_execution2():
    import warrior
    from argparse import Namespace
    from xml.etree.ElementTree import Element
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore import testsuite_driver
    from warrior.Framework.Utils import email_utils as email

    Namespace = MagicMock()
    Element = MagicMock()
    email.compose_send_email = MagicMock(return_value = None)
    warrior_cli_driver.update_jira_by_id = MagicMock(return_value = None)
    Element.tag = 'TestSuite'
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = Element)
    testsuite_driver.main = MagicMock(return_value = (True, {'suite_execution_dir': "some dir", 'ws_logs_execdir': "some dir", 'ws_results_execdir': "some dir"}))
    jiraproj= None
    default_repo= {'db_obj': False}
    abs_filepath = "xml"
    status= True
    cli_args = Namespace
    cli_args.ad = False
    cli_args.jiraproj = None
    cli_args.jiraid = False
    warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)

def test_file_execution3():
    import warrior
    from argparse import Namespace
    from xml.etree.ElementTree import Element
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore import project_driver
    from warrior.Framework.Utils import email_utils as email

    Namespace = MagicMock()
    Element = MagicMock()
    email.compose_send_email = MagicMock(return_value = None)
    warrior_cli_driver.update_jira_by_id = MagicMock(return_value = None)
    Element.tag = 'Project'
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = Element)
    project_driver.main = MagicMock(return_value = (True, {'project_execution_dir': "some dir", 'wp_logs_execdir': "some dir", 'wp_results_execdir': "some dir"}))
    jiraproj= None
    default_repo= {'db_obj': False}
    abs_filepath = "xml"
    status= True
    cli_args = Namespace
    cli_args.ad = False
    cli_args.jiraproj = None
    cli_args.jiraid = False
    warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)

def test_file_execution4(capsys):
    import warrior
    from argparse import Namespace
    from xml.etree.ElementTree import Element
    from warrior.WarriorCore import project_driver

    Namespace = MagicMock()
    Element = MagicMock()
    Element.tag = 'roject'
    warrior.Framework.Utils.xml_Utils.getRoot = MagicMock(return_value = Element)
    jiraproj= None
    default_repo= {'db_obj': False}
    abs_filepath = "xml"
    status= True
    cli_args = Namespace
    cli_args.ad = False
    cli_args.jiraproj = None
    cli_args.jiraid = False
    warrior_cli_driver.file_execution(cli_args, abs_filepath, default_repo)
    del warrior_cli_driver.file_execution

def test_execution1(capsys):
    from warrior.Framework.ClassUtils import database_utils_class
    from warrior.WarriorCore.warrior_cli_driver import execution
    from warrior.Framework.Utils import config_Utils, file_Utils
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore import framework_detail
    from argparse import Namespace

    warrior_cli_driver.file_execution = MagicMock(return_value= True)
    parameter_list = [1,2]
    cli_args = Namespace
    cli_args.livehtmllocn = False
    cli_args.version = False
    cli_args.ironclaw = False
    cli_args.dbsystem = None
    database_utils_class.create_database_connection = MagicMock(return_value = False)
    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    cli_args = Namespace
    cli_args.livehtmllocn = False
    livehtmlobj= False
    overwrite = {"1":"1", "2":"2"}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1]
    config_Utils.redirect_print.katana_console_log = MagicMock(return_value= "livehtmlobj")
    overwrite = {"1":"1", "2":"2"}
    livehtmlobj = True
    execution(parameter_list, cli_args, overwrite, livehtmlobj)
    del warrior_cli_driver.file_execution

def test_execution2(capsys):
    from warrior.WarriorCore.warrior_cli_driver import execution
    from warrior.Framework.Utils import config_Utils, file_Utils
    from warrior.WarriorCore import framework_detail
    from warrior.Framework.ClassUtils import database_utils_class
    from warrior.WarriorCore import ironclaw_driver
    from argparse import Namespace

    cli_args = Namespace
    cli_args.version = True
    cli_args.ironclaw = True
    cli_args.dbsystem = None
    framework_detail.warrior_framework_details = MagicMock(return_value = None)
    ironclaw_driver.main = MagicMock(return_value = True)
    livehtmlobj= True
    overwrite = {"1":"1", "2":"2"}
    parameter_list = []
    config_Utils.redirect_print.katana_console_log = MagicMock()
    overwrite = {"1":"1", "2":"2"}
    livehtmlobj = True
    with patch('sys.exit') as exit_mock:
        execution(parameter_list, cli_args, overwrite, livehtmlobj)
        assert exit_mock.called

def test_group_execution1():
    from warrior.WarriorCore.warrior_cli_driver import group_execution
    from warrior.WarriorCore import warrior_cli_driver
    from argparse import Namespace
    from warrior.Framework.Utils import file_Utils
    from warrior.WarriorCore import framework_detail
    from warrior.Framework.ClassUtils import database_utils_class

    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    framework_detail.warrior_banner = MagicMock(return_value= None)
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    file_Utils.fileExists = MagicMock(return_value= True)
    database_utils_class.create_database_connection =  MagicMock()
    warrior_cli_driver.add_live_table_divs = MagicMock(return_value= None)
    warrior_cli_driver.file_execution = MagicMock(return_value= True)
    cli_args = Namespace
    cli_args.livehtmllocn = False
    livehtmlobj= False
    overwrite = {"1":"1", "2":"2", "pythonpath":''}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1,2,3,4]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)
    assert result == True
    del warrior_cli_driver.file_execution
    del warrior_cli_driver.add_live_table_divs

def test_group_execution2(capsys):
    from warrior.WarriorCore.warrior_cli_driver import group_execution
    from argparse import Namespace
    from warrior.Framework.Utils import file_Utils
    from warrior.Framework.ClassUtils import database_utils_class

    file_Utils.get_extension_from_path = MagicMock(return_value= '.sdxml')
    cli_args = Namespace
    cli_args.livehtmllocn = False
    livehtmlobj= False
    overwrite = {"1":"1", "2":"2","pythonpath":''}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)
    out, err = capsys.readouterr()
    assert out == "-E- unrecognized file format !!!\n"

def test_group_execution3(capsys):
    from argparse import Namespace
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.Framework.Utils import file_Utils
    from warrior.Framework.ClassUtils import database_utils_class
    from warrior.WarriorCore.warrior_cli_driver import group_execution

    warrior_cli_driver.file_execution = MagicMock(return_value= True)
    warrior_cli_driver.add_live_table_divs = MagicMock(return_value= None)
    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    cli_args = Namespace
    cli_args.livehtmllocn = False
    livehtmlobj= False
    overwrite = {"1":"1", "2":"2","pythonpath":''}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)
    out, err = capsys.readouterr()
    assert out == "-I- Absolute path: path of file\n"
    del warrior_cli_driver.file_execution
    del warrior_cli_driver.add_live_table_divs

def test_group_execution4():
    from warrior.WarriorCore.warrior_cli_driver import group_execution
    from warrior.WarriorCore import warrior_cli_driver# import add_live_table_divs
    from argparse import Namespace
    from warrior.Framework.Utils import file_Utils
    from warrior.WarriorCore import framework_detail
    from warrior.Framework.ClassUtils import database_utils_class

    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    framework_detail.warrior_banner = MagicMock(return_value= None)
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    file_Utils.fileExists = MagicMock(return_value= False)
    cli_args = Namespace
    cli_args.livehtmllocn = False
    livehtmlobj= False
    overwrite = {"1":"1", "2":"2", "pythonpath":''}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1,2,3,4]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)

def test_group_execution5(capsys):
    from warrior.Framework import Utils
    from argparse import Namespace
    from warrior.Framework.Utils import file_Utils
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.Framework.ClassUtils import database_utils_class
    from warrior.WarriorCore.warrior_cli_driver import group_execution

    warrior_cli_driver.add_live_table_divs = MagicMock(return_value= None)
    warrior_cli_driver.file_execution = MagicMock(return_value= True)
    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    Utils.file_Utils.fileExists = MagicMock(return_value = True)
    cli_args = Namespace
    cli_args.livehtmllocn = "str"
    livehtmlobj= None
    overwrite = {"1":"1","2":"2","pythonpath":""}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)
    out, err = capsys.readouterr()
    assert out == '-I- Absolute path: path of file\n'
    del warrior_cli_driver.file_execution
    del warrior_cli_driver.add_live_table_divs

def test_group_execution6(capsys):
    from warrior.Framework import Utils
    from argparse import Namespace
    from warrior.Framework.Utils import file_Utils
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.Framework.ClassUtils import database_utils_class
    from warrior.WarriorCore.warrior_cli_driver import group_execution

    warrior_cli_driver.add_live_table_divs = MagicMock(return_value= None)
    warrior_cli_driver.file_execution = MagicMock(return_value= True)
    file_Utils.get_extension_from_path = MagicMock(return_value= '.xml')
    file_Utils.getAbsPath = MagicMock(return_value= "path of file")
    Utils.file_Utils.fileExists = MagicMock(return_value = True)
    cli_args = Namespace
    cli_args.livehtmllocn = "str"
    livehtmlobj= None
    overwrite = {"1":"1","2":"2","pythonpath":"/home/cde:/home/abc"}
    db_obj= database_utils_class.create_database_connection
    db_obj.status = True
    parameter_list = [1]
    result = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)
    out, err = capsys.readouterr()
    assert out == "-I- Absolute path: path of file\n-I- user repositories path list is ['/home/cde', '/home/abc']\n-E- Given pythonpath doesn't exist : /home/cde\n-E- Given pythonpath doesn't exist : /home/abc\n"
    del warrior_cli_driver.file_execution
    del warrior_cli_driver.add_live_table_divs

def test_append_path1(capsys):
    from warrior.WarriorCore.warrior_cli_driver import append_path

    filepath = ["/home/helo/Desktop"]
    path_list = ["abc.xml"]
    path = "Warriorspace/Testcases/"
    append_path(filepath, path_list, path)
    out, err = capsys.readouterr()
    assert True

def test_decide_runcat_actions1(capsys):
    from warrior.WarriorCore.warrior_cli_driver import decide_runcat_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(filepath="['Warriorspace/Testcases/unitest.xml']", \
        tcdir=None, runcat="abc", suitename=None)
    w_cli_obj.check_tag = MagicMock(return_value = "/home/hlo")
    with patch('sys.exit') as exit_mock:
        decide_runcat_actions(w_cli_obj, namespace)
    out, err = capsys.readouterr()
    assert True

def test_decide_runcat_actions2(capsys):
    from warrior.WarriorCore.warrior_cli_driver import decide_runcat_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(filepath=['Warriorspace/Testcases/unitest.xml'], \
        tcdir=None, runcat=["abc"], suitename="suite")

    w_cli_obj.examine_create_suite = MagicMock(return_value = '["/home/hlo"]')
    filepath = w_cli_obj.examine_create_suite

    with patch('sys.exit') as exit_mock:
        decide_runcat_actions(w_cli_obj, namespace)
    out, err = capsys.readouterr()
    assert True

def test_decide_createsuite_actions1():
    from warrior.WarriorCore.warrior_cli_driver import decide_createsuite_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(filepath="['Warriorspace/Testcases/unitest.xml']", \
        tcdir=None, cat= None, suitename="suite")
    w_cli_obj.examine_create_suite = MagicMock(return_value = "['/hoome/hlo']")

    with pytest.raises(SystemExit):
        result = decide_createsuite_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_createsuite_actions2():
    from warrior.WarriorCore.warrior_cli_driver import decide_createsuite_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(filepath=None, \
        tcdir=None, cat= None, suitename=None)
    w_cli_obj.examine_create_suite = MagicMock(return_value = "['/hoome/hlo']")

    with pytest.raises(SystemExit):
        result = decide_createsuite_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_createsuite_actions3():
    from warrior.WarriorCore.warrior_cli_driver import decide_createsuite_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(filepath="['Warriorspace/Testcases/unitest.xml']", \
        tcdir=None, cat= "cat", suitename=None)
    w_cli_obj.examine_create_suite = MagicMock(return_value = "['/hoome/hlo']")

    with pytest.raises(SystemExit):
        result = decide_createsuite_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_ujd_actions1():
    from warrior.WarriorCore.warrior_cli_driver import decide_ujd_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(ujd=True, ddir="hlo", djson=None,jiraproj=None)
    w_cli_obj.manual_defects = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_ujd_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_ujd_actions2():
    from warrior.WarriorCore.warrior_cli_driver import decide_ujd_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(ujd=True, ddir=None, djson={"one":1,"two":2}, jiraproj=None)
    w_cli_obj.manual_defects = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_ujd_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_ujd_actions3():
    from warrior.WarriorCore.warrior_cli_driver import decide_ujd_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(ujd=True, ddir="ddir", djson={"one":1,"two":2}, jiraproj=None)
    w_cli_obj.manual_defects = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_ujd_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_ujd_actions4():
    from warrior.WarriorCore.warrior_cli_driver import decide_ujd_actions
    from warrior.WarriorCore.Classes import war_cli_class

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(ujd=True, ddir=None, djson=None, jiraproj=None)
    w_cli_obj.manual_defects = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_ujd_actions(w_cli_obj, namespace)
        assert exit_mock.called

def test_decide_overwrite_var1():
    from warrior.WarriorCore.warrior_cli_driver import decide_overwrite_var

    namespace = Namespace(datafile='Warriorspace/Data/unitest.xml',\
        wrapperfile='Warriorspace/wrapper_files/unitest.xml', random_tc_execution=True,\
        resultdir='Warriorspace/Execution', logdir='Warriorspace/Execution', outputdir= \
        'Warriorspace/Execution')

    with pytest.raises(SystemExit):
        decide_overwrite_var(namespace)
        assert exit_mock.called

def test_decide_action1():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.warrior_cli_driver import decide_action
    from warrior.WarriorCore.Classes import war_cli_class
    from warrior.Framework.Utils import file_Utils

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass

    namespace = Namespace(RMT=0, RUF=0, target_time=10, kwparallel=False,\
        kwsequential=False, tcparallel=False, tcsequential=False,\
        filepath='Warriorspace/Testcases/unitest.xml', runcat="runcat",\
        tc_name=None, ts_name=None, proj_name=None)

    w_cli_obj.gosleep = MagicMock(return_value = None)
    warrior_cli_driver.decide_runcat_actions = MagicMock(return_value = ['Warriorspace/Testcases/unitest.xml'])
    warrior_cli_driver.decide_createsuite_actions = MagicMock(return_value = None)
    file_Utils.get_parent_dir = MagicMock(return_value = None)
    warrior_cli_driver.decide_overwrite_var = MagicMock(return_value = None)

    decide_action(w_cli_obj, namespace)
    del warrior_cli_driver.decide_overwrite_var

def test_decide_action2():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.warrior_cli_driver import decide_action
    from warrior.WarriorCore.Classes import war_cli_class
    from warrior.Framework.Utils import file_Utils

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass

    namespace = Namespace(RMT=0, RUF=0, target_time=None, kwparallel=False,\
        kwsequential=False, tcparallel=False, tcsequential=False,\
        filepath=None, runcat=None,\
        tc_name=None, ts_name=None, proj_name=None, create=True,)

    warrior_cli_driver.decide_createsuite_actions = MagicMock(return_value = ['Warriorspace/Testcases/unitest'])
    file_Utils.get_parent_dir = MagicMock(return_value = None)
    warrior_cli_driver.decide_overwrite_var = MagicMock(return_value = None)

    decide_action(w_cli_obj, namespace)
    del warrior_cli_driver.decide_overwrite_var

def test_decide_action3():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.warrior_cli_driver import decide_action
    import warrior.Framework.Utils.encryption_utils as Encrypt
    from warrior.WarriorCore.Classes import war_cli_class
    from warrior.Framework.Utils import file_Utils

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass

    namespace = Namespace(RMT=0, RUF=0, target_time=None, kwparallel=False,\
        kwsequential=False, tcparallel=False, tcsequential=False,\
        filepath=None, runcat=None, encrypt=['ll','ss'],tc_name=None, ts_name=None,\
         proj_name=None, create=None, secretkey=True,)
    Encrypt.set_secret_key = MagicMock(return_value = (True, ['aa','sss']))
    Encrypt.encrypt = MagicMock(return_value = "testing msg")
    warrior_cli_driver.decide_overwrite_var = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_action(w_cli_obj, namespace)
        assert exit_mock.called
    del warrior_cli_driver.decide_overwrite_var

def test_decide_action4():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.warrior_cli_driver import decide_action
    import warrior.Framework.Utils.encryption_utils as Encrypt
    from warrior.WarriorCore.Classes import war_cli_class
    from warrior.Framework.Utils import file_Utils

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass
    namespace = Namespace(RMT=0, RUF=0, target_time=None, kwparallel=False,\
        kwsequential=False, tcparallel=False, tcsequential=False,\
        filepath=None, runcat=None, encrypt=['ll','ss'],tc_name=None, ts_name=None,\
         proj_name=None, create=None, secretkey=True,)

    Encrypt.set_secret_key = MagicMock(return_value = (True, ['aa','sss']))
    Encrypt.encrypt = MagicMock(return_value = "1234")
    warrior_cli_driver.decide_overwrite_var = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_action(w_cli_obj, namespace)
        assert exit_mock.called
    del warrior_cli_driver.decide_overwrite_var

def test_decide_action5():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.warrior_cli_driver import decide_action
    import warrior.Framework.Utils.encryption_utils as Encrypt
    from warrior.WarriorCore.Classes import war_cli_class
    from warrior.Framework.Utils import file_Utils

    war_cli_class.WarriorCliClass = MagicMock(return_value = None)
    w_cli_obj = war_cli_class.WarriorCliClass

    namespace = Namespace(RMT=0, RUF=0, target_time=None, kwparallel=False,\
        kwsequential=False, tcparallel=False, tcsequential=False,\
        filepath=None, runcat=None, encrypt=['ll','ss'],tc_name=None, ts_name=None,\
         proj_name=None, create=None, secretkey=False)

    file_Utils.get_parent_dir = MagicMock(return_value = str(os.getcwd()))
    warrior_cli_driver.decide_overwrite_var = MagicMock(return_value = None)

    with pytest.raises(SystemExit):
        decide_action(w_cli_obj, namespace)
        assert exit_mock.called
    del warrior_cli_driver.decide_overwrite_var

def test_main():
    from warrior.WarriorCore import warrior_cli_driver
    from warrior.WarriorCore.Classes import war_cli_class

    class temp:
        def parser(a,b):
            return "uuuu"
    obj = temp()
    war_cli_class.WarriorCliClass = MagicMock(return_value = obj)
    warrior_cli_driver.decide_action = MagicMock(return_value = None)
    result = warrior_cli_driver.main("")
    assert result == None
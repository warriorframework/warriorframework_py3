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

try:
    import site
    import os
    import sys
    from collections import OrderedDict

    print("import os was successful")
    def check_warrior_default_modules_import():
        try:
            from warrior.Framework import Utils
        except Exception as e:
            e = str(e)
            if e.startswith("No module named 'warrior"):
                pkg_name = e.split("No module named")[-1].split("'")[1]
                pkg_parent = "warrior_" + pkg_name.split("warrior")[-1]
                pkg_full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "warrior_modules", pkg_parent)
                if os.path.exists(pkg_full_path):
                    if pkg_full_path not in sys.path:
                        sys.path.append(pkg_full_path)
                        check_warrior_default_modules_import()
                else:
                    print_error("{0}\n".format(str(e)))
            else:
                raise
        else:
            print("import Utils was successful")

    check_warrior_default_modules_import()

    from warrior.Framework import Utils
    from warrior.WarriorCore.Classes.rerun_testsuite import execute_failedsuite
    from warrior.WarriorCore.Classes.rerun_project import execute_failedproject

    print("Import rerun was successful")

    import shutil

    print("import shutil was successful")

    import warrior.Framework.Utils.email_utils as email

    print("import email was successful")

    from warrior.Framework.Utils.print_Utils import print_error, print_info, print_debug

    print("import print_Utils was successful")
    from warrior.WarriorCore import testcase_driver, testsuite_driver, project_driver

    print("import testcase_driver, testsuite_driver, project_driver were successful")
    from warrior.WarriorCore import ironclaw_driver, framework_detail

    print("import ironclaw_driver, framework_detail were successful")
    from warrior.WarriorCore.Classes.jira_rest_class import Jira

    print("import jira_rest_class was successful")
    from warrior.Framework.ClassUtils import database_utils_class

    print("import database_utils_class was successful")
    from xml.etree import ElementTree as et

    print("import element tree was successful")
except:
    print("\033[1;31m*********************************************")
    print(" !-Unable to import library in for Warrior Framework in warrior_cli_driver")
    print(" !-Successful imported libraries are printed above")
    print(" !-Please check your import statements for any code added to the framework")
    print(" !-Possible cause could be circular import")
    print("*********************************************\033[0m")
    raise

import re
import multiprocessing
from os.path import dirname, abspath
from warrior.Framework.Utils import config_Utils, file_Utils, xml_Utils
from warrior.Framework.Utils.data_Utils import get_credentials
import warrior.Framework.Utils.encryption_utils as Encrypt
from warrior.WarriorCore.Classes import war_cli_class

"""Handle all the cli command, new functions may be added later"""


def update_jira_by_id(jiraproj, jiraid, exec_dir, status):
    """ If jiraid is provided, upload the log and result file to jira """
    if jiraid is not False:
        jira_obj = Jira(jiraproj)
        if jira_obj.status is True:
            # Get the current jira issue status
            issue_status = jira_obj.get_jira_issue_status(jiraid)
            isReopend = False
            # Reopen the jira issue if it is closed, to upload the execution logs
            if issue_status and issue_status.lower() == "closed":
                print_info("Reopening Jira issue '{0}' to upload warrior "
                           "execution logs".format(jiraid))
                jira_obj.set_jira_issue_status(jiraid, "Reopened")
                isReopend = True
            # Upload execution logs
            zip_file = shutil.make_archive(exec_dir, 'zip', exec_dir)
            jira_obj.upload_logfile_to_jira_issue(jiraid, zip_file)
            # Close the jira issue if it is reopened in the above if block
            if isReopend is True:
                print_info("Closing Jira issue '{0}' which was reopened "
                           "earlier".format(jiraid))
                jira_obj.set_jira_issue_status(jiraid, "Closed")
            # Update Jira issue based on warrior execution status
            jira_obj.update_jira_issue(jiraid, status)
    else:
        print_info("jiraid not provided, will not update jira issue")


def add_live_table_divs(livehtmllocn, file_list):
    """
    add the divs for the live html table
    """
    root_attribs = {'id': 'liveTables'}
    root = Utils.xml_Utils.create_element("div", "", **root_attribs)

    # for each iteration create a div with id = the iteration number
    # the table for tis iteration will be added under this div

    for i in range(0, len(file_list)):
        marker_start = 'table-{0}starts'.format(str(i))
        marker_end = 'table-{0}ends'.format(str(i))
        div_attribs = {'id': str(i)}
        elem = Utils.xml_Utils.create_subelement(root, 'div', div_attribs)
        start_comment = Utils.xml_Utils.create_comment_element(marker_start)
        end_comment = Utils.xml_Utils.create_comment_element(marker_end)
        elem.append(start_comment)
        elem.append(end_comment)
        # write the tree to the file
        if isinstance(livehtmllocn, str):
            xml_Utils.write_tree_to_file(root, livehtmllocn)
        elif isinstance(livehtmllocn, multiprocessing.managers.DictProxy):
            livehtmllocn["html_result"] = xml_Utils.convert_element_to_string(root)


def file_execution(cli_args, abs_filepath, default_repo):
    """
        Call the corresponded driver of each file type
    """
    result = False
    a_defects = cli_args.ad
    jiraproj = cli_args.jiraproj
    jiraid = cli_args.jiraid

    if Utils.xml_Utils.getRoot(abs_filepath).tag == 'Testcase':
        default_repo['war_file_type'] = "Case"
        result, _, data_repository = testcase_driver.main(
            abs_filepath, data_repository=default_repo,
            runtype='SEQUENTIAL_KEYWORDS',
            auto_defects=a_defects, jiraproj=jiraproj, jiraid=jiraid)
        if not Utils.data_Utils.get_object_from_datarepository('genericdatafile'):
            update_jira_by_id(jiraproj, jiraid, os.path.dirname(
                data_repository['wt_resultsdir']), result)
            email.compose_send_email("Test Case: ", abs_filepath,
                                     data_repository['wt_logsdir'],
                                     data_repository['wt_resultsdir'], result)
    elif Utils.xml_Utils.getRoot(abs_filepath).tag == 'TestSuite':
        default_repo['war_file_type'] = "Suite"
        result, suite_repository = testsuite_driver.main(
            abs_filepath, auto_defects=a_defects,
            jiraproj=jiraproj, data_repository=default_repo)
        update_jira_by_id(jiraproj, jiraid,
                          suite_repository['suite_execution_dir'], result)
        email.compose_send_email("Test Suite: ", abs_filepath,
                                 suite_repository['ws_logs_execdir'],
                                 suite_repository['ws_results_execdir'], result)
    elif Utils.xml_Utils.getRoot(abs_filepath).tag == 'Project':
        default_repo['war_file_type'] = "Project"
        result, project_repository = project_driver.main(
            abs_filepath, auto_defects=a_defects,
            jiraproj=jiraproj, data_repository=default_repo)
        update_jira_by_id(jiraproj, jiraid,
                          project_repository['project_execution_dir'], result)
        email.compose_send_email("Project: ", abs_filepath,
                                 project_repository['wp_logs_execdir'],
                                 project_repository['wp_results_execdir'], result)
    else:
        print_error("Unrecognized root tag in the input xml file ! exiting!!!")

    return result


def group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj):
    """
        Process the parameter list and prepare environment for file_execution
    """
    livehtmllocn = cli_args.livehtmllocn
    abs_cur_dir = os.path.abspath(os.curdir)

    status = True

    iter_count = 0  ## this iter is used for live html results
    for parameter in parameter_list:
        default_repo = OrderedDict()
        result = False
        # check if the input parameter is an xml file
        if Utils.file_Utils.get_extension_from_path(parameter) == '.xml':
            filepath = parameter
            framework_detail.warrior_banner()
            abs_filepath = Utils.file_Utils.getAbsPath(filepath, abs_cur_dir)
            print_info('Absolute path: {0}'.format(abs_filepath))
            if Utils.file_Utils.fileExists(abs_filepath):
                if list(overwrite.items()):
                    default_repo.update(overwrite)

                if db_obj is not False and db_obj.status is True:
                    default_repo.update({'db_obj': db_obj})
                else:
                    default_repo.update({'db_obj': False})

                # pdate livehtmllocn to default repo
                if livehtmllocn or livehtmlobj is not None:
                    live_html_dict = {}
                    live_html_dict['livehtmllocn'] = \
                        livehtmllocn if livehtmlobj is None else livehtmlobj
                    live_html_dict['iter'] = iter_count

                    default_repo.update({'live_html_dict': live_html_dict})
                    if iter_count == 0 and livehtmlobj is None:
                        add_live_table_divs(livehtmllocn, parameter_list)
                    elif iter_count == 0 and livehtmlobj is not None:
                        add_live_table_divs(livehtmlobj, parameter_list)

                # Adding user repo's to pythonpath
                path_list = []
                if default_repo.get("pythonpath", False):
                    path_list = default_repo.get("pythonpath").split(":")
                    print_info("user repositories path list is {}".format(path_list))
                for path in path_list:
                    if os.path.exists(path):
                        sys.path.append(path)
                    else:
                        print_error("Given pythonpath doesn't exist : {}".format(path))
                result = file_execution(cli_args, abs_filepath, default_repo)
            else:
                print_error("file does not exist !! exiting!!")
        else:
            print_error("unrecognized file format !!!")
        status = status and result
        iter_count += 1
    return status


# def execution(parameter_list, a_defects, cse_execution, iron_claw,
#          jiraproj, overwrite, jiraid, dbsystem, livehtmllocn):
def execution(parameter_list, cli_args, overwrite, livehtmlobj):
    """Parses the input parameters (i.e. sys.argv)
        If the input parameter is an xml file:
            - check if file exists, if exists
                - if the input is a testcase xml file, execute the testcase
                - if the input is a testsuite xml file, excute the testsuite
                - if the input is a project xml file, excute the project
        If the input is not an xml file:
            - check if it is a json object/array respresenting a valid Warrior
            suite structure, if yes to execute a build
    Arguments:
        1. parameter_list = list of command line parameters supplied by
        the user to execute Warrior
    """
    if livehtmlobj:
        config_Utils.redirect_print.katana_console_log(livehtmlobj)

    if cli_args.version:
        framework_detail.warrior_framework_details()
        sys.exit(0)
    if not parameter_list:
        print_error("Provide at least one xml file to execute")
        sys.exit(1)

    iron_claw = cli_args.ironclaw
    dbsystem = cli_args.dbsystem

    status = False

    if iron_claw:
        status = ironclaw_driver.main(parameter_list)
    else:
        db_obj = database_utils_class.create_database_connection(dbsystem=dbsystem)
        status = group_execution(parameter_list, cli_args, db_obj, overwrite, livehtmlobj)

        if db_obj is not False and db_obj.status is True:
            db_obj.close_connection()

    return status


def warrior_execute_entry(*args, **kwargs):
    """
        main method
        filepath: required at least one
        auto_defects:
        version:
        iron_claw:
        jiraproj:
        overwrite:
        jiraid:
        dbsystem:
        livehtmllocn:
    """
    try:
        if len(sys.argv) >= 2:
            if sys.argv[1] == "-tc_gen":
                print_info("Initializing tc generator tool !!")

                tc_generator_dir_path = "WarriorTools/tc_generator"
                current_working_directory = dirname(dirname(abspath(__file__)))
                tc_generator_path = os.path.join(current_working_directory, tc_generator_dir_path)
                os.system("python {}/tc_generator {}".format(tc_generator_path, " ".join(sys.argv[2:])))
                sys.exit()

            if sys.argv[1] == "-warrior_py3_migration_tool":
                print_info("Initializing tc warrior_py3_migration_tool tool !!")
                war_path = dirname(dirname(abspath(__file__)))
                warrior_py3_migration_tool_path = "{}/WarriorTools/warrior_py3_migration_tools".\
                format(war_path)
                os.system("python {}/warrior_py3_migration_tool {}".format(warrior_py3_migration_tool_path,\
                 " ".join(sys.argv[2:])))
                sys.exit()

            if sys.argv[1] == "-rerun":
                print_info("Initializing the rerun feature  !!")
                try:
                    junit_path = sys.argv[2]
                    if os.path.exists(junit_path):
                        tree = et.parse(junit_path)
                        root = tree.getroot()
                        if root.tag.islower() and root.tag == "testsuites":
                            child_list = []
                            for child in root:
                                child_list.append(child.tag)
                            if "property" in child_list:
                                print_info("The Junit file provided is a project file")
                                execute_failedproject(junit_path)
                                sys.exit()
                            else:
                                print_info("The Junit file provided is a testsuite file")
                                execute_failedsuite(junit_path)
                                sys.exit()
                        else:
                            print_error("Invalid junit path")
                            sys.exit()
                    else:
                        print_error("Invalid junit path")
                except Exception as e:
                    print(e)
                    print_error("Junit Path is missing")
                    sys.exit()

        if not kwargs:
            # Launch from terminal/cli exeuction
            filepath, cli_args, overwrite = main(sys.argv[1:])
        else:
            args = [] if not args else args
            # Launch from python function call
            filepath, cli_args, overwrite = main(*args)
        livehtmlobj = kwargs.get("livehtmlobj", None)
        status = execution(filepath, cli_args, overwrite, livehtmlobj)
        status = {"true": True, "pass": True, "ran": True}.get(str(status).lower())
        # add code to send div finished using katana interface class

        if status is True:
            print_info("DONE 0")
            sys.exit(0)
        else:
            print_info("DONE 1")
            sys.exit(1)
    except:
        data_repo = config_Utils.data_repository
        if data_repo is not None:
            if 'war_parallel' in data_repo:
                if not data_repo['war_parallel']:
                    war_file_type = data_repo['war_file_type']
                    tc_junit_object = data_repo['wt_junit_object']
                    if war_file_type == "Case":
                        tc_junit_object.junit_output(data_repo['wt_resultsdir'])
                    elif war_file_type == "Suite":
                        tc_junit_object.junit_output(data_repo['wt_results_execdir'])
                    elif war_file_type == "Project":
                        tc_junit_object.junit_output(data_repo['wp_results_execdir'])


"""Handle all the cli command, new functions may be added later"""


def decide_runcat_actions(w_cli_obj, namespace):
    """Decide the actions to be taken for runcat tag """
    filepath = namespace.filepath

    if namespace.tcdir is not None and len(namespace.tcdir) == 0:
        namespace.tcdir = None

    if namespace.runcat and namespace.suitename is None:
        namespace.cat = namespace.runcat
        filepath = w_cli_obj.check_tag(namespace.cat, namespace.tcdir)

    elif namespace.runcat and namespace.suitename is not None and len(namespace.runcat) != 0:
        namespace.cat = namespace.runcat
        filepath = w_cli_obj.examine_create_suite(namespace)
        print_info("suite created in ", filepath[0])

    if len(filepath) == 0:
        print_error("No matching Testcases found for the provided category(ies)")
        exit(1)
    print_info("file path for runcat actions is ", str(filepath))
    return filepath


def decide_createsuite_actions(w_cli_obj, namespace):
    """Decide the actions for -createsuite tag """
    filepath = namespace.filepath

    # already check namespace.create here, no need to double check
    if namespace.filepath is not None and len(namespace.filepath) == 0:
        namespace.filepath = None

    if all([namespace.suitename, namespace.filepath]):
        filepath = w_cli_obj.examine_create_suite(namespace)
        print_info("suite created in ", filepath[0])
        exit(0)

    if all([namespace.suitename, namespace.cat]):
        filepath = w_cli_obj.examine_create_suite(namespace)
        print_info("suite created in ", filepath[0])
        exit(0)

    elif not namespace.cat and not all([namespace.suitename, namespace.filepath]):
        print_error("Invalid combination... Use -createsuite with -suitename, "
                    "filepath(s) (i.e. list of testcase xml files. "
                    "Use -h or --help for more command line options")
        exit(1)
    elif namespace.cat and not namespace.suitename:
        print_error("Invalid combination... Use -creatsuite + -category "
                    "with -suitename")
        exit(1)

    return filepath


def decide_ujd_actions(w_cli_obj, namespace):
    """Decide upload jira objects actions """
    if namespace.ujd and any([namespace.ddir, namespace.djson]):
        if namespace.ddir is not None and namespace.djson is None:
            w_cli_obj.manual_defects("dir", namespace.ddir, jiraproj=namespace.jiraproj)
        elif namespace.djson is not None and namespace.ddir is None:
            w_cli_obj.manual_defects("files", namespace.djson, jiraproj=namespace.jiraproj)
        elif namespace.ddir is not None and namespace.djson is not None:
            print_error("Use -ujd with one of -ddir or -djson  not both")
        exit(0)
    elif namespace.ujd and not any([namespace.ddir, namespace.djson]):
        print_error("Use -ujd with one of -ddir or -djson")
        exit(1)


def decide_overwrite_var(namespace):
    """options provided in cli get preference over the ones provided inside tests
    """
    overwrite = {}
    if namespace.datafile:
        if namespace.datafile[0] != os.sep:
            namespace.datafile = os.getcwd() + os.sep + namespace.datafile
        overwrite['ow_datafile'] = namespace.datafile
    #namespace for mapfile
    if namespace.mapfile:
        if namespace.mapfile[0] != os.sep:
            namespace.mapfile = os.getcwd() + os.sep + namespace.mapfile
        overwrite['ow_mapfile'] = namespace.mapfile
    # namespace for wrapperfile
    if namespace.wrapperfile:
        if namespace.wrapperfile[0] != os.sep:
            namespace.wrapperfile = os.getcwd() + os.sep + namespace.wrapperfile
        overwrite['ow_testwrapperfile'] = namespace.wrapperfile

    # namespace for random tc execution
    if namespace.random_tc_execution:
        overwrite['random_tc_execution'] = namespace.random_tc_execution

    if namespace.resultdir:
        if namespace.resultdir[0] != os.sep:
            namespace.resultdir = os.getcwd() + os.sep + namespace.resultdir
        overwrite['ow_resultdir'] = namespace.resultdir
    if namespace.logdir:
        if namespace.logdir[0] != os.sep:
            namespace.logdir = os.getcwd() + os.sep + namespace.logdir
        overwrite['ow_logdir'] = namespace.logdir
    if namespace.outputdir:
        if namespace.outputdir[0] != os.sep:
            namespace.outputdir = os.getcwd() + os.sep + namespace.outputdir
        overwrite['ow_resultdir'] = namespace.outputdir
        overwrite['ow_logdir'] = namespace.outputdir
    if all([namespace.outputdir, any([namespace.resultdir, namespace.logdir])]):
        print_error("outputdir shouldn't be used with resultdir or logdir")
        exit(1)
    if namespace.jobid:
        #settings_xml = Tools.__path__[0] + os.sep + 'w_settings.xml'
        settings_xml = os.getenv("WAR_TOOLS_DIR") + os.sep + 'w_settings.xml'
        job_url = get_credentials(settings_xml, 'job_url', ['url'], 'Setting')
        if job_url['url'] is not None:
            url = job_url['url']
        else:
            print_debug("jobid is specified but no job url found in w_settings")
            print_info("Using jobid only in JUnit file")
            url = ""
        overwrite['jobid'] = url + str(namespace.jobid)
    if namespace.pythonpath:
        overwrite['pythonpath'] = namespace.pythonpath

    if namespace.genericdatafile:
        overwrite['genericdatafile'] = namespace.genericdatafile
    if namespace.gen_no_of_samples:
        overwrite['gen_no_of_samples'] = namespace.gen_no_of_samples
    if namespace.gen_select_rows:
        overwrite['gen_select_rows'] = namespace.gen_select_rows
    if namespace.gen_shuffle_columns:
        overwrite['gen_shuffle_columns'] = namespace.gen_shuffle_columns
    if namespace.gen_purge_db:
        overwrite['gen_purge_db'] = namespace.gen_purge_db
    if namespace.gen_exec_tag:
        overwrite['gen_exec_tag'] = namespace.gen_exec_tag
    if namespace.gen_report:
        overwrite['gen_report'] = namespace.gen_report

    return overwrite


def append_path(filepath, path_list, path):
    """Append appropriate paths for testcase/suite/project in test folder
    """
    temp_list = []
    for file_name in path_list:
        file_name = path + file_name
        temp_list.append(file_name)
    if temp_list:
        filepath.extend(temp_list)
    return filepath


def decide_action(w_cli_obj, namespace):
    """Prepare filepath and other arguments for Warrior main to use"""
    # First level, sleep

    #setenv varibles by cli
    if namespace.setenv:
        env_vir_list = [x.strip() for x in namespace.setenv.split(',')]
        for env_vir in env_vir_list:
            env_val_splt = env_vir.split(':')
            env_vir_name = env_val_splt[0]
            env_vir_val = env_val_splt[1]
            # env_name = env_val_splt[0].strip('"\'')
            # env_val = env_val_splt[1].strip('"\'')
            os.environ[env_vir_name] = env_vir_val

    if namespace.target_time:
        w_cli_obj.gosleep(namespace.target_time)

    # Second level, decide filepath
    cli_args = [namespace.kwparallel, namespace.kwsequential,
                namespace.tcparallel, namespace.tcsequential,
                namespace.RMT, namespace.RUF]
    filepath = namespace.filepath

    # runcat related actions
    if namespace.runcat:
        filepath = decide_runcat_actions(w_cli_obj, namespace)

    elif namespace.create:
        filepath = decide_createsuite_actions(w_cli_obj, namespace)

    elif namespace.encrypt:
        status = True
        encoded_key = False
        if namespace.secretkey:
            # Checks if User has given a string for creating a secret key
            status, encoded_key = Encrypt.set_secret_key(namespace.secretkey)
        else:
            # If secret key has not been given, checks for the existence of the
            # secret.key file
            #path = file_Utils.get_parent_dir(os.path.realpath(__file__),
            #                                 "WarriorCore")
            #path = os.path.join(path, "Tools", "admin", "secret.key")
            path = os.path.join(os.getenv("WAR_TOOLS_DIR"), "admin", "secret.key")
            if not os.path.exists(path):
                print_error("Could not find the secret.key file in Tools/Admin!"
                            " Please use '-secretkey your_key_text' in the "
                            "-encrypt command for creating the file!")
                status = False
        if status:
            # sends secret key and plain text password for encryption
            message = Encrypt.encrypt(namespace.encrypt[0], encoded_key)
            # Checks if message is not hexadecimal
            if re.match(r".*[g-z].*", message):
                print_error(message)
            else:
                print_info("The encrypted text for '{0}' is: {1}".
                           format(namespace.encrypt[0], message))
                exit(0)
        else:
            print_error("Encrypted text could not be generated.")
            exit(1)

    elif namespace.decrypt:
        status = True
        encoded_key = False
        if namespace.secretkey:
            # Checks if User has given a string for creating a secret key
            status, encoded_key = Encrypt.set_secret_key(namespace.secretkey)
        else:
            # If secret key has not been given, checks for the existence of the
            # secret.key file
            #path = file_Utils.get_parent_dir(os.path.realpath(__file__),
            #                                 "WarriorCore")
            #path = os.path.join(path, "Tools", "admin", "secret.key")
            path = os.path.join(os.getenv("WAR_TOOLS_DIR"), "admin", "secret.key")
            if not os.path.exists(path):
                print_error("Could not find the secret.key file in Tools/Admin!"
                            " Please use '-secretkey your_key_text' in the "
                            "-encrypt command for creating the file!")
                status = False
        if status:
            # sends secret key and encrypted text password for decryption
            message = Encrypt.decrypt(namespace.decrypt[0], encoded_key)
            print_info("The decrypted text for '{0}' is: {1}". \
                       format(namespace.decrypt[0], message))
            exit(0)
        else:
            print_error("Decrypted text could not be generated.")
            exit(1)

    elif any(cli_args):
        filepath = w_cli_obj.examine_cli_args(cli_args, namespace)

    elif namespace.ujd:
        decide_ujd_actions(w_cli_obj, namespace)

    # append additional path
    if namespace.tc_name is not None:
        filepath = append_path(filepath, namespace.tc_name, "Warriorspace/Testcases/")
    if namespace.ts_name is not None:
        filepath = append_path(filepath, namespace.ts_name, "Warriorspace/Suites/")
    if namespace.proj_name is not None:
        filepath = append_path(filepath, namespace.proj_name, "Warriorspace/Projects/")

    # overwrite layer
    overwrite = decide_overwrite_var(namespace)

    if filepath is None:
        print_error("No input filepath: {0}".format(namespace.filepath))
        exit(1)
    else:
        for index, file_name in enumerate(filepath):
            if len(file_name.split('.')) == 1:
                filepath[index] = file_name + '.xml'

    return (filepath, namespace, overwrite)


def main(args):
    """init a Warrior Cli Class object, parse its arguments and run it"""
    w_cli_obj = war_cli_class.WarriorCliClass()
    parsed_args = w_cli_obj.parser(args)
    return decide_action(w_cli_obj, parsed_args)


if __name__ == "__main__":
    print(re.match(r"[g-z]", input("Enter: ")))
    main(sys.argv[1:])

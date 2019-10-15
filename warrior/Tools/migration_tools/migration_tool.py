#!/usr/bin/python

#This script add the user repository name according to the drivers in Testcase file

import sys
import os
import re
import ast
import time
import argparse
import subprocess
from datetime import datetime
current_working_directory = os.getcwd()


warrior_actions = ["CiRegressionActions", "CliActions", "CloudshellActions", "CommonActions", "DemoActions",
                   "ExampleActions", "FileActions", "GnmiActions", "KafkaActions", "LogActions", "NetconfActions",
                   "NetworkActions", "RestActions", "SeleniumActions", "ServerActions", "SnmpActions", "WappActions"]
warrior_actions_classes = ["ci_regression_actions", "cli_actions", "cloudshell_actions", "common_actions",
                           "demo_actions", "example_actions", "file_actions", "gnmi_actions", "kafka_actions",
                           "log_actions", "netconf_Actions", "connection_actions", "diagnostics_actions",
                           "file_ops_actions", "rest_actions", "browser_actions", "elementlocator_actions",
                           "elementoperation_actions", "verify_actions", "wait_actions", "server_actions",
                           "common_snmp_actions", "wapp_reporting_actions"]
warrior_utils = ["cli_Utils", "config_Utils", "csv_Utils", "data_Utils", "datetime_utils", "demo_utils", "dict_Utils",
                 "driver_Utils", "email_utils", "encryption_utils", "file_Utils", "import_utils", "list_Utils",
                 "print_Utils", "rest_Utils", "selenium_Utils", "snmp_utils", "string_Utils", "telnet_Utils",
                 "testcase_Utils", "xml_Utils"]
warrior_framework_classes = ["configuration_element_class", "database_utils_class", "gnmi_utils_class",
                             "json_utils_class", "kafka_utils_class", "netconf_utils_class", "rest_server_class",
                             "rest_utils_class", "snmp_utility_class", "ssh_util_class", "testdata_class",
                             "xl_utils_class"]
builtin_modules = ["os", "collections", "pexpect", "time", ""]
warrior_cli_utils = ["base_class", "connection", "diagnostics", "file_ops", "loging", "network_class","warrior_cli_class"]


class Add_Repo_in_StepSection(object):


    def __init__(self, warrior_repo=None, Keyword_repos=None, add_repo_output=None,\
     imp_url=None, user_repo_path=None, imp_output_dir=None, add_repo_war_repos_path=None, add_repo_kw_repos_path=None):
        self.warrior_repo = warrior_repo
        self.Keyword_repos = Keyword_repos
        self.add_repo_output = add_repo_output
        self.imp_url = imp_url
        self.user_repo_path = user_repo_path
        self.imp_output_dir = imp_output_dir
        self.add_repo_war_repos_path = add_repo_war_repos_path
        self.add_repo_kw_repos_path = add_repo_kw_repos_path


    def add_repo_in_step(self, war_dir_path=None):
        '''
        This definition will find the number of drivers present in a testcase file
        '''
        if self.add_repo_war_repos_path:
            print("add_repo_war_repos_path", self.add_repo_war_repos_path)
            # path = self.add_repo_war_repos_path

            print("Provided path :", self.add_repo_war_repos_path)
            print("Finding the xml files.....")
            for root, dirs, files in os.walk(self.add_repo_war_repos_path):
                count = 0
                for file in files:
                    if file.endswith('.xml'):

                        #heare opening the file which ends with .xml
                        with open((root +"/"+ file),"r") as reading_file:
                            print("Found the xml file to read", file)
                            lines = reading_file.read()

                            stp = re.findall('<step Driver="([a-zA-Z0-9_]+)" Keyword=', lines)
                            self.drivers = list(set(stp))

                            #heare passing the driver to the get_repo_name definition and collecting the dictionary
                            repo_driver_dict = self.get_repo_name()

                            print("Adding the repo name under step section")

                            #heare adding the repo in mathced places 
                            for driver_item in repo_driver_dict.keys():
                                if repo_driver_dict[driver_item] != "warroir":   
                                    exist_str = '<step Driver="%s"' % driver_item 
                                    new_str = '<step Driver="%s" Repo="%s"' %(driver_item, 
                                        repo_driver_dict[driver_item])
                                    lines = re.sub(exist_str, new_str, lines)

                        #here writing modified lines into .xml file
                        with open((root +"/"+ file),"w") as writing_file:
                           writing_file.write(lines)
            print("successfully completed the adding Repo under all Testcase files.")
            print("The resuls present in ", self.add_repo_output)
            sys.exit()

        self.warrior_repo = war_dir_path
        path = self.warrior_repo
        print("Provided path :", self.warrior_repo)
        print("Finding the xml files.....")
        for root, dirs, files in os.walk(self.warrior_repo):
            count = 0
            for file in files:
                if file.endswith('.xml'):

                    #heare opening the file which ends with .xml
                    with open((root +"/"+ file),"r") as reading_file:
                        print("Found the xml file to read", file)
                        lines = reading_file.read()

                        stp = re.findall('<step Driver="([a-zA-Z0-9_]+)" Keyword=', lines)
                        self.drivers = list(set(stp))

                        #heare passing the driver to the get_repo_name definition and collecting the dictionary
                        repo_driver_dict = self.get_repo_name()

                        print("Adding the repo name under step section")

                        #heare adding the repo in mathced places 
                        for driver_item in repo_driver_dict.keys():
                            if repo_driver_dict[driver_item] != "warroir":   
                                exist_str = '<step Driver="%s"' % driver_item 
                                new_str = '<step Driver="%s" Repo="%s"' %(driver_item, 
                                    repo_driver_dict[driver_item])
                                lines = re.sub(exist_str, new_str, lines)

                    #here writing modified lines into .xml file
                    with open((root +"/"+ file),"w") as writing_file:
                       writing_file.write(lines)
        print("successfully completed the adding Repo under all Testcase files.")
        print("The resuls present in ", self.add_repo_output)


    def get_repo_name(self):
        '''
        In this definition finding the repo name
        '''
        path = os.getcwd()
        driver_repo_dict = {}

        for driver in self.drivers:
            print("Found the Driver present in xml file", driver)
            driver_file = driver+".py"
            for root, dirs, files in os.walk(path):
                for file in files:
                    if (file.endswith('.py') and file != "__init__.py"):
                        if file == driver_file:
                            driver_repo = (os.path.abspath(os.path.join(root, os.pardir)))
                            driver_repo_name = driver_repo.split('/')[-1]
                            driver_repo_dict[driver]=driver_repo_name
                            print("Found the repo name of the Driver", driver_repo_name)
        return driver_repo_dict


    def repo_clone(self):

        # self.warrior_repo = self.warrior_repo.replace("/", "")
        self.warrior_repo_name = self.warrior_repo.split("/")[-1].split(".")[0]
        keyword_repo_names = ast.literal_eval(self.Keyword_repos)
        keyword_repo_name = ", ".join( repr(e) for e in keyword_repo_names )
        self.all_kw_repos_names = []
        repo_names = keyword_repo_name.split(' ')
        for repo in repo_names:
            rep = repo.replace('"', '').replace("'", '')
            kw_dir_name = rep.split("/")[-1].split(".")[0]
            self.all_kw_repos_names.append(kw_dir_name)

        print("warrior_repo_name", self.warrior_repo_name)
        print("all_kw_repos_names", self.all_kw_repos_names)

        def get_immediate_subdirectories_in_output_dir(self):
            try:

                current_wkdir = os.getcwd()
                print("current working directory is",current_wkdir)
                c = current_wkdir.replace("'", "")

                dir_names = []

                for name in os.listdir(current_wkdir):
                    dir_names.append(name)

                self.all_kw_dirs_in_repo = []
                for dir_name in dir_names:
                    if dir_name == self.warrior_repo_name:
                        war_dir_path = os.getcwd()+"/"+dir_name
                        print("warrior directory path is ", war_dir_path)

                    for kw in self.all_kw_repos_names:
                        if dir_name == kw:
                            dir_path = os.getcwd()+"/"+kw
                            self.all_kw_dirs_in_repo.append(dir_path)

                return war_dir_path, self.all_kw_dirs_in_repo

            except Exception as e:
                print("No cloned repos are presented in current directory!!!")
                print("Error is ", e)


        if self.add_repo_output == None:
            new_dir = os.path.join(os.getcwd(), "Add_repo_name_"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

            try:
                os.mkdir(new_dir)
                os.chdir(new_dir)
                self.add_repo_output = os.getcwd()
                print("Created result directory is ", self.add_repo_output)
                print("******************************************************************************")
                print("Result directory is ", new_dir)
                print("******************************************************************************")
            except Exception as e:
                print("directory alredy present. Please try with diffrent!!!", e)

        
        try:
            out_dir = self.add_repo_output
            os.chdir(out_dir)
            print("Provided output directory is", self.add_repo_output)
            print("******************************************************************************")
            print("Result directory is ", os.getcwd())
            print("******************************************************************************")
        except Exception as e:
            print("provded directory is not present. Please try with diffrent directory!!!")
            print("Erropr is ",e)
            raise

        try:
            print(" warrior repo is ", self.warrior_repo)
            # self.warrior_repo = self.warrior_repo.replace("/", "")
            print("cloning Warror/warroirspace repository. Please wait....")
            gitimpo.Git(self.add_repo_output).clone(self.warrior_repo)
            print("successfully cloned Warror/warroirspace repository")
            print("cloning Keywords repositories")

            list_kw_urls = self.Keyword_repos.split(" ")
            all_kw_dirs = []

            i = 0
            for u in list_kw_urls:
                kw_url = list_kw_urls[i]
                u_r_l = kw_url.replace('[', '').replace(']', '').replace("'", '').replace(',', '')
                repo_name = kw_url.split("/")[-1].split(".")[0]
                print("cloning the warrior Keyword repo. Please wait....")
                print("clong repo is ",u_r_l)
                all_kw_dirs.append(u_r_l)
                gitimpo.Git(self.add_repo_output).clone(u_r_l)
                print("successfully cloned Warror Keyword repo",u_r_l)
                i = i+1
            print("successfully cloned Keywords repository(s)!!")
        except Exception as e:
            print("################################################################")
            print("repository(s) alredy present in this directory")
            print("#################################################################")
            print("Error ", e)
            sys.exit()
        self.war_dir_path, self.all_kw_dirs_in_repo = get_immediate_subdirectories_in_output_dir(self)
        self.add_repo_in_step(self.war_dir_path)


class Verify_Import_Statements(object):

    def __init__(self, user_repo_path):
        self.user_repo_path = user_repo_path


    def check_for_statement_is_available_in_user_repo(self, line, user_repo_path):
        self.user_repo_path = user_repo_path

        line = line.strip()
        if line.startswith("from"):
            import_words = line.split()[1].split(".")
            after_imports = line.split()[-1]
            if "," in after_imports:
                after_imports = after_imports.split(",")[-1]
            else:
                pass
            if after_imports in warrior_utils:
                return "warrior"

            abs_path = "/".join(import_words)
            actual_path = os.path.join(self.user_repo_path, abs_path)
            directory_name = os.path.split(self.user_repo_path)[-1]
            if os.path.exists(actual_path) or os.path.exists("{}.py".format(actual_path)):
                return directory_name
            else:
                return "warrior"
        elif line.strip().startswith("import"):
            import_words = line.strip("import").strip().split(".")
            abs_path = "/".join(import_words)
            actual_path = os.path.join(self.user_repo_path, abs_path)
            directory_name = os.path.split(self.user_repo_path)[-1]
            if os.path.exists(actual_path) or os.path.exists("{}.py".format(actual_path)):
                return directory_name
            else:
                return "warrior"

        else:
            return "not valid"


    def verify_import_statements(self):
        if os.path.exists(self.user_repo_path):

            directory_name = os.path.split(self.user_repo_path)[-1]
            for root, dirs, files in os.walk(self.user_repo_path):
                if root.endswith(directory_name) and "__init__py" not in files:
                    cmd = "touch  {}/__init__.py".format(self.user_repo_path)
                    os.system(cmd)

                for file in files:

                    if file == "__init__.py":
                        pass
                    elif file.endswith(".py"):

                        fd = open(root + "/" + file, "r+")
                        file_lines = fd.readlines()
                        for fline in file_lines:
                            if fline.startswith("class"):
                                break
                            if fline[:-1] == "import Framework.Utils as Utils" or re.search(
                                    "\s*import Framework.Utils as Utils", fline[:-1]):
                                fline = fline[:-1]
                                a = "sed -i 's/import Framework.Utils as Utils/import warrior.Framework.Utils as Utils/g' {}".format(
                                    root + "/" + file)
                                os.system(a)
                            elif fline[:-2] == "import Framework.Utils as Utils" or re.search(
                                    "\s*import Framework.Utils as Utils", fline[:-2]):
                                fline = fline[:-2]
                                a = "sed -i 's/import Framework.Utils as Utils/import warrior.Framework.Utils as Utils/g' {}".format(
                                    root + "/" + file)
                                os.system(a)
                            elif "Framework" in fline:
                                if "\r" in fline:
                                    fline = fline[:-2]
                                else:
                                    fline = fline[:-1]
                                repo_name = self.check_for_statement_is_available_in_user_repo(fline, self.user_repo_path)
                                if repo_name == "warrior":
                                    warrior_flag = True
                                    user_repo_flag = False
                                    other_flag = True
                                elif repo_name=="not valid":
                                    other_flag = False
                                else:
                                    user_repo_flag = True
                                    warrior_flag = False
                                    other_flag = True

                                if "from" in fline:
                                    cd = fline.split("from")[1]
                                    if cd.strip().startswith("Framework"):
                                        aa = fline.split("import")[0].strip().split(".")[-1]
                                        if (aa in warrior_utils or aa in warrior_cli_utils) and warrior_flag:
                                            ffline = re.sub("Framework", "warrior.Framework", fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file, )
                                            os.system(a)
                                        elif fline.split()[-1] in warrior_utils and warrior_flag:
                                            ffline = re.sub("Framework", "warrior.Framework", fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file, )
                                            os.system(a)
                                        elif fline.split(".")[-1].split()[0] in warrior_framework_classes and warrior_flag:
                                            ffline = re.sub("Framework", "warrior.Framework", fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file, )
                                            os.system(a)

                                        elif user_repo_flag:
                                            ffline = re.sub("Framework", "{}.Framework".format(directory_name), fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                            os.system(a)
                                        elif other_flag:
                                            print("Not found  statement {} in user repo or warrior and file name {}".
                                                  format(fline.strip(), file))

                            elif "Actions" in fline:
                                if "\r" in fline:
                                    fline = fline[:-2]
                                else:
                                    fline = fline[:-1]
                                repo_name = self.check_for_statement_is_available_in_user_repo(fline, self.user_repo_path)
                                if repo_name == "warrior":
                                    warrior_flag = True
                                    user_repo_flag = False

                                else:
                                    user_repo_flag = True
                                    warrior_flag = False
                                if "from" in fline:
                                    cd = fline.split("from")[1]
                                    if cd.strip().startswith("Actions"):
                                        aa = fline.split("import")[0].strip().split(".")[-1]
                                        if aa in warrior_actions or aa in warrior_actions_classes and warrior_flag:
                                            ffline = re.sub("Actions", "warrior.Actions", fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                            os.system(a)
                                        elif user_repo_flag:
                                            ffline = re.sub("Actions", "{}.Actions".format(directory_name), fline, 1)
                                            a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                            os.system(a)
                                        else:
                                            print("not able too find {} and file {}".format(fline, file))
                                elif fline.startswith("import"):
                                    if fline.split(".")[-1] in warrior_actions and warrior_flag:
                                        ffline = re.sub("Actions", "warrior.Actions".format(directory_name), fline, 1)
                                        a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                        os.system(a)
                                    elif user_repo_flag:
                                        ffline = re.sub("Actions", "{}.Actions".format(directory_name), fline, 1)
                                        a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                        os.system(a)
                                    else:

                                        print("not able to find {} and file {}".format(fline, file))
                                else:
                                    if "[Actions" in fline:
                                        pattern = "\s*package_list\s*\=\s*\[Actions.*\.(\w+)\]"
                                        match = re.search(pattern, fline)
                                        fline = fline.replace("[", r"\[")
                                        if match:
                                            if match.group(1) in warrior_actions:
                                                ffline = re.sub("Actions", "warrior.Actions".format(directory_name), fline,
                                                                1)
                                                awe = """sed -i 's/{}/{}/g' {}""".format(fline.strip(), ffline.strip(),
                                                                                         root + "/" + file)
                                                os.system(awe)
                                            else:
                                                ffline = re.sub("Actions", "{}.Actions".format(directory_name), fline, 1)
                                                af = """sed -i 's/{}/{}/g' {}""".format(fline.strip(), ffline.strip(),
                                                                                        root + "/" + file)
                                                os.system(af)

                            elif fline.startswith("WarriorCore"):
                                if "\r" in fline:
                                    fline = fline[:-2]
                                else:
                                    fline = fline[:-1]
                                ffline = re.sub("WarriorCore", "warrior.WarriorCore", fline, 1)
                                a = """sed -i 's/{}/{}/g' {}""".format(fline, ffline, root + "/" + file)
                                os.system(a)
        else:
            print("path not found")




#Argparser to add command line argumets
parser = argparse.ArgumentParser()
parser.add_argument('--imp_url', "-iu",type = str, help="git/bitbucket repo cloning url")
parser.add_argument('--imp_output_dir', "-iod", type = str, help="import changes to store the output directory ")
parser.add_argument('--imp_user_repo_path',"-iurp", type=str, help="user repo name including \
 absolute path")

parser.add_argument("--add_repo_warrior_url", "-arwu", type = str, help = "Enter the absolute url link of user\
 repository of Warrorspace/xml files ") 
parser.add_argument("--add_repo_keyword_url", "-arku",nargs='*', type = str, help = "Enter the absolute url link\
 of user repository of Keyword files") 
parser.add_argument("--add_repo_output_dir", "-arod", type = str, help = "Enter the absolute path to \
    create output directory of added repo name under StepSection files")
parser.add_argument("--add_repo_war_repos_path", "-arwrp", type = str, help = "Enter the absolute path to \
    add repo name in keyword repos paths")
parser.add_argument("--add_repo_kw_repos_path", "-arkrp", type = str, help = "Enter the absolute path to \
    add repo name in keyword repos paths")


args = parser.parse_args()

imp_url = args.imp_url
imp_output_dir = args.imp_output_dir
user_repo_path = args.imp_user_repo_path  

warrior_repo = args.add_repo_warrior_url
Keyword_repos = args.add_repo_keyword_url
add_repo_war_repos_path = args.add_repo_war_repos_path
add_repo_kw_repos_path = args.add_repo_kw_repos_path
add_repo_output = args.add_repo_output_dir



class Pre_requirements(object):

                       
    def __init__(self, warrior_repo=None, Keyword_repos=None, add_repo_output=None, imp_url=None,\
     user_repo_path=None,  imp_output_dir=None, add_repo_war_repos_path=None, add_repo_kw_repos_path=None):
        self.warrior_repo = warrior_repo
        self.Keyword_repos = Keyword_repos
        self.add_repo_output = add_repo_output
        self.add_repo_war_repos_path = add_repo_war_repos_path
        self.add_repo_kw_repos_path = add_repo_kw_repos_path

        self.imp_url = imp_url
        self.user_repo_path = user_repo_path
        self.imp_output_dir = imp_output_dir



    def check_packages(self, str_package):
        """ Checks if the specified python package is installed.
        return type: boolean
        :Arguments:
        1. str_package (str) = name of the package to be checked
        :Returns:
        bool = True/False
        """
        try:
            import imp
            imp.find_module(str_package)
            bool_found = True
        except ImportError:
            bool_found = False
        return bool_found

    def check_git_status(self):
        try:
            null = open("/dev/null", "w")
            sp_output = subprocess.Popen("git", stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE, shell=True)
            null.close()
            output = sp_output.stdout.read()
            print(output)
            return True

        except OSError:
            return False

    def activate_virtualenv(self):
        '''Activate virtual environment to add dependencies
        '''
        virt_name = "namespace_venv"
        ve_dest = os.path.join(current_working_directory, virt_name)
        print("ve_name: "+virt_name, )
        print("destination: "+ve_dest,)
        try:
            venv_cmd = os.path.expanduser("~/.local/bin/virtualenv")
            subprocess.check_call([venv_cmd, "--system-site-packages", ve_dest])
            venv_file = "{}/bin/activate_this.py".format(ve_dest)
            exec(compile(open(venv_file).read(), venv_file, 'exec'), dict(__file__=venv_file))
            return True
        except Exception as e:
            print_error("Activating virtual env at {} resulted in exception {}".format(
                                                    ve_dest, e), logfile, print_log_name)
            print_error("Check {} is a proper virtualenv binary".format(ve_loc),
                        logfile, print_log_name)
            setDone(1)
            return False

    def install_depen(self, dependency, dependency_name):
        """ This function checks if a dependency was installed. If not,
         then it raises an error.
        """
        counter = 0
        pip_cmds = ['pip', 'install', dependency]
        try:
            print("installing "+dependency)
            sp_output = subprocess.Popen(pip_cmds, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            output, error = sp_output.communicate()
            if "Requirement already satisfied" in output or "Successfully installed GitPython"\
             in output:
                print(" was able to install " + dependency_name)
                return True
            return_code = sp_output.returncode
            if return_code > 0:
                print(output, error)
        except IOError:
            counter = 1
            print("unable to install " + dependency_name )
        except:
            counter = 1
            print("unable to install " + dependency_name )
        if counter == 0:
            try:
                sp_output = subprocess.Popen(["pip", "show", dependency_name], stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = sp_output.stdout.read()
                if output == "":
                    print(dependency_name + " could not be installed!!" )
                else:
                    print(dependency_name + " installation complete!",
                               logfile, print_log_name)
            except:
                print("wasn't able to determine if " + dependency_name)

    def add_repo_in_step_repos(self):

        if (self.add_repo_war_repos_path and self.add_repo_kw_repos_path and self.add_repo_output) or (self.add_repo_war_repos_path and self.add_repo_kw_repos_path):

            print("Got the user repo paths. proceeding further!!")
            print("add_repo_war_repos_path is ",self.add_repo_war_repos_path)
            if self.add_repo_output:
                try:
                    rep = self.add_repo_war_repos_path.split("/")[-1]
                    print("Provided output path is", self.add_repo_output)
                    os.system("cp -r {} {}".format(self.add_repo_war_repos_path, self.add_repo_output))
                    self.add_repo_war_repos_path = self.add_repo_output+"/"+rep
                    repos_paths = self.add_repo_kw_repos_path.split(" ")
                    li = []
                    for repo_kw in repos_paths:
                        rep = repo_kw.split("/")[-1]
                        os.system("cp -r {} {}".format(repo_kw, self.add_repo_output))
                        d = self.add_repo_output+"/"+rep
                        li.append(d)
                    self.add_repo_kw_repos_path = li
                except:
                    print("Please provider correct output directory!!")
            else:
                new_dir = os.path.join(os.getcwd(), "Add_repo_name_in_repos"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

                try:
                    os.mkdir(new_dir)
                    os.chdir(new_dir)
                    self.add_repo_output = os.getcwd()
                    try:
                        rep = self.add_repo_war_repos_path.split("/")[-1]
                        print("Provided output path is", self.add_repo_output)
                        os.system("cp -r {} {}".format(self.add_repo_war_repos_path, self.add_repo_output))
                        self.add_repo_war_repos_path = self.add_repo_output+"/"+rep

                        repos_paths = self.add_repo_kw_repos_path.split(" ")
                        li = []
                        for repo_kw in repos_paths:
                            rep = repo_kw.split("/")[-1]
                            os.system("cp -r {} {}".format(repo_kw, self.add_repo_output))
                            d = self.add_repo_output+"/"+rep
                            li.append(d)
                        self.add_repo_kw_repos_path = li

                    except:
                        print("Please provider correct output directory!!")

                    print("Created result directory is ", self.add_repo_output)
                    print("******************************************************************************")
                    print("Result directory is ", new_dir)
                    print("******************************************************************************")
                except Exception as e:
                    print("directory alredy present. Please try with diffrent!!!", e)

            Repo_adding = Add_Repo_in_StepSection(warrior_repo, Keyword_repos, add_repo_output, \
                imp_url, user_repo_path, imp_output_dir, add_repo_war_repos_path, add_repo_kw_repos_path)
            Repo_adding.add_repo_in_step()
            sys.exit()

    def add_repo_in_step_starts(self):

        print("Got user repo urls. proceeding further!!")
        print("Provided warroir repository link is ", self.warrior_repo)
        print("Provided Keywords repository link is ", self.Keyword_repos)

        flag = False
        packages = ["pip", "git"]
        if self.warrior_repo and self.Keyword_repos:
            flag = True
            if hasattr(sys, 'real_prefix'):
                pass
                git_status = self.check_git_status()
                if git_status:
                    print("Git is available proceeding further ")
                else:
                    print("Git is not installed on the system. "
                          "Please install git and restart this installation.")
                self.install_depen("GitPython", "git")
                import git as gitimpo
                global gitimpo
            else:
                bool_found = self.check_packages("pip")
                if not bool_found :
                    print("pip is not installed ")
                else:
                    print("pip is installed proceeding further !!!")
                git_status = self.check_git_status()
                if git_status:
                    print("Git is available proceeding further ")
                else:
                    print("Git is not installed on the system. "
                          "Please install git and restart this installation.")
                self.install_depen("virtualenv", "virtualenv")
                self.activate_virtualenv()
                self.install_depen("GitPython", "git")
                import git as gitimpo
                global gitimpo


        Repo_adding = Add_Repo_in_StepSection(warrior_repo, Keyword_repos, add_repo_output, \
            imp_url, user_repo_path, imp_output_dir, add_repo_war_repos_path, add_repo_kw_repos_path)

        Repo_adding.repo_clone()


    def verify_import_statements_starts(self):

        if self.imp_url:
            print("got url as argument ..proceeding further ")

        elif self.user_repo_path:
            print("got user_repo_path as argument ..proceeding further ")
            verify = Verify_Import_Statements(self.user_repo_path)

            if self.imp_output_dir:
                if os.path.exists(self.imp_output_dir):
                    pass
                else:
                    print("given path not found ")
                    os.remove()
                    sys.exit()

                parent_dir = self.user_repo_path.split("/")
                parent_path = "/".join(parent_dir[:-1])
                os.chdir(parent_path)
                new_dir = "results_time"
                os.mkdir("results_time")
                os.system("cp -r {} {}".format(self.user_repo_path.split("/")[-1], new_dir))
                wew = "{}/{}".format(new_dir, parent_dir[-1])
                self.user_repo_path = os.path.join(os.getcwd(),wew)
            verify.verify_import_statements()
            if self.imp_output_dir:
                text = self.user_repo_path.split("/")
                final_path = "/".join(text[:-1])
                os.system("mv {} {}".format(final_path, self.imp_output_dir))
                os.system("rm -rf results_time")
                print("The results are stored in {}".format(os.path.join(self.imp_output_dir,text[-2],text[-1])))
            else:
                print("The results are stored in {}".format(self.user_repo_path))
        else:
            sys.exit("Need  at least one argument from the user cloning url or user repo path")

        flag = False
        packages = ["pip", "git"]
        if self.imp_url:
            flag = True
            if hasattr(sys, 'real_prefix'):
                git_status = self.check_git_status()
                if git_status:
                    print("Git is available proceeding further ")
                else:
                    print("Git is not installed on the system. "
                          "Please install git and restart this installation.")
                    sys.exit("Git is madatory Please install it")
                dep_install_status = self.install_depen("GitPython", "git")
                if dep_install_status:
                    print("Successfully installed package {}".format("GitPython"))
                else:
                    print("Not able to install the package {}".format("GitPython"))
                import git
                path = self.imp_url.split("/")[-1].split(".")[0]
                user_dir_path_flag = False
                if self.imp_output_dir:
                    self.user_repo_path = self.imp_output_dir
                    if os.path.exists(self.user_repo_path):
                        os.chdir(self.user_repo_path)
                    else:
                        print("the provided path {} is not found ".format(self.user_repo_path))
                        sys.exit()
                elif os.path.exists(os.path.join(current_working_directory, path)):
                    user_dir_path_flag = True
                    import time
                    timestamp = time.time()
                    new_directory_name = "{}_{}".format(path,int(timestamp))
                    self.user_repo_path = os.path.join(current_working_directory,new_directory_name)
                    os.mkdir(self.user_repo_path)
                    os.chdir(self.user_repo_path)
                else:
                    self.user_repo_path = os.path.join(current_working_directory, path)
                print("cloning the user provided url")
                git.Git(os.getcwd()).clone(self.imp_url)
                if not self.user_repo_path.endswith(path):
                    self.user_repo_path = os.path.join(self.user_repo_path, path)

                verify = Verify_Import_Statements(self.user_repo_path)
                verify.verify_import_statements()
                if user_dir_path_flag:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))
                elif self.imp_output_dir:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))
                else:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))
            else:
                bool_found = self.check_packages("pip")
                if not bool_found :
                    print("pip is not installed ")
                else:
                    print("pip is installed proceeding further !!!")
                git_status = self.check_git_status()
                if git_status:
                    print("Git is available proceeding further ")
                else:
                    print("Git is not installed on the system. "
                          "Please install git and restart this installation.")
                self.install_depen("virtualenv", "virtualenv")
                virt_act_status = self.activate_virtualenv()
                if virt_act_status:
                    print("successfully activated virtualenv")
                else:
                    print("Not able to activate the virtual env")
                dep_install_status = self.install_depen("GitPython", "git")
                if dep_install_status:
                    print("Successfully installed package {}".format("GitPython"))
                else:
                    print("Not able to install the package {}".format("GitPython"))
                import git
                path = self.imp_url.split("/")[-1].split(".")[0]
                user_dir_path_flag = False

                if self.imp_output_dir:
                    self.user_repo_path = self.imp_output_dir
                    if os.path.exists(self.user_repo_path):
                        os.chdir(self.user_repo_path)
                    else:
                        print("the provided path {} is not found ".format(self.user_repo_path))
                        sys.exit()
                elif os.path.exists(os.path.join(current_working_directory, path)):
                    user_dir_path_flag = True
                    import time
                    timestamp = time.time()
                    new_directory_name = "{}_{}".format(path, int(timestamp))
                    self.user_repo_path = os.path.join(current_working_directory, new_directory_name)
                    os.mkdir(self.user_repo_path)
                    os.chdir(self.user_repo_path)
                    print("Found the same name {} directory in current working directory , hence creating new directory {}".format(path, new_directory_name))
                else:
                    self.user_repo_path = os.path.join(current_working_directory, path)
                print("cloning the user provided url")
                git.Git(os.getcwd()).clone(self.imp_url)
                verify = Verify_Import_Statements(self.user_repo_path)
                verify.verify_import_statements()
                if user_dir_path_flag:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))
                elif self.imp_output_dir:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))
                else:
                    print("The changes will be available in this {} folder".format(self.user_repo_path))


if (imp_url and imp_output_dir) or (user_repo_path and imp_output_dir) or (imp_url) or (user_repo_path):
    print("Performing operation on Verify Import Statements")

    start_here = Pre_requirements(warrior_repo, Keyword_repos, add_repo_output, imp_url,\
        user_repo_path, imp_output_dir, add_repo_war_repos_path, add_repo_kw_repos_path)

    start_here.verify_import_statements_starts()

elif (warrior_repo and Keyword_repos and add_repo_output) or (warrior_repo and Keyword_repos):
    print("Performing operation on Add Repo in StepSection")

    start_here = Pre_requirements(str(args.add_repo_warrior_url), str(args.add_repo_keyword_url), add_repo_output, imp_url,\
        user_repo_path, imp_output_dir, add_repo_war_repos_path, add_repo_kw_repos_path)
    start_here.add_repo_in_step_starts()

elif (add_repo_war_repos_path and add_repo_kw_repos_path and add_repo_output) or (add_repo_war_repos_path and add_repo_kw_repos_path):

    start_here = Pre_requirements(warrior_repo, Keyword_repos, add_repo_output, imp_url,\
        user_repo_path, imp_output_dir, str(args.add_repo_war_repos_path), str(args.add_repo_kw_repos_path))
    start_here.add_repo_in_step_repos()
else:
    print("Please enter the requried Arguments. To know the argument to be passed to script entert 'python migration_tools.py --help'")
    sys.exit()


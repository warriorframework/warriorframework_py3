import argparse
import os
# Argparser to add command line argumets
from xml.etree import ElementTree as et

parser = argparse.ArgumentParser()
parser.add_argument('--type', help="type of test case cli or netconf", required=True)
parser.add_argument('--tc_name', help="type of test case cli or netconf", required=True)
parser.add_argument('--ip', help="type of test case cli or netconf", required=True)
parser.add_argument('--username', help="type of test case cli or netconf", required=True)
parser.add_argument('--password', help="type of test case cli or netconf", required=True)
parser.add_argument('--with_repo_structure', action='store_true',
                    help="to store the generated output files in warriorspace format")
args = parser.parse_args()
print("Arguments provided by user is {}".format(args))

class Warrior_execution_setup_files:

    def __init__(self):
        self.tc_name = args.tc_name.split(".")[0]
        self.current_working_directory = os.getcwd()
        print("current working directory is {}".format(self.current_working_directory))
        self.template_path = os.path.join(self.current_working_directory, "templates")
        self.input_data_file = "{}_{}".format(self.tc_name, "id_file.xml")
        self.tc_file = "{}_{}".format(self.tc_name, "tc_file.xml")
        self.td_file = "{}_{}".format(self.tc_name, "td_file.xml")

    def setup_warrior_structure(self):
        self.ws_directory = "Warriorspace"
        self.testcases_dir = "Warriorspace/Testcases"
        self.data_files_dir = "Warriorspace/Datafiles"
        self.config_files_dir = "Warriorspace/Configfiles"

        os.chdir(self.current_working_directory)
        if not os.path.exists(self.ws_directory):
            os.mkdir(self.ws_directory)
        if not os.path.exists(self.testcases_dir):
            os.mkdir(self.testcases_dir)
        if not os.path.exists(self.data_files_dir):
            os.mkdir(self.data_files_dir)
        if not os.path.exists(self.config_files_dir):
            os.mkdir(self.config_files_dir)

    def replace_values_in_input_data_xml_tags(self):
        tree = et.parse(self.input_data_file_path)
        tree.find('.//username').text = args.username
        tree.find('.//password').text = args.password
        tree.find('.//ip').text = args.ip
        if args.with_repo_structure:
            self.td_file = os.path.join(self.current_working_directory, self.config_files_dir, self.td_file)
        tree.find('.//testdata').text = self.td_file
        tree.write(self.input_data_file_path)

    def replace_values_in_test_case_xml_tags(self):
        tree = et.parse(self.test_case_file_path)
        if args.with_repo_structure:
            self.input_data_file = os.path.join(self.current_working_directory, self.data_files_dir, self.input_data_file)
        tree.find('.//InputDataFile').text = self.input_data_file
        tree.write(self.test_case_file_path)

    def generate_cli_files(self, with_repo_structure=False):

        if args.type == "cli":

            if with_repo_structure:
                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_data_file_template.xml"),
                                            os.path.join(self.current_working_directory, self.data_files_dir,
                                                         self.input_data_file)))
                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_test_data_template.xml"),
                                            os.path.join(self.current_working_directory, self.config_files_dir,
                                                         self.td_file)))
                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_test_case_template.xml"),
                                            os.path.join(self.current_working_directory, self.testcases_dir,
                                                         self.tc_file)))

                self.input_data_file_path = os.path.join(self.current_working_directory, self.data_files_dir,
                                                         self.input_data_file)
                print("*******")
                print("Location of input data file : {}".format(self.input_data_file_path))
                print("*******")
                self.test_case_file_path = os.path.join(self.current_working_directory, self.testcases_dir,
                                                        self.tc_file)
                print("*******")
                print("Location of test case file : {}".format(self.test_case_file_path))
                print("*******")
                self.test_data_file_path = os.path.join(self.current_working_directory, self.config_files_dir,
                                                        self.td_file)
                print("*******")
                print("Location of test data file : {}".format(self.test_data_file_path))
                print("*******")
                self.replace_values_in_input_data_xml_tags()
                self.replace_values_in_test_case_xml_tags()
                print("Run line  command is : Warrior {}".format(self.test_case_file_path))
            else:
                # generating the required files i.e test case , data file and testdata file

                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_data_file_template.xml"),
                                            os.path.join(self.current_working_directory, self.input_data_file)))
                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_test_data_template.xml"),
                                            os.path.join(self.current_working_directory, self.td_file)))
                os.system("cp {} {}".format(os.path.join(self.template_path, "cli_test_case_template.xml"),
                                            os.path.join(self.current_working_directory, self.tc_file)))

                self.input_data_file_path = os.path.join(self.current_working_directory, self.input_data_file)
                self.test_case_file_path = os.path.join(self.current_working_directory, self.tc_file)
                self.test_data_file_path = os.path.join(self.current_working_directory, self.td_file)
                print("*******")
                print("Location of testcase file::{}".format(self.test_case_file_path))
                print("*******")
                print("Location of inputdata file::{}".format(self.input_data_file_path))
                print("*******")
                print("Location of testdata file::{}".format(self.test_data_file_path))
                print("*******")
                self.replace_values_in_input_data_xml_tags()
                self.replace_values_in_test_case_xml_tags()
                print("Run line  command is : Warrior {}".format(self.test_case_file_path))

obj = Warrior_execution_setup_files()
if args.with_repo_structure:
    obj.setup_warrior_structure()
    obj.generate_cli_files(with_repo_structure=True)
else:
    obj.generate_cli_files()

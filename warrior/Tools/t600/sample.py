import sys
import json
import os
import site
import glob
import subprocess
import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et


class Sample():
    def __init__(self):
        if len(sys.argv[1:]) != 2:
            print("json file path and operation are mandatory !!!")
            sys.exit()
        self.json_file_path = sys.argv[1]
        self.operation = sys.argv[2]

        self.current_working_directory = os.getcwd()
        site_home_path = os.path.split(site.__file__)[0]
        site_packages_path = "site-packages/warrior/Tools/templates"
        self.template_path = os.path.join(site_home_path, site_packages_path)
        self.testcase_file = "sample.xml"
        self.input_data_file = "sample_id.xml"
        self.testdata_file = "sample_td.xml"

    def load_json_file(self):
        # import pdb
        # pdb.set_trace()
        if os.path.exists(self.json_file_path):
            fd = open(self.json_file_path)
            data = json.loads(fd.read())
            return data
        else:
            print("file not found {}".format(self.json_file_path))

    def generate_input_data_file(self):
        json_data = self.load_json_file()
        root = ET.Element('credentials')
        for key in json_data["devices"].keys():
            system = json_data["devices"][key]
            items = ET.SubElement(root, 'system')
            items.set("name", key)
            ip = ET.SubElement(items, 'ip')
            conn_type = ET.SubElement(items, 'conn_type')
            cli_port = ET.SubElement(items, 'ssh_port')
            username = ET.SubElement(items, 'username')
            password = ET.SubElement(items, 'password')
            prompt = ET.SubElement(items, 'prompt')
            testdata = ET.SubElement(items, 'testdata')
            #dip_port = ET.SubElement(items, 'dip_port')

            # ip address
            if system["ip"] is None:
                ip.text = "localhost"
            else:
                ip.text = system["ip"]

            # conn port
            if system.get("protocol"):
                conn_type.text = system["protocol"]
            if system.get("port"):
                cli_port.text = system["port"]

            # username
            if system["username"] is None:
                username.text = 'fujitsu'
            else:
                username.text = system["username"]

            # password
            if system["password"] is None:
                password.text = '1finity'
            else:
                password.text = system["password"]

            # prompt
            if not system.get("prompt"):
                prompt.text = "\$"
            else:
                prompt.text = system["prompt"]

            # # testdata
            # if system.get("testdata"):
            testdata.text = self.testdata_file
            # # dip_port
            # if system["dip_port"]:
            #     testdata.text = system["dip_port"]

            # create a new XML file with the results
            mydata = ET.tostring(root)
            dom = xml.dom.minidom.parseString(mydata)
            final_data = dom.toprettyxml()

            input_data_file = open(self.input_data_file, "w")
            input_data_file.write(final_data)

    def generate_test_case_file(self):
        json_data = self.load_json_file()

        self.testcase = ET.Element('Testcase')
        details = ET.SubElement(self.testcase, 'Details')
        name = ET.SubElement(details, 'Name')
        title = ET.SubElement(details, 'Title')
        input_data_file = ET.SubElement(details, 'InputDataFile')
        engineer = ET.SubElement(details, 'Engineer')

        name.text = "Sample"
        title.text = "Sample"
        input_data_file.text = self.input_data_file
        engineer.text = "Warrior User"

        self.steps = ET.SubElement(self.testcase, 'Steps')

        count = 1
        for key in json_data["devices"].keys():
            step = ET.SubElement(self.steps, 'step')
            step.set("Driver", "cli_driver")
            step.set("Keyword", "connect")
            step.set("TS", str(count))
            args = ET.SubElement(step, 'Arguments')
            arg = ET.SubElement(args, 'argument')
            arg.set("name", "system_name")
            arg.set("value", key) # this value should be repalced from json
            count = int(count) + 1

        # for send_commands by title
        self.d = {}
        for key in json_data["devices"].keys():
            step = ET.SubElement(self.steps, 'step')
            step.set("Driver", "cli_driver")
            step.set("Keyword", "send_commands_by_testdata_title")
            step.set("TS", str(count))
            args = ET.SubElement(step, 'Arguments')

            arg = ET.SubElement(args, 'argument')
            arg.set("name", "system_name")
            arg.set("value", key)  # this value should be repalced from json

            arg = ET.SubElement(args, 'argument')
            arg.set("name", "title")
            value = key + str(count)
            print(value)
            arg.set("value", value)  # this value should be repalced from json
            self.d.update({key: value})
            count = int(count) + 1


        # disconnect
        for key in json_data["devices"].keys():
            step = ET.SubElement(self.steps, 'step')
            step.set("Driver", "cli_driver")
            step.set("Keyword", "disconnect")
            step.set("TS", str(count))
            args = ET.SubElement(step, 'Arguments')
            arg = ET.SubElement(args, 'argument')
            arg.set("name", "system_name")
            arg.set("value", key)  # this value should be repalced from json
            count = int(count) + 1

        # step = ET.SubElement(self.steps, 'step')
        # step.set("Driver", "cli_driver")
        # step.set("Keyword", "disconnect")
        # args = ET.SubElement(step, 'Arguments')
        # arg = ET.SubElement(args, 'argument')
        # arg.set("name", "system_name")
        # arg.set("value", "system1")  # this value should be repalced from json

        mydata = ET.tostring(self.testcase)
        dom = xml.dom.minidom.parseString(mydata)
        final_data = dom.toprettyxml()
        input_data_file = open(self.testcase_file, "w")
        input_data_file.write(final_data)

    def generate_test_data_file(self):
        json_data = self.load_json_file()
        self.testdata = ET.Element('data')
        for key in json_data["devices"].keys():
            if self.operation == "set":
                testdata = ET.SubElement(self.testdata, 'testdata')
                testdata.set("title", self.d[key])
                testdata.set("execute", "yes")
                for k in json_data[self.operation][key].keys():
                    command = ET.SubElement(testdata, 'command')
                    command.set("send", str(json_data[self.operation][key][k]))
                    command.set("end", "\$")

        mydata = ET.tostring(self.testdata)
        dom = xml.dom.minidom.parseString(mydata)
        final_data = dom.toprettyxml()
        input_data_file = open(self.testdata_file, "w")
        input_data_file.write(final_data)

    def ran_generated_testcase(self):
        os.system("Warrior {}".format(self.testcase_file))
        pass

    def process_logs(self):

        if os.environ.get("HOME"):
            home_path = os.environ["HOME"]
            exe_dir = "Warriorspace/Execution"

            logs_dir = os.path.join(home_path, exe_dir)
            act_path = os.path.join(logs_dir, "*")
            list_of_files = glob.glob(act_path)
            logs_dir_full = max(list_of_files, key=os.path.getctime)
            log_file_name = os.path.split(logs_dir_full)[-1]
            final_path = os.path.join(logs_dir_full, "Logs")

            os.chdir(final_path)
            print(final_path, log_file_name)
            import pdb
            #pdb.set_trace()
            tc_name = self.testcase_file.split(".")[0]
            file_desc = (open("{}_consoleLogs.log".format(tc_name)))
            file_content = file_desc.read()

            import re
            match = re.search("TESTCASE\:sample\s*STATUS\:(PASS|FAIL)", file_content)
            #print(match)
            result = {}
            result.update({"script_status" : match.group(1)})
            print(result)
            with open('data.txt', 'w') as outfile:
                json.dump(result, outfile)
            print("The location of result file {}".format(os.path.join(os.getcwd(), "data.txt")))


            #print(json.dump(result))





            # import pdb
            # pdb.set_trace()
            # os.system("ls -lrt | tail -n 2 | rev | cut -d' ' -f1 | rev >>hello.txt")
            # fd = open("hello.txt", "r")
            # lines = fd.readlines()
            # tc_name = self.testcase_file.split(".")[1]
            # for line in lines:
            #     if line.startswith(tc_name):
            #         dir_name = line
            #         print(dir_name)
            #
            # print(subprocess.check_output(r"ls -lrt | tail -n 2 | rev | cut -d' ' -f1 | rev"))

    def generate_cli_files(self):
        os.system("cp {} {}".format(os.path.join(self.template_path, "cli_test_case_template.xml"),
                                    os.path.join(self.current_working_directory, self.tc_file)))
        self.test_case_file_path = os.path.join(self.current_working_directory, self.tc_file)

    def replace_values_in_test_case_xml_tags(self):
        tree = et.parse(self.test_case_file_path)
        tree.find('.//InputDataFile').text = self.input_data_file
        tree.write(self.test_case_file_path)
        tree.findall("")

s = Sample()
s.generate_input_data_file()
s.generate_test_case_file()
s.generate_test_data_file()
s.ran_generated_testcase()
s.process_logs()
#s.replace_values_in_test_case_xml_tags()
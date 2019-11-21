from collections import OrderedDict
from datetime import datetime
from katana.utils.json_utils import read_xml_get_json
from katana.utils.navigator_util import Navigator


class VerifyProjectFile:

    def __init__(self, template, file_path):
        self.navigator = Navigator()
        self.template = template
        self.file_path = file_path
        self.template_data = read_xml_get_json(template, ordered_dict=True)
        self.data = read_xml_get_json(file_path, ordered_dict=True)
        self.output = {"status": True, "message": ""}
        self.root = "Project"

    def verify_file(self):
        """ This function verifies the suite file """
        self.__verify_root()
        if self.output["status"]:
            self.__verify_details()
            self.__verify_requirements()
            self.__verify_cases()
        return self.output, self.data

    def __verify_root(self):
        """ Verifies the root of the suite file """
        for key in self.data:
            if key != self.root:
                self.output["status"] = False
                self.output["message"] = "{0} is not is the correct format."
                print("-- An Error Occurred -- {0}".format(self.output["message"]))
            break

    def __verify_details(self):
        """ Verifies details section of the suite """
        top_key = "Details"
        if top_key not in self.data[self.root] or self.data[self.root][top_key] is None:
            self.data[self.root][top_key] = {}
        for key, value in self.template_data[self.root][top_key].items():
            key, value = self.__verified_details_key_value(key, value)
            self.data[self.root][top_key][key] = self.__verify_values(key, value, self.data[self.root][top_key])

    def __verify_requirements(self):
        """ Verifies the requirements section of the suite file """
        top_key = "Requirements"
        if top_key not in self.data[self.root] or self.data[self.root][top_key] is None:
            self.data[self.root][top_key] = {"Requirement": []}
        elif "Requirement" not in self.data[self.root][top_key] or self.data[self.root][top_key]["Requirement"] is None:
            self.data[self.root][top_key]["Requirement"] = []
        elif not isinstance(self.data[self.root][top_key]["Requirement"], list):
            self.data[self.root][top_key]["Requirement"] = [self.data[self.root][top_key]["Requirement"]]

    def __verify_cases(self):
        """ Verifies the cases section of the suite file """
        top_key = "Testsuites"
        if top_key not in self.data[self.root] or self.data[self.root][top_key] is None:
            self.data[self.root][top_key] = {"Testsuite": []}
        elif "Testsuite" not in self.data[self.root][top_key] or self.data[self.root][top_key]["Testsuite"] is None:
            self.data[self.root][top_key]["Testsuite"] = []
        elif not isinstance(self.data[self.root][top_key]["Testsuite"], list):
            self.data[self.root][top_key]["Testsuite"] = [self.data[self.root][top_key]["Testsuite"]]


    @staticmethod
    def __verified_steps_key_value(key, value, verify_data):
        """ Verifies specific keys in each step """
        if value is None:
            value = ""

        if key == "Execute":
            if key not in verify_data or verify_data[key] is None:
                verify_data[key] = {}
            if "Rule" not in verify_data[key] or verify_data[key]["Rule"] is None:
                verify_data[key]["Rule"] = [{}]
            elif not isinstance(verify_data[key]["Rule"], list):
                verify_data[key]["Rule"] = [verify_data[key]["Rule"]]

        return key, value, verify_data

    def __verified_details_key_value(self, key, value):
        """ Verifies specific keys in details """
        if value is None:
            value = ""
        if value == "":
            if key == "Engineer":
                value = self.navigator.get_engineer_name()
            if key == "Date":
                now = datetime.now()
                value = "{0}-{1}-{2}".format(now.year, now.month, now.day)
            if key == "Time":
                now = datetime.now()
                value = "{0}:{1}".format(now.hour, now.minute)
        return key, value

    def __verify_values(self, tmpl_key, tmpl_value, parent):
        """ Verifies key value in each step with the case template file """
        output = ""
        if tmpl_key not in parent:
            output = tmpl_value
        elif parent[tmpl_key] is None:
            output = tmpl_value
        else:
            if isinstance(parent[tmpl_key], list):
                for i in range(0, len(parent[tmpl_key])):
                    for k, v in tmpl_value.items():
                        parent[tmpl_key][i][k] = self.__verify_values(k, v, parent[tmpl_key][i])
                    output = parent[tmpl_key]
            elif isinstance(tmpl_value, OrderedDict):
                for k, v in list(tmpl_value.items()):
                    parent[tmpl_key][k] = self.__verify_values(k, v, parent[tmpl_key])
                output = parent[tmpl_key]
            else:
                output = parent[tmpl_key] if parent[tmpl_key].strip() != "" else tmpl_value
        return output


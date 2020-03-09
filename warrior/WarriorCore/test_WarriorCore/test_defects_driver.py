'''
UT for defects_driver
'''
import sys, os
from os.path import abspath, dirname
from argparse import Namespace

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
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest import mock
import pytest


import os
import json
import time
from warrior import Tools
from warrior.WarriorCore.Classes.jira_rest_class import Jira
from warrior.Framework.Utils.print_Utils import print_error, print_info, print_warning
from warrior.Framework.Utils import xml_Utils, file_Utils

class test_DefectsDriver(object):
    """ Defects Driver Class """

    def __init__(self, data_repository):
        """Constructor for Defects Driver"""
        self.xmlfile = data_repository['wt_resultfile']
        self.defectsdir = data_repository['wt_defectsdir']
        self.logsdir = data_repository['wt_logsdir']
        self.resultfile = data_repository['wt_resultfile']
        self.testcase_filepath = data_repository['wt_testcase_filepath']
        self.jiraproj = data_repository['jiraproj']
        self.w_jira_object = None


    def _get_text_forjson_test1(self):
        """Process the text and attributes of a node
        into a text, this text will be used in the defect json file"""
        text = ""        
        excl_list = ["Name", "Arguments"]

        if node.tag == "Keyword":
            text = node.find("Name").text
        elif node.tag == "argument":
            text = self._get_argument_text(node)
        elif node.tag in excl_list:
            text = ""
        else:
            text = node.text
        return text
        _get_text_forjson(self, node)
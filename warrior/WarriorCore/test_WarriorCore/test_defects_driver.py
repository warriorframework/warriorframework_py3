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

'''
UT for defects_driver
'''
import sys, os
from os.path import abspath, dirname
from argparse import Namespace

# import pdb
# pdb.set_trace()
try:
    from warrior.WarriorCore import defects_driver
#except ModuleNotFoundError as error:
except:
    WARRIORDIR = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(WARRIORDIR)
    try:
        from warrior.WarriorCore import defects_driver
    except:
        raise

from unittest.mock import patch
from unittest.mock import MagicMock
from unittest import mock, TestCase
import pytest


import os
import json
import time
from warrior import Tools
from warrior.WarriorCore.Classes.jira_rest_class import Jira
from warrior.Framework.Utils.print_Utils import print_error, print_info, print_warning
from warrior.Framework.Utils import xml_Utils, file_Utils

from warrior.WarriorCore.defects_driver import DefectsDriver

class Test_DefectsDriver(TestCase):
    """ Defects Driver Class """


    def test_get_defect_json_list1(self):

        data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
        'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

        cls_obj = DefectsDriver(data_repository)
        os.listdir = MagicMock(return_value=['hello.py', 'exmp.json'])

        cls_obj.xmlfile = data_repository['wt_resultfile']
        cls_obj.defectsdir = data_repository['wt_defectsdir']
        cls_obj.logsdir = data_repository['wt_logsdir']
        cls_obj.resultfile = data_repository['wt_resultfile']
        cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
        cls_obj.jiraproj = data_repository['jiraproj']
        cls_obj.w_jira_object = None

        cls_obj.get_defect_json_list()

    def test_get_defect_json_list2(self):

        data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
        'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

        cls_obj = DefectsDriver(data_repository)
        os.listdir = MagicMock(return_value=['hello.py', 'exmp.json'])

        cls_obj.xmlfile = data_repository['wt_resultfile']
        cls_obj.defectsdir = data_repository['wt_defectsdir']
        cls_obj.logsdir = data_repository['wt_logsdir']
        cls_obj.resultfile = data_repository['wt_resultfile']
        cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
        cls_obj.jiraproj = data_repository['jiraproj']
        cls_obj.w_jira_object = None

        cls_obj.get_defect_json_list()


    def test_connect_warrior_jira(self):
        """Creates a Warrior Jira object """

        data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
        'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

        Jira = MagicMock(return_value='object')

        cls_obj = DefectsDriver(data_repository)
        cls_obj.connect_warrior_jira()

    def test_attach_logs_to_jira_issues(self):
        """Attach logs to jira issues """

        data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
        'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

        cls_obj = DefectsDriver(data_repository)

        cls_obj.xmlfile = data_repository['wt_resultfile']
        cls_obj.defectsdir = data_repository['wt_defectsdir']
        cls_obj.logsdir = data_repository['wt_logsdir']
        cls_obj.resultfile = data_repository['wt_resultfile']
        cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
        cls_obj.jiraproj = data_repository['jiraproj']

        def test_fn():
            return True
        create_issues_from_jsonlist = MagicMock(return_value='test_fn')
        cls_obj.w_jira_object = create_issues_from_jsonlist

        file_Utils.create_zipdir = MagicMock(return_value=None)
        cls_obj.w_jira_object.upload_logfile_to_jira_issue = MagicMock(return_value=None)
        issue = "bug"

        cls_obj.attach_logs_to_jira_issues(issue)

    def test_create_jira_issues1(self):
        """Creates issues in jira """
        # issue_list = []

        data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
        'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

        cls_obj = DefectsDriver(data_repository)

        defects_json_list = ['abc1.json', 'abc2.json']

        cls_obj.xmlfile = data_repository['wt_resultfile']
        cls_obj.defectsdir = data_repository['wt_defectsdir']
        cls_obj.logsdir = data_repository['wt_logsdir']
        cls_obj.resultfile = data_repository['wt_resultfile']
        cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
        cls_obj.jiraproj = data_repository['jiraproj']

        def test_fn():
            return True
        create_issues_from_jsonlist = MagicMock(return_value='test_fn')
        cls_obj.w_jira_object = create_issues_from_jsonlist
        # cls_obj.w_jira_object.status = MagicMock(return_value=True)


        cls_obj.w_jira_object.create_issues_from_jsonlist = MagicMock(return_value=['issue1', 'issue2'])
        cls_obj.attach_logs_to_jira_issues = MagicMock(return_value=None)

        cls_obj.create_jira_issues(defects_json_list)
        del cls_obj.attach_logs_to_jira_issues

    # def test_create_failing_kw_json1(self):
    #     """Create a json file each failing keyword """

    #     data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
    #     'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

    #     cls_obj = DefectsDriver(data_repository)

    #     defects_json_list = ['abc1.json', 'abc2.json']

    #     cls_obj.xmlfile = data_repository['wt_resultfile']
    #     cls_obj.defectsdir = data_repository['wt_defectsdir']
    #     cls_obj.logsdir = data_repository['wt_logsdir']
    #     cls_obj.resultfile = data_repository['wt_resultfile']
    #     cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
    #     cls_obj.jiraproj = data_repository['jiraproj']


    #     file_Utils.getNameOnly = MagicMock(return_value='testcasename_results')
    #     xml_Utils.getRoot = MagicMock(return_value='xmltag')
    #     tree = xml_Utils.getRoot
    #     find = MagicMock(return_value='/abc/file.xml')
    #     tree.findall = MagicMock(return_value=['connect', 'disconnect', 'log_message'])


    #     cls_obj.create_failing_kw_json()

    # def test_create_failing_kw_json2(self):
    #     """Create a json file each failing keyword """

    #     data_repository = {'wt_resultfile':'abc.xml', 'wt_defectsdir':'/home', \
    #     'wt_logsdir':'/home', 'wt_testcase_filepath':'/home/abc/Desktop', 'jiraproj':'True'}

    #     cls_obj = DefectsDriver(data_repository)

    #     defects_json_list = ['abc1.json', 'abc2.json']

    #     cls_obj.xmlfile = data_repository['wt_resultfile']
    #     cls_obj.defectsdir = data_repository['wt_defectsdir']
    #     cls_obj.logsdir = data_repository['wt_logsdir']
    #     cls_obj.resultfile = data_repository['wt_resultfile']
    #     cls_obj.testcase_filepath = data_repository['wt_testcase_filepath']
    #     cls_obj.jiraproj = data_repository['jiraproj']


    #     file_Utils.getNameOnly = MagicMock(return_value='testcasename_results')
    #     xml_Utils.getRoot = MagicMock(return_value='xmltag')
    #     tree = xml_Utils.getRoot
    #     find = MagicMock(return_value='<datafile>/abc/file.xml</datafile>')
    #     findall = MagicMock(return_value=[])

    #     cls_obj.create_failing_kw_json()
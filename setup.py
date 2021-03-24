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
from setuptools import setup, find_packages

PACKAGE_NAME = "warriorframework"
PACKAGE_VERSION = "4.6.0"

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="warriorteam",
    author_email='frameworkwarrior@gmail.com',
    scripts=['warrior/Warrior',
             'warrior/Warriormigrate',
             'warrior/WarriorTools/warrior_py3_migration_tools/warrior_py3_migration_tool',
             'warrior/WarriorTools/tc_generator/tc_generator',
             'warrior/warrior_upgrade'],
    packages=find_packages(exclude=['warrior/test_WarriorCore']),
    package_data={'':['**/*', '*']},
    include_package_data=True,
    data_files=[('warrior_settings/Tools', ['warrior/Tools/w_settings.xml']),
                ('warrior_settings/Tools/admin', ['warrior/Tools/admin/secret.key']),
                ('warrior_settings/Tools/jira', ['warrior/Tools/jira/jira_config.xml']),
                ('warrior_settings/Tools/database', ['warrior/Tools/database/database_config.xml']),
                ('warrior_settings/Tools/connection', \
                                  ['warrior/Tools/connection/configs/1finity_command_data.xml', \
                                   'warrior/Tools/connection/configs/ubuntu_command_data.xml', \
                                   'warrior/Tools/connection/connect_settings.xml']),
                ('warrior_settings/Tools/xsd', ['warrior/Tools/xsd/warrior_testcase.xsd',\
                                                'warrior/Tools/xsd/warrior_project.xsd',\
                                                'warrior/Tools/xsd/warrior_suite.xsd']),
                ('warrior_settings/Tools/reporting',\
                                  ['warrior/Tools/reporting/wjunit_to_xunit.xsl',\
                                   'warrior/Tools/reporting/html_results_template.html'])],
    long_description=open('module.txt').read(),
    description="Warrior Framework is an open source Automation Framework",
    url="https://github.com/warriorframework/warriorframework_py3",
    project_urls={
        "Documentation": "http://warriorframework.org/",
        "Source Code": "https://github.com/warriorframework/warriorframework_py3",
    },
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 3.6',],
    install_requires=["kafka-python==1.4.6", "configobj==5.0.6", "requests==2.21.0"]

)

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
PACKAGE_VERSION = "4.1.0"

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="warriorteam",
    author_email='frameworkwarrior@gmail.com',
    scripts=['warrior/Warrior',
             'katana/manage.py',
             'warrior/Tools/warrior_py3_migration_tools/warrior_py3_migration_tool',
             'warrior/Tools/tc_generator/tc_generator',],
    packages=find_packages(),
    package_data={'':['**/*', '*']},
    include_package_data=True,
    long_description=open('module.txt').read(),
    description="Warrior Framework is an open source Automation Framework",
    url="https://github.com/warriorframework/warriorframework_py3",
    project_urls={
        "Documentation": "http://warriorframework.org/",
        "Source Code": "https://github.com/warriorframework/warriorframework_py3",
    },
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 3.6',
                 ],
    install_requires=["pexpect==4.2", "requests==2.21.0", "selenium==3.8.0",
                      "lxml==4.4.1", "paramiko==2.4.2", "pysnmp==4.4.9",
                      "pyvirtualdisplay==0.2.1", "kafka-python==1.4.6",
                      "cloudshell-automation-api==9.3.0.175525",
                      "pycryptodome==3.6.1", "Django==2.1.2", "xmltodict==0.12.0",
                      "python-ldap", "django_auth_ldap",
                      "djangorestframework==3.10.3",]

)

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
import os
import site

PACKAGE_NAME = "warriorcli"
PACKAGE_VERSION = "1.0.0"

try:
    import warrior
except:
    print('\033[91m' +
          f"Can't install {PACKAGE_NAME}, first you need to install warriorframework package" + '\033[0m')

else:
    if os.getenv('VIRTUAL_ENV'):
        warrior_path = "/".join(os.path.abspath(warrior.__file__).split(os.getenv('VIRTUAL_ENV'))[1].split("/")[1:-1])
    else:
        warrior_path = "/".join(os.path.abspath(warrior.__file__).split(site.getuserbase())[1].split("/")[1:-1])
        print(f"Found warriorframework package at:'{warrior_path}'")
    setup(
        name=PACKAGE_NAME,
        version=PACKAGE_VERSION,
        author="warriorteam",
        author_email='frameworkwarrior@gmail.com',
        scripts=[],
        packages=find_packages(),
        include_package_data=True,
        package_data={'':['**/*', '*']},
        data_files=[(warrior_path+"/Actions/CliActions", [os.path.join("warriorcli", "Actions", "CliActions", "__init__.py")]),
                    (warrior_path+"/Actions/CliActions", [os.path.join("warriorcli", "Actions", "CliActions", "cli_actions.py")]),
                    (warrior_path+"/ProductDrivers", [os.path.join("warriorcli", "ProductDrivers", "cli_driver.py")]),
                    (warrior_path+"/ProductDrivers", [os.path.join("warriorcli", "ProductDrivers", "cli_driver.py")]),
                    (warrior_path+"/Framework/Utils", [os.path.join("warriorcli", "Utils", "cli_Utils.py")]),
                    (warrior_path+"/Framework/Utils", [os.path.join("warriorcli", "Utils", "list_Utils.py")]),
                    (warrior_path+"/Framework/ClassUtils", [os.path.join("warriorcli", "ClassUtils", "ssh_utils_class.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "base_class.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "connection.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "diagnostics.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "file_ops.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "loging.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "__init__.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "network_class.py")]),
                    (warrior_path+"/Framework/ClassUtils/WNetwork", [os.path.join("warriorcli", "ClassUtils", "WNetwork", "warrior_cli_class.py")]),

                    ],
        long_description="cli_driver package for warrior framework",
        description="Warrior Framework is an open source Automation Framework",
        url="https://github.com/warriorframework/warriorframework_py3",
        project_urls={
            "Documentation": "http://warriorframework.org/",
            "Source Code": "https://github.com/warriorframework/warriorframework_py3",
        },
        classifiers=['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: Apache Software License',
                     'Programming Language :: Python :: 3.6', ],
        install_requires=["pexpect==4.8.0", "pycryptodome==3.6.1"]

    )

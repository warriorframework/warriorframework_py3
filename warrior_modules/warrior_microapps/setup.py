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

PACKAGE_NAME = "warriormicroapps"
PACKAGE_VERSION = "1.0.0"

try:
    import warrior
except:
    print('\033[91m' +
          f"Couldn't install {PACKAGE_NAME}, first you need to install warriorframework package" + '\033[0m')

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
        package_data={'':['**/*', '*']},
        data_files=[(warrior_path+"/Actions/MicroappsActions", [os.path.join("warriormicroapps", "Actions", "MicroappsActions", "__init__.py")]),
                    (warrior_path+"/Actions/MicroappsActions", [os.path.join("warriormicroapps", "Actions", "MicroappsActions", "microapps_actions.py")]),
                    (warrior_path+"/ProductDrivers", [os.path.join("warriormicroapps", "ProductDrivers", "microapps_driver.py")]),
                    ],
        include_package_data=True,
        long_description= "microapps_driver package for warrior framework",
        description="Warrior Framework is an open source Automation Framework",
        url="https://github.com/warriorframework/warriorframework_py3",
        project_urls={
            "Documentation": "http://warriorframework.org/",
            "Source Code": "https://github.com/warriorframework/warriorframework_py3",
        },
        classifiers=['Development Status :: 5 - Production/Stable',
                    'License :: OSI Approved :: Apache Software License',
                    'Programming Language :: Python :: 3.6',],
        install_requires=[]

    )

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

"""Warrior Network connectivity module """

from warrior.Framework.ClassUtils.WNetwork.base_class import Base

class Connection(Base):
    """Warrior connectivity class """
    
    def __init__(self, *args, **kwargs):
        """ Constructor """
        super(Connection, self).__init__(*args, **kwargs)

    def connect(self):
        """ """

    def connect_ssh(self):
        """ """
        print("ssh connection")

    def connect_telnet(self):
        """ """
        
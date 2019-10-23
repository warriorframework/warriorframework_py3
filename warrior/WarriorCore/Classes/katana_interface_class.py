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

"""
This class is deprecated as a new communication method has been created in WAR-1440
"""

from xml.dom import minidom
import os
import json
try:
    import requests
    has_requests = True
except ImportError:
    has_requests = False
    print("warrior can not communicate with katana please install requests and try again")



class KatanaInterface:
    katanaLocation = ''

    def __init__(self):
        if has_requests:
            self.get_location()

    def get_location(self):
        l_dir = os.path.dirname(__file__)
        filename = os.path.join(l_dir, '../../Tools/w_settings.xml')
        settings_xml = minidom.parse(filename)
        setting_elems = settings_xml.getElementsByTagName('Setting')
        for i in setting_elems:
            if i.attributes['name'].value == 'katana':
                self.katanaLocation = i.attributes['location'].value

    def send_file(self, fileLocation, to_call=None):
        if self.katanaLocation != '':
            jsonObj = {'file_path': fileLocation, 'to_call': to_call}
            client = requests.session()
            url = self.katanaLocation + to_call if to_call else self.katanaLocation
            resp = requests.post(url, data=jsonObj)
            #print 'resp: ', resp.status_code, resp.text

    def end_comunication(self):
        if self.katanaLocation != '':
            jsonObj = {}
            jsonObj['toCall'] = 'setLocation'
            #requests.post(self.katanaLocation, json=jsonObj)

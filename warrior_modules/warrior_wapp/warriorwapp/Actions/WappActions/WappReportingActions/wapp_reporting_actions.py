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

import datetime
import multiprocessing
from warrior.Framework.Utils import config_Utils
from warrior.WarriorCore.Classes.warmock_class import mockready
from warrior.Framework.Utils.data_Utils import get_object_from_datarepository, get_credentials


class CWPluginActions(object):
    """ Class with kw providing utilities that connect Warrior to Wapps """

    def __init__(self):
        """
        constructor
        """
        self.resultfile = config_Utils.resultfile
        self.datafile = config_Utils.datafile
        self.logsdir = config_Utils.logsdir
        self.filename = config_Utils.filename
        self.logfile = config_Utils.logfile

    @mockready
    def report_ne_status_to_katana(self, system_name):
        """
            write the ne execution result to the live html obj
        """
        live_html_obj = get_object_from_datarepository("live_html_dict")
        cred = get_credentials(self.datafile, system_name)
        status = False
        if live_html_obj and isinstance(live_html_obj.get("livehtmllocn", None),
                                        multiprocessing.managers.DictProxy):
            result = True
            for key, val in config_Utils.data_repository.items():
                if key.startswith("step-") and key.endswith("_status"):
                    if isinstance(val, bool) and result != "ERROR":
                        result &= val
                    else:
                        result = "ERROR"
            # In order to share data between process, have to use the multiprocess
            # manager dict to store it
            # Cannot simply create a new dict and assign it to the live_html_obj
            tmp = live_html_obj["livehtmllocn"]["system_result"]
            tmp[cred["circuit_id"]] = tmp.get(cred["circuit_id"], {})
            tmp[cred["circuit_id"]][cred["id"]] = (
                result, datetime.datetime.now().replace(microsecond=0),
                str(self.logfile)[:-4] + "_consoleLogs.log")
            live_html_obj["livehtmllocn"]["system_result"] = tmp
            status = True
        return status

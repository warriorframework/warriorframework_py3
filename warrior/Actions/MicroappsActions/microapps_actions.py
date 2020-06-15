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


import os
from warrior.Framework import Utils
from warrior.Framework.Utils.testcase_Utils import pNote



class MicroappsActions(object):
    """class MicroappsActions having method that are for warrior_result product"""

    def get_warrior_result(self):
        """Returns warrior status and failed command details.
           :Returns:
                1. script_status(boolean) : True if all steps Passed else False
                2. step_status_message (str) : step status
                3. failure_reason (str) : failure reason
        """
        wdesc = "to get current status of warrior script and failure reason"
        Utils.testcase_Utils.pNote(wdesc)
        script_status = True
        step_status_message = None
        failure_reason = None
        data_repository = Utils.config_Utils.data_repository
        for session_td_key, session_td_value in data_repository.items():
            if session_td_key.startswith('step') and session_td_key.endswith('_result'):
                if session_td_value != "PASS" and session_td_value.lower() != "skipped":
                    step_impact = data_repository.get(session_td_key.replace('_result', '_impact'))
                    if (step_impact.upper() == "IMPACT"):
                        script_status = False
                        step_status_message = "{0} status {1}". \
                            format(session_td_key.replace('_result', ''), session_td_value)
                        break

        if not script_status:
            for session_td_key, session_td_value in data_repository.items():
                if '_td_response' in session_td_key:
                    for title_td_key, title_td_value in session_td_value.items():
                        for command_key, command_value in title_td_value.items():
                            if '_status' not in command_key and '_command' not in command_key:
                                command = title_td_value.get(command_key + "_command", None)
                                status = title_td_value.get(command_key + "_status", None)
                                response = title_td_value.get(command_key, None)
                                if status is not None and status != "PASS":
                                    script_status = False
                                    if command is not None:
                                        splitted_command = command.split(":")
                                        if splitted_command[0] == "3" or splitted_command[0] == \
                                                "wctrl:x" or splitted_command[0] == ";":
                                            failure_reason = "Communication Failure with device"
                                        else:
                                            if "Expected pattern not found" in response:
                                                failure_reason = "{} Failed : reason {}".format(splitted_command[0],
                                                                                                response)
                                            else:
                                                failure_reason = "{0} Failed".format(splitted_command[0])

        if failure_reason is None and script_status is False:
            failure_reason = "Script execution failed"
        output_dict = {"script_status": script_status, "step_status_message": step_status_message,
                       "failure_reason": failure_reason}
        status = True
        return status, output_dict
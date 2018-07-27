"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

# -*- coding: utf-8 -*-
import json
import multiprocessing
import os
import queue
import subprocess
from io import open

# import native
from django.http import StreamingHttpResponse

from katana.utils.navigator_util import Navigator

# declaring navigator_util in global scope
NAV = Navigator()


class MultiprocessingUtils():

    def __init__(self):
        """
               Constructor for execution app
               """
        self.katana_dir = NAV.get_katana_dir()
        self.config_json = os.path.join(self.katana_dir,
                                        'config.json')
        self.warrior = os.path.join(NAV.get_warrior_dir(),
                                    'Warrior')

    def call_subprocess(self, cmd):
        # invoke subprocess to perform execution of warrior_cmd
        output = subprocess.Popen(cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)
        return output

    def execute(self, request):

        # After clicking on execute, a request is formulated
        data_dict = json.loads(request.GET.get('data'))
        execution_file_list = data_dict['execution_file_list']
        cmd_string = data_dict['cmd_string']
        live_html_res_file = data_dict['liveHtmlFpath']
        config_json_dict = json.loads(open(self.config_json).read())
        python_path = config_json_dict['pythonpath']

        # define multiprocessing's manager
        manager = multiprocessing.Manager()
        # define queue
        live_console_obj = manager.Queue()

        if not pool_object.apply_async(self.stream_warrior_output, (self.warrior,
                                                                    live_console_obj,
                                                                    cmd_string,
                                                                    execution_file_list,
                                                                    live_html_res_file,
                                                                    python_path)):
            print("apply_async object not returned")
        return StreamingHttpResponse(self.get_stream_result(live_console_obj))

    def stream_warrior_output(self, warrior_exe,
                              live_console_obj,
                              cmd_string,
                              file_list,
                              live_html_res_file,
                              python_path=None):
        pypath = python_path if python_path else 'python3'
        print_cmd = '{0} {1} {2}'.format(pypath, warrior_exe, cmd_string)
        warrior_cmd = str('{0} {1} -livehtmllocn {2} {3}'.format(pypath,
                                                                 warrior_exe,
                                                                 live_html_res_file,
                                                                 cmd_string))

        output = self.call_subprocess(warrior_cmd)

        file_li_string = ""
        for item in file_list:
            li_string = "<li>{0}</li>".format(item)
            file_li_string += li_string
        file_list_html = "<ol>{0}</ol>".format(file_li_string)
        cmd_string = "<h6><strong>Command: </strong></h6>{0}<br>".format(print_cmd)
        logs_heading = "<br><h6><strong>Logs</strong>:</h6>"
        init_string = "<br><h6><strong>Executing:</strong></h6>{0}" \
                          .format(file_list_html) + cmd_string + logs_heading

        self.put_queue(output, live_console_obj)

        # before returning set eoc div on the live html results file
        with open(live_html_res_file, 'a') as html_file:
            html_file.write("<div class='eoc'></div>")

        return

    def put_queue(self, output, live_console_obj):
        # begin reading from stdout
        for line in output.stdout:
            # break when done
            if line.startswith('-I- DONE'):
                live_console_obj.put(line)
                print('...done\n\n')
                break
            live_console_obj.put(line)
        # Get rid of zombie processes, after reading stdout
        # Call wait() on the subprocess object
        output.wait()
        return

    def get_stream_result(self, live_console_obj):
        """
        Start reading from queue and report to execute_warrior()
        :param live_console_obj: Queue that holds the console execution results.
        """
        result = ' '
        while result:
            try:
                # time out after 30s
                result = live_console_obj.get(True, 30)
            except queue.Empty:
                print('Queue is empty and a timeout occured')
            if result is not None:
                yield result + '<br/>'
            if result.startswith('-I- DONE'):
                break
        yield '<br/>'


# define multiprocessing Pool object after the subprocess function
pool_object = multiprocessing.Pool(multiprocessing.cpu_count())

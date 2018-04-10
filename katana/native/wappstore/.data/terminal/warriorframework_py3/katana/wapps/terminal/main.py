# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, os
import subprocess

class Main:

    def __init__(self):
        pass

    def get_location(self):
        pass

    def terminal_stream(self, request):
        return self.runCommand(request.POST.get('data'))

    def runCommand(self, osString):
        """ Runs a command in a Terminal and returns back the output """
        output = {}
        output['output'] = ''
        if osString != 'blank_input':
            osArray = osString.split(' ')
            if osArray[0] == 'cd' and len(osArray) > 1:
                try:
                    os.chdir(osArray[1])
                except OSError as e:
                    output['output'] = str(e)
            else:
                try:
                    output['output'] = subprocess.check_output(osString, stderr=subprocess.STDOUT, shell=True)
                except (subprocess.CalledProcessError, OSError) as e:
                    output['output'] = e.output
                    pass
        output['location'] = os.getcwd()
        return output

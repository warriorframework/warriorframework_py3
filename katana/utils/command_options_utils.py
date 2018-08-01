import re
import subprocess

class CommandOptions:
    """
    Parent class for all
    command specific options parsing
    """
    def __init__(self, cmd, start, end):
        self.cmd = cmd
        self.start = start
        self.end = end
        self.response = []
        self.options = []

    def get_response(self):
        """
        gets response of the given command,
        including options
        :return:
        """
        output = subprocess.Popen([self.cmd],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)
        while output.poll() is None:
            self.response.append(output.stdout.readline())

    def options_parser(self):
        """
        Implementable command specific custom parser
        in child classes
        :return:
        """
        pass

    def get_options(self):
        """
        Trigger function to get response, and
        invoke command specific parser
        :return:
        """
        self.response = []
        self.get_response()
        self.options_parser()


class DockerRunCommandOptions(CommandOptions):
    """
    Child class for Docker Run
    command options parsing
    """
    def options_parser(self):
        si, ei = None, -1
        for i, l in enumerate(self.response):
            if re.match(self.start, l):
                si = i
            if self.end is not None and re.match(self.end, l):
                ei = i
        i = 0
        t = self.response[si+1: ei]
        while i < len(t)-2:
            # o = t[i]
            # while True:
            #     i += 1
            #     if "--" not in t[i]:
            if "--" in t[i] and "--" not in t[i+1]:
                self.options.append(t[i].replace('\n', ' ').replace('\r', ' ') + t[i+1].strip(" "))
                i += 2
            else:
                self.options.append(t[i])
                i += 1
        res = "".join(self.options)
        print(res)
        # return options

if __name__ == "__main__":
    drco = DockerRunCommandOptions(cmd="docker run --help", start="Options:", end=None)
    drco.get_options()
    # print(drco.options)
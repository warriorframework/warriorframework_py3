import re
import json
import subprocess

class CommandOptions:
    """
    Parent class for all
    command specific options parsing
    """
    class Option:
        """
        Option command, with
        name: --port or -p
        default: 0 or 1 or any other value
        description: flag description
        """
        def __init__(self, name=None, default=None, description=None):
            self.name = name
            self.default = default
            self.description = description

        def __str__(self):
            return "{}, {}, {}".format(
                self.name,
                self.default,
                self.description
            )

    def __init__(self, cmd, start, end):
        self.cmd = cmd
        self.start = start
        self.end = end
        self.response = []
        self.options = []
        self.get_options()

    def __str__(self):
        return "\n".join(["{}, {}, {}".format(
            option.name,
            option.default,
            option.description)
            for option in self.options])

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
        self.get_response()
        self.options_parser()

    def get_options_json(self):
        """
        converts list of Options,
        to list of json
        :return:
        """
        return json.loads(json.dumps(self.options, default=lambda option: option.__dict__))


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
        # flags = [i for i, o in enumerate(t) if "--" in o]
        res = "".join(t)
        # while i < len(t)-2:
        #     # o = t[i]
        #     # while True:
        #     #     i += 1
        #     #     if "--" not in t[i]:
        #     if "--" in t[i] and "--" not in t[i+1]:
        #         self.options.append(t[i].replace('\n', ' ').replace('\r', ' ') + t[i+1].strip(" "))
        #         i += 2
        #     else:
        #         self.options.append(t[i])
        #         i += 1
        # res = "".join(self.options)
        res = res.replace('\n', '').replace('\t', '')
        option1 = CommandOptions.Option("--add-host list",
                                        "",
                                        "Add a custom host-to-IP mapping (host:ip)")
        option2 = CommandOptions.Option("--add-host list",
                                        "",
                                        "Add a custom host-to-IP mapping (host:ip)")
        self.options.append(option1)
        self.options.append(option2)

if __name__ == "__main__":
    drco = DockerRunCommandOptions(cmd="docker run --help", start="Options:", end=None)
    print(drco.get_options_json())
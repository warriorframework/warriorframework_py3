import sys
import os
import inspect
import importlib
import re
import pkgutil
from string import Template

class CreateWrappeKwActions:

    def __init__(self, warrior_dir):
        """Constructor for WriteWrappeKwActions Class"""
        self.warrior_dir = warrior_dir
        # This can be removed after merging WAR-1960 PR
        sys.path.insert(0, self.warrior_dir)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        rel_template_path = "../templates/kw_sequencer/kw_sequencer_template"
        self.kw_sequencer_template = os.path.join(current_dir, rel_template_path)

    def write_wrapper_kw(self, action_file, wrapper_kw_name, w_desc, sub_keywords):
        """ Writes wrapper keyword in the corresponding action file """

        action_file_abspath = os.path.join(self.warrior_dir, action_file)
        vars_to_replace = {'keyword_doc_list': ""}
        keyword_doc_template = ("The keyword '{}' in Driver '{}' has defined "
                                "arguments\n        '{}'.\n        ")
        vars_to_replace['wrapper_kw'] = wrapper_kw_name
        vars_to_replace['wdesc'] = w_desc
        action_file_classpath = ".".join(os.path.splitext(action_file)[0].split(os.sep))
        action_module = importlib.import_module(action_file_classpath)
        action_class = inspect.getmembers(action_module, inspect.isclass)[0][1]
        action_methods = [item[0] for item in inspect.getmembers(action_class, inspect.isroutine)]
        if vars_to_replace['wrapper_kw'] in action_methods:
            print("Wrapper Keyword '{}' already exists in '{}'. Please create a Wrapper Keyword "
                  "with different name.".format(vars_to_replace['wrapper_kw'],
                                                action_file_abspath))
            return False
        keyword_details = []
        for sub_keyword in sub_keywords:
            sub_kw_action = self.get_action(sub_keyword['@Driver'], sub_keyword['@Keyword'])
            if action_file_classpath != sub_kw_action.__module__:
                # the sub keyword action is different from the wrapper keyword
                # action, hence need to import
                keyword_action_class = sub_kw_action.__module__+'.'+sub_kw_action.__name__
            else:
                # the sub keyword action is same as wrapper keyword action,
                # hence can be called directly with self
                keyword_action_class = ''
            arguments = sub_keyword.get('Arguments')
            if arguments:
                argument_list = arguments.get('argument')
                kw_args = {arg.get('@name'): arg.get('@value') for arg in argument_list}
            keyword_details.append((sub_keyword['@Keyword'], keyword_action_class, kw_args))
            # documenation of individual keywords in the katana is generated here
            arg_list_str = ','.join(['{}="{}"'.format(key, value)
                                     for (key, value) in kw_args.items()])
            vars_to_replace['keyword_doc_list'] += keyword_doc_template.format(
                                                    sub_keyword['@Keyword'],
                                                    sub_keyword['@Driver'], arg_list_str)

        # generating the code to substitute keyword_details in template
        # this would be a list of three-tuples where each three tuple
        # corresponds to a subkeyword with details of (keyword name,
        # action class corresponding to the keyword, dictionary of named arguments)
        ws27 = ',\n'+' '*27
        ws28 = ws27+' '
        inner_to_print_list = ['('+ws28.join(["'{}', '{}'".format(a, b),
                                              str(c)])+')' for (a, b, c) in keyword_details]
        outer_to_print = '['+ws27.join(inner_to_print_list)+']'
        vars_to_replace['keyword_details'] = outer_to_print

        # vars_to_replace is used here to sustitute the patterns in keyword template
        # which would be appended as wrapper keyword in the corresponding action class
        with open(self.kw_sequencer_template) as kwseqtemp:
            kwseqtempstr = kwseqtemp.read()
        kwseqtemp = Template(kwseqtempstr)
        kwseqtempstr = kwseqtemp.substitute(vars_to_replace)

        # appending the wrapper keyword code to the action class corresponding to wrapper keyword
        try:
            with open(action_file_abspath, 'a') as actfile:
                actfile.write(kwseqtempstr)
        except Exception as e:
            print("got exception '{}' while writing to action file".format(e))
            print("Error writing keyword '{}' to actionfile "
                  "'{}'".format(vars_to_replace['wrapper_kw'], action_file_abspath))
            return False

        print("wrapper keyword '{}' saved in the path "
              "'{}'".format(vars_to_replace['wrapper_kw'], action_file_abspath))
        return True

    def get_action(self, driver, keyword):
        """ Return the class name corresponding to the keyword in the driver """
        class_name = None
        drvmod = 'ProductDrivers.' + driver
        drvmodobj = importlib.import_module(drvmod)
        drvfile_methods = inspect.getmembers(drvmodobj, inspect.isroutine)
        main_method = [item[1] for item in drvfile_methods if item[0] == 'main'][0]
        main_src = inspect.getsource(main_method)
        pkglstmatch = re.search(r'package_list.*=.*\[(.*)\]', main_src, re.MULTILINE | re.DOTALL)
        pkglst = pkglstmatch.group(1).split(',')
        for pkg in pkglst:
            pkgobj = importlib.import_module(pkg)
            pkgdir = os.path.dirname(pkgobj.__file__)
            action_modules = [pkg+'.'+name for _, name, _ in pkgutil.iter_modules([pkgdir])]
            action_module_objs = [importlib.import_module(action_module)
                                  for action_module in action_modules]
            for action_module_obj in action_module_objs:
                for action_class in inspect.getmembers(action_module_obj, inspect.isclass):
                    for func_name in inspect.getmembers(action_class[1], inspect.isroutine):
                        if keyword == func_name[0]:
                            class_name = action_class[1]
        return class_name

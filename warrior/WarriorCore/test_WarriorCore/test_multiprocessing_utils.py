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

'''
UT for multiprocessing
'''

import os
import sys
from argparse import Namespace
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest

try:
    import warrior
    # except ModuleNotFoundError as error:
except Exception as e:
    # import pdb
    # pdb.set_trace()
    sys.path.append('/'.join(__file__.split('/')[:-4]))
    import warrior

multiprocessing = MagicMock(return_value=None)

from warrior.WarriorCore import multiprocessing_utils


def test_create_and_start_process_with_queue():
    """Creates python multiprocesses for the provided target module with the
    provided arguments and  starts them
    """

    from warrior.WarriorCore.multiprocessing_utils import create_and_start_process_with_queue

    class exmp1(object):
        """docstring for exmp1"""
        def __init__(self, arg):
            super(exmp1, self).__init__()
            self.arg = arg
    class exmp2(object):
        """docstring for exmp1"""
        def __init__(self, arg):
            super(exmp2, self).__init__()
            self.arg = arg
            
    class Manager(object):
        """docstring for ClassName"""
        def __init__(self, arg):
            super(Manager, self).__init__()
            self.arg = arg
        def Queue(self):
            return exmp1()
            
    Process = MagicMock(return_value='process')
    # Manager().Queue()
    target_module = exmp2('')
    args_dict = {}
    jobs_list = []
    output_q = None

    create_and_start_process_with_queue(target_module, args_dict, jobs_list, output_q, p_name='')

def test_get_results_from_queue():
    """Get the result form the provided multiprocessing queue object """

    from warrior.WarriorCore.multiprocessing_utils import get_results_from_queue

    class exmp1(object):
        """docstring for exmp1"""
        def __init__(self, arg):
            super(exmp1, self).__init__()
            self.arg = arg
    class exmp2(object):
        """docstring for exmp1"""
        def __init__(self, arg):
            super(exmp2, self).__init__()
            self.arg = arg

    class queue(object):
        """docstring for queue"""
        def __init__(self, arg):
            super(queue, self).__init__()
            self.arg = arg
        def qsize(self):
            return 2
        def get(self):
            return "some str"
            
    queue = queue('')
    # result_list = []
    # for _ in range(queue.qsize()):
    #     # print type(queue), queue.qsize()
    #     result_list.append(queue.get())
    # return result_list

    get_results_from_queue(queue)

def test_update_attribute():
    """merge the count for 2 attribute dictionary
    Arguments:
    1. dict1 = target dict
    2. dict2 = obtain count from this dict and put in dict1
    """

    from warrior.WarriorCore.multiprocessing_utils import update_attribute    

    dict1 = {'errors':'1'}
    dict2 = {'errors':'2'}

    update_attribute(dict1, dict2)

# def test_update_pj_junit_resultfile():
#     """loop through ts_junit object and attach suite result to project(testsuites)
#     :Arguments:
#         1. pj_junit_obj = target project
#         2. ts_junit_list = list of suite junit objects
#     """
#     import pdb
#     pdb.set_trace()
#     from warrior.WarriorCore.multiprocessing_utils import update_pj_junit_resultfile

#     iter = MagicMock(return_value='testsuite')

#     class root(object):
#         """docstring for root"""
#         def __init__(self, arg):
#             super(root, self).__init__()
#             self.arg = arg
#         def smpl(self):
#             return ['a', 'b']
#         smpl('')
#     class exmp1(object):
#         """docstring for exmp1"""
#         def __init__(self, arg):
#             super(exmp1, self).__init__()
#             self.arg = arg
#         # root = smpl('')
#         Root = root('')
#         Root.smpl()

#     class exmp2(object):
#         """docstring for exmp1"""
#         def __init__(self, arg):
#             super(exmp2, self).__init__()
#             self.arg = arg

#     ts_junit_obj1 = exmp1('')
#     ts_junit_obj2 = exmp2('')    


#     ts_junit_list = [ts_junit_obj1, ts_junit_obj2]
    
#     for ts_junit_obj in ts_junit_list:
#         for ts in ts_junit_obj.root.iter('testsuite'):
#             # append suite result to testsuites
#             pj_junit_obj.root.append(ts)
#         # update the count in testsuites attribute
#         pj_junit_obj.attrib = update_attribute(pj_junit_obj.root.attrib,
#                                                ts_junit_obj.root.attrib)
#     # return pj_junit_obj



#     update_pj_junit_resultfile(pj_junit_obj, ts_junit_list)

import imp

from utils.directory_traversal_utils import join_path


class CreateWrappeKwActions:

    def __init__(self, action_file, wrapper_kw_name, w_desc, sub_keywords):
        """Constructor for WriteWrappeKwActions Class"""
        self.action_file = action_file
        self.wrapper_kw_name = wrapper_kw_name
        self.w_desc = w_desc
        self.sub_keywords = sub_keywords

    def write_wrapper_kw(self):
        """ Writes wrapper keyword in the corresponding action file """
        pass

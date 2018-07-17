import os
from utils.directory_traversal_utils import create_dir
from utils.user_utils import get_username
from wui.core.core_utils.app_info_class import AppInformation


class CreateWarriorRecon:

    def __init__(self, parent_dir):
        """
        This is the constructor for CreateWarriorRecon. It records the parent directory and
        location of the warrior_recon directory here.

        dir_structure contains the directories that should be created inside warrior_recon

        :param parent_dir: directory when warrior_recon will be created

        """
        self.parent_dir = parent_dir
        self.user_data_dir = os.path.join(self.parent_dir, "warrior_recon")
        self.dir_structure = {
            "user_data": {
                get_username(): {
                    "wapps_data": self.get_wapps_dirs()
                }
            }
        }

    def create_warrior_recon_dir(self):
        """
        Creates the warrior_recon directory in specified location. If the creation of directory is
        successful, the internal directories are created. If the warrior_recon directory already
        exists, internal directories will be created only if they are missing.

        This function needs to be called explicitly.
        """
        if not create_dir(self.user_data_dir):
            print("-- An Error Occurred -- Something went wrong while creating the "
                  "warrior_recon directory")
        else:
            self.create_recon_sub_dirs(self.user_data_dir, self.dir_structure)

    def create_recon_sub_dirs(self, parent, dir_structure):
        """
        Recursive function that takes in a parent directory and dir_structure JSON and calls itself
        to create internal directories

        :param parent: Parent directory where internal directories should be created
        :param dir_structure: JSON containing internal directory structure
        """
        if type(dir_structure) is dict:
            # Iterates through dictionary and calls self.create_recon_sub_dirs() to create dirs
            for key, value in dir_structure.items():
                current_dir = os.path.join(parent, key)
                if create_dir(current_dir):
                    self.create_recon_sub_dirs(current_dir, value)
                else:
                    print("-- An Error Occurred -- Something went wrong while creating the {0} "
                          "directory".format(current_dir))
        elif type(dir_structure) is str:
            # If str, creates the directory (base case)
            current_dir = os.path.join(parent, dir_structure)
            if not create_dir(current_dir):
                print("-- An Error Occurred -- Something went wrong while creating the {0} "
                      "directory".format(current_dir))
        elif type(dir_structure) is list:
            # iterates through list and calls self.create_recon_sub_dirs()
            for d in dir_structure:
                self.create_recon_sub_dirs(parent, d)
        else:
            # Error handling (base case)
            print("-- An Error Occurred -- {0} not recognized".format(dir_structure))

    @staticmethod
    def get_wapps_dirs():
        """
        Gets all installed wapp names and add them to output dictionary.
        :return: dictionary containing wapp names as keys and their value as a list containing
                 .data and wapp_log directory
                 Eg: {"settings": [".data", "wapp_logs"]}
        """
        output = {}
        for app in AppInformation.information.apps:
            output[app.app_dir_name] = [".data", "wapp_logs"]
        return output

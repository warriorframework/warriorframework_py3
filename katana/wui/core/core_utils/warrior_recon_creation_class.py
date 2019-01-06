import getpass
import os
from utils.directory_traversal_utils import create_dir, get_parent_directory
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
                self.get_username(): {
                    "wapps_data": self.get_wapps_dirs()
                }
            }
        }
        self.output = {"status": True, "message": "", "data_directory": self.user_data_dir}

    def create_warrior_recon_dir(self):
        """
        Creates the warrior_recon directory in specified location. If the creation of directory is
        successful, the internal directories are created. If the warrior_recon directory already
        exists, internal directories will be created only if they are missing.

        This function needs to be called explicitly.
        """
        if not create_dir(self.user_data_dir):
            self._record_output("Something went wrong while creating the warrior_recon directory")
        else:
            self.create_recon_sub_dirs(self.user_data_dir, self.dir_structure)
        return self.output

    def verify_existing_warrior_recon_dir(self):
        """
        Creates missing internal directories.

        This function needs to be called explicitly.
        """
        self.user_data_dir = self.parent_dir
        self.parent_dir = get_parent_directory(self.user_data_dir)
        self.output.update({"data_directory": self.user_data_dir})
        self.create_recon_sub_dirs(self.user_data_dir, self.dir_structure)
        return self.output

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
                    self._record_output("Something went wrong while creating the {0} "
                                        "directory".format(current_dir))
        elif type(dir_structure) is str:
            # If str, creates the directory (base case)
            current_dir = os.path.join(parent, dir_structure)
            if not create_dir(current_dir):
                self._record_output("Something went wrong while creating the {0} "
                                    "directory".format(current_dir))
        elif type(dir_structure) is list:
            # iterates through list and calls self.create_recon_sub_dirs()
            for d in dir_structure:
                self.create_recon_sub_dirs(parent, d)
        else:
            # Error handling (base case)
            self._record_output("{0} not recognized".format(dir_structure))

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

    def _record_output(self, message):
        self.output["status"] = False
        self.output["message"] += message + "\n"
        print("-- An Error Occurred -- {0}".format(message))

    @staticmethod
    def get_username():
        """
        Returns the current username
        """
        return getpass.getuser()

    # TODO: Check if it is required for this method to be part of class or as an independent function.
    def create_user_dir(self, path):
        """
        Creates user directory should it not already exist.
        :param path: Path to create directories.
        """
        if path and isinstance(path, str):
            try:
                os.makedirs(path)
            except OSError as file_exception:
                print("-- An Error Occurred -- {}".format(file_exception))
        else:
            print("-- An Error Occurred -- Incorrect args provided. Please verify the arguments.")

import json
import os
from django.conf import settings

from katana.utils.navigator_util import Navigator
from .directory_traversal_utils import get_parent_dir_path, join_path, file_or_dir_exists

DOTDATA = '.data'
WAPPLOGS = 'wapp_logs'


class UserData:
    # constructor for class User_data
    def __init__(self, wapp_name, username=None):
        self.username = username
        self.wapp_name = wapp_name

    # define method, get .data directory
    # given request object
    def get_dotdata_dir(self, request):
        # get location to .data
        username = user_authenticated(request)
        if username is not None and self.wapp_name is not None:
            self.username = username
            wapp_name = self.wapp_name
            # get top level directory for user_data
            top_dir = get_user_home_dir(username)
            if top_dir is not "":
                dotdata_dir = join_path(top_dir, username, wapp_name, DOTDATA)
                if file_or_dir_exists(dotdata_dir):
                    return dotdata_dir
            else:
                print('top_dir not found')
                return None
        else:
            print('.data directory not found')
            return None

    # define method, get wapp_logs
    # given request object
    def get_wapplogs_dir(self, request):
        # get location to wapp_logs
        username = user_authenticated(request)
        if username is not None and self.wapp_name is not None:
            self.username = username
            wapp_name = self.wapp_name
            # get top level directory for user_data
            top_dir = get_user_home_dir(username)
            if top_dir is not "":
                wapplogs_dir = join_path(top_dir, username, wapp_name, WAPPLOGS)
                if file_or_dir_exists(wapplogs_dir):
                    return wapplogs_dir
            else:
                print('top_dir not found')
                return None
        else:
            print('wapp_logs directory not found')
            return None



def get_user_home_dir(username=None):
    """
    Returns the home directory for the provided username
    uses the value of the variable USER_HOME_DIR_TEMPLATE in settings.py and
    replaces the occurrence of {username} in it
    """
    user_home_dir = None
    user_home_dir_template = getattr(settings, 'USER_HOME_DIR_TEMPLATE', None)
    if user_home_dir_template:
        user_home_dir = user_home_dir_template.format(username=(username if username else ""))
    return user_home_dir


def get_user_data():
    """
    function is still used for backward compatibility,
    can be deprecated once completely handled by client server model
    """
    userdata = {}
    nav_obj = Navigator()
    json_file = os.path.join(nav_obj.get_katana_dir() + "user_profile.json")
    try:
        with open(json_file, 'r') as f:
            userdata = json.load(f)
    except Exception as e:
        print("-- An Error Occurred -- {0}".format(e))
        print("User data could not be retrieved.")
    return userdata


# check if user is authenticated using the request object
def user_authenticated(request):
    if request.user.is_authenticated():
        return request.user.username
    else:
        return None

import json
import os
from django.conf import settings
from utils.navigator_util import Navigator


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
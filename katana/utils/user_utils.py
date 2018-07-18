import getpass
import json

import os
from django.conf import settings

from utils.navigator_util import Navigator


def get_user_home_dir(username):
    """
    Returns the home directory for the provided username
    uses the value of the variable USER_HOME_DIR_TEMPLATE in settings.py and
    replaces the occurrence of {username} in it
    """
    user_home_dir = os.path.expanduser("~")
    user_home_dir_template = getattr(settings, 'USER_HOME_DIR_TEMPLATE', None)
    if user_home_dir_template:
        user_home_dir = user_home_dir_template.format(username=(username if username else ""))
    return user_home_dir


def get_username(request=None):
    """
    Returns the current username
    """
    username = False
    if request is not None and 'data' in request.POST:
        data_dict = json.loads(request.POST.get('data'))
        username = data_dict.get('username', False)
    if not username:
        username = getpass.getuser()
    return username


def get_password(request=None):
    """
    Returns the current username
    """
    password = False
    if request is not None and 'data' in request.POST:
        data_dict = json.loads(request.POST.get('data'))
        password = data_dict.get('password', False)
    return password


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
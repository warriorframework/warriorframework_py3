from django.conf import settings

class UserData():
    # constructor for class User_data
    def __init__(self, wapp_name):
        self.wapp_name = wapp_name

    def get_user_path(self, request):
        username = user_authenticated(request)
        if username is not None:
            top_dir = get_user_home_dir(username)
            if top_dir:
                user_dir = join_path(top_dir, USERDATA, username)
                return user_dir
            else:
                print('-- An Error Occurred -- fetching of top level directory resulted in a empty string')
                return None
        else:
            print('-- An Error Occurred -- user not authenticated')
            return None

    def get_dotdata_dir(self, request):
        """
        get .data directory, given request object
        :param request:
        :return:
        """
        dotdata_dir = None
        # get location to .data
        wapp_name = self.wapp_name
        # get top level directory for user_data
        user_path = self.get_user_path(self, request)
        if user_path and wapp_name:
            dotdata_dir = join_path(user_path, WAPPSDATA, wapp_name, DOTDATA)
            if not file_or_dir_exists(dotdata_dir):
                print('-- An Error Occurred -- file_or_dir_exists not found. Creating directory...')
                # create the directory
                warrior_recon = CreateWarriorRecon()
                warrior_recon.create_user_dir(dotdata_dir)
        else:
            print('-- An Error Occurred -- user_path or wapp_name not found')
        return dotdata_dir

    def get_wapplogs_dir(self, request):
        """
        get wapp_logs, given request object
        :param request: Request object
        :return:
        """
        wapplogs_dir = None
        # get location to wapp_logs
        wapp_name = self.wapp_name
        # get top level directory for user_data
        user_path = self.get_user_path(self, request)
        if user_path and wapp_name:
            wapplogs_dir = join_path(user_path, WAPPSDATA, wapp_name, WAPPLOGS)
            if not file_or_dir_exists(wapplogs_dir):
                print('-- An Error Occurred -- file_or_dir_exists not found. Creating directory...')
                # create the directory
                warrior_recon = CreateWarriorRecon()
                warrior_recon.create_user_dir(wapplogs_dir)
        else:
            print('-- An Error Occurred -- user_path or wapp_name not found')
        return wapplogs_dir


def user_authenticated(request):
    """
    check if user is authenticated using the request object
    :param request: Request object
    :return:
    """
    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.username
    return user_name


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
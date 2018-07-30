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
        # get top level directory for user_data
        top_dir = get_top_level_dir()
        # get location to .data
        username = user_authenticated(request)
        if username is not None and self.wapp_name is not None:
            self.username = username
            wapp_name = self.wapp_name
            dotdata_dir = join_path(top_dir, username, wapp_name, DOTDATA)
            if file_or_dir_exists(dotdata_dir):
                return dotdata_dir
        else:
            print('.data directory not found')
            return None

    # define method, get wapp_logs
    # given request object
    def get_wapplogs_dir(self, request):
        # get top level directory for user_data
        top_dir = get_top_level_dir()
        # get location to wapp_logs
        username = user_authenticated(request)
        if username is not None and self.wapp_name is not None:
            self.username = username
            wapp_name = self.wapp_name
            wapplogs_dir = join_path(top_dir, username, wapp_name, WAPPLOGS)
            if file_or_dir_exists(wapplogs_dir):
                return wapplogs_dir
        else:
            print('wapp_logs directory not found')
            return None


# stub to get top level directory
def get_top_level_dir():
    nav = Navigator()
    return get_parent_dir_path(nav.get_katana_dir())

# check if user is authenticated using the request object
def user_authenticated(request):
    if request.user.is_authenticated():
        return request.user.username
    else:
        return None

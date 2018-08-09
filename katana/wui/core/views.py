"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import os
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from utils.directory_traversal_utils import get_parent_directory, join_path, file_or_dir_exists
from utils.file_utils import readlines_from_file, write_to_file
from utils.json_utils import read_json_data
from utils.navigator_util import Navigator
from utils import user_utils
from utils.user_utils import get_user_home_dir, get_user_data
from wui.core.apps import AppInformation
from wui.core.core_utils.core_utils import get_local_home_directory, get_suggested_home_dir
from wui.core.core_utils.warrior_recon_creation_class import CreateWarriorRecon

templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'core')
try:
    import django_auth_ldap.backend
except Exception as e:
    print(e)

try:
    from django_auth_ldap.backend import LDAPBackend
except Exception as err:
    print("Please install django auth ldap to authenticate against ldap")
    print("Error while importing django auth ldap: \n", err)


def refresh_landing_page(request):
    return render(request, 'core/landing_page.html',
                  {"apps": AppInformation.information.apps})


def get_file_explorer_data(request):
    nav_obj = Navigator()
    if "data[start_dir]" in request.POST and request.POST["data[start_dir]"] != "false":
        start_dir = request.POST["data[start_dir]"]
    elif "data[path]" in request.POST and request.POST["data[path]"] != "false":
        start_dir = get_parent_directory(request.POST["data[path]"])
    else:
        start_dir = join_path(nav_obj.get_warrior_dir(), "Warriorspace")
    output = nav_obj.get_dir_tree_json(start_dir_path=start_dir)
    return JsonResponse(output)


def read_config_file(request):
    nav_obj = Navigator()
    config_file_path = join_path(nav_obj.get_katana_dir(), "config.json")
    data = read_json_data(config_file_path)
    if data is None:
        data = False
    return JsonResponse(data)


def check_if_file_exists(request):
    filename = request.POST.get("filename")
    directory = request.POST.get("directory")
    extension = request.POST.get("extension")
    path = request.POST.get("path")
    if path is not None:
        output = {"exists": file_or_dir_exists(path)}
    else:
        output = {"exists": file_or_dir_exists(join_path(directory, filename + extension))}
    return JsonResponse(output)


class UserAuthView(View):
    """
    User authentication view
    """    
    
    def __init__(self, **kwargs):
        """
        constructor for the view
        """
        self.index_page = os.path.join(templates_dir, 'unified_index.html')
        self.home_page = os.path.join(templates_dir, 'home_page.html')
        self.configured_ldap = False
        if hasattr(settings, 'AUTH_LDAP_SERVER_URI') and settings.AUTH_LDAP_SERVER_URI:
            self.configured_ldap = True
        self.userprofile  = None
        self.username = None
        self.password = None
        self.op_dict = {'auth_status': 0, 'redirect_url': None}     
        self.action_method_map = {
            'login': self.get_login_page,
            'logout': self.logout_user,
            'redirect_to_home_page': self.redirect_to_home_page
        }

    def get(self, request):
        """
        Render the form for user authentication
        """
        req_data = request.GET.get('data')
        data_dict = json.loads(req_data) if req_data else {}
        action = data_dict.get('action')
        method = self.action_method_map.get(action, self.get_login_page)
        return method(request)
    
    def post(self, request):
        """
        authenticate and login a user
        auth_status = 0 means authentication failed
                      1 means authentication success
                      2 means multi user supported but no home dir for user
        
        """
        data_dict = json.loads(request.POST.get('data'))
        self.username = data_dict.get('username', None)
        self.password = data_dict.get('password')
        # authenticate, login  the user
        self.userprofile = self.authenticate_user()    
        multi_user_support = getattr(settings, 'MULTI_USER_SUPPORT', False)
        home_dir_template = get_user_home_dir(self.username)
        # if multi user support is False then just login user
        if not multi_user_support:
            self.login_user(request)

        # if multi user supported then home_dir_template is mandatory
        if multi_user_support:
            if not home_dir_template:
                self.op_dict['msg'] = "Please configure HOME_DIR_TEMPLATE in settings, mandatory in case \
                of multi user environment."
                self.op_dict['auth_status'] = 2
            else:
                self.login_user(request)
        return JsonResponse(self.op_dict)

    def authenticate_user(self):
        """
        authenticate the user
        """
        userprofile = None
        try:
            userprofile = authenticate(username=self.username, password=self.password)
        except Exception as err:
            print(err)
            self.op_dict['msg'] = err
        return userprofile
    
    def login_user(self, request):
        """
        login an authenticated user

        """
        try:
            if self.userprofile is not None:
                self.op_dict['msg'] = "authentication for user={0} successful.".format(self.username)
                home_dir = user_utils.get_user_home_dir(self.username)              
                
                login(request, self.userprofile)
                request.session['home_dir'] = home_dir
                self.op_dict['redirect_url'] = 'home/'                
                self.op_dict['auth_status'] = 1
            
            else:
                self.op_dict['msg'] = "authentication for user={0} failed.".format(self.username)
        except Exception as err:
            self.op_dict['msg'] = str(err)
    
    def redirect_to_home_page(self, request):
        """
        on successful login build the homepage for the user
        """
        user_data = get_user_data()
        home_dir = False if self.configured_ldap else get_local_home_directory()
        suggested_home_dir = False if home_dir else get_suggested_home_dir()
        data = {"apps": AppInformation.information.apps, "userData": user_data,
                "configured_ldap": self.configured_ldap, "home_directory": home_dir,
                "suggested_home_directory": suggested_home_dir}
        return render(request, self.index_page, data)

    def get_login_page(self, request):
        """
        Sends the index_page as response.
        """
        user_data = get_user_data()
        home_dir = False if self.configured_ldap else get_local_home_directory()
        suggested_home_dir = False if home_dir else get_suggested_home_dir()
        data = {"apps": AppInformation.information.apps, "userData": user_data,
                "configured_ldap": self.configured_ldap, "home_directory": home_dir,
                "suggested_home_directory": suggested_home_dir}
        return render(request, self.index_page, data)

    def logout_user(self, request):
        """
        logout the user
        """
        logout(request)
        path = request.get_full_path()
        self.op_dict['redirect_url'] = '/'
        return JsonResponse(self.op_dict)


def setup_data_location(request):
    """
    This function sets up a local data directory
    :param request: Contains path to data directory and whether or not it is an existing data
           storage directory or not
    :return:
    """
    data_directory = request.POST.get('path_to_data_directory')
    existing = request.POST.get('existing') == 'true'
    output = {"message": "Data storage successfully imported" if existing else "Data storage successfully created"}
    if os.path.isdir(data_directory):
        output["status"] = True
        cwr_obj = CreateWarriorRecon(data_directory)
        if existing:
            # Verify existing data directory
            output = cwr_obj.verify_existing_warrior_recon_dir()
        else:
            # Create new data directory (warrior_recon)
            output = cwr_obj.create_warrior_recon_dir()
    else:
        print("-- An Error Occurred -- {0} does not exist or is not a directory".format(data_directory))
        output["status"] = False
        output["message"] = "{0} does not exist or is not a directory.".format(data_directory)

    if output["status"]:
        # Update settings.py file
        data = readlines_from_file(join_path(Navigator().get_katana_dir(), "wui", "settings.py"))

        for i, line in enumerate(data):
            if line.strip().startswith('USER_HOME_DIR_TEMPLATE'):
                data[i] = "USER_HOME_DIR_TEMPLATE = \"{0}\"\n".format(output["data_directory"])
                settings.USER_HOME_DIR_TEMPLATE = output["data_directory"]
                break

        write_to_file(join_path(Navigator().get_katana_dir(), "wui", "settings.py"), "".join(data))
    return JsonResponse(output)

    # ===============================================================================
    # !!!!! This functionality has been moved to UserAuthView class (scroll down)
    # commenting the code for now.
    # once backward compatibility has been safely verified after testing thoroughly
    # the commented code can be deleted !!!!
    #
    # class CoreView(View):
    #
    #     def __init__(self):
    #         self.navigator = Navigator()
    #
    #     def get_user_data(self):
    #         json_file = self.navigator.get_katana_dir() + '/user_profile.json'
    #         with open(json_file, 'r') as f:
    #             json_data = json.load(f)
    #         return json_data
    #
    #     def get(self, request):
    #         """
    #         This get function get information about the installed apps
    #
    #         Args:
    #             request: HttpRequest that contains metadata about the request
    #
    #         Returns:
    #             HttpResponse: containing an HTML template and data
    #                 HTML template: core/index.html
    #                 Data: [{"url":"/url/of/app", "name": "app_name",
    #                         "icon": "icon_name", "color": "red"}]
    #
    #         """
    #         print('hi')
    #         template = 'core/index.html'
    #         return render(request, template, {"apps": AppInformation.information.apps,
    #                                            "userData": self.get_user_data()})
    # ===============================================================================
    
    
    #===========================================================================
    # for future use, remain commented for now
    #
    #
    # def get_home_dir(self, request):
    #     """
    #     get the home directory associated to the user.
    #     """
    #     home_dir = True
    #     auth_backend = request.session['_auth_user_backend']
    #    
    #     if auth_backend == 'django_auth_ldap.backend.LDAPBackend':
    #         # get home_dir of the user
    #         attrs_req = ['homeDirectory', 'homeDrive']
    #         home_dir = self.get_ldap_user_attrib(request, attrs_req)
    #         print(home_dir, type(home_dir))
    #         
    #         pass
    #     
    #     
    #     return True
    #===========================================================================
    
    #===========================================================================
    # for future use remain commented for now
    #
    # def get_ldap_user_attrib(self, request, attrs):
    #     """
    #     if attribs req is an empty list then return all the attribs
    #     as dict 
    #     """
    #     #print('user_dict:',request.user.__dict__)
    #     attribs = {}
    #     import ldap
    #     import ldap.filter
    #     ldap_uri = settings.AUTH_LDAP_SERVER_URI
    #     bind_dn = settings.AUTH_LDAP_BIND_DN
    #     bind_dn_password = settings.AUTH_LDAP_BIND_PASSWORD
    #     ldap_search_base_dn = settings.AUTH_LDAP_SEARCH_BASE_DN
    #     search_username = request.user.username
    #     filter_string = '(samaccountname={0})'.format(search_username)
    #     
    #     #from django_auth_ldap.config import LDAPSearch
    #     #print('attrs:', self.userprofile.ldap_user.__dict__)
    #     
    #     #results = LDAPSearch(ldap_search_base_dn, ldap.SCOPE_SUBTREE, filter_string, ['*'])
    #     #print('results: ',results.__dict__)
    #     #=======================================================================
    #     import ldap
    #     import ldap.filter
    #     # from django_auth_ldap.config import LDAPSearch
    #     # # direct python-ldap search
    #     l = ldap.initialize(ldap_uri)    
    #     l.protocol_version = ldap.VERSION3
    #     l.simple_bind_s(bind_dn, bind_dn_password ) 
    #     results = l.search(ldap_search_base_dn, ldap.SCOPE_SUBTREE, filter_string, attrs)
    #     result_type, result_data = l.result(results, 0)
    #     op = result_data[0][1]
    #     print (op)
    #     attribs = {k: v[0].decode('utf8') for k, v in op.items()}
    #     #=======================================================================  
    #     return attribs
    #===========================================================================
    
    
        
    




    
    
    
    
    




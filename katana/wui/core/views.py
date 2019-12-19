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

# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import PasswordChangeForm
import json
import os
from katana.utils.directory_traversal_utils import get_parent_directory, join_path, file_or_dir_exists
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
from katana.wui.core.apps import AppInformation
from katana.wui.users.views import PublicView
from .core_utils.core_settings import FileSettings, LDAPSettings, Restart, EMAILSettings

try:
    from django_auth_ldap.backend import LDAPBackend
except Exception as err:
    print("Please install django auth ldap to authenticate against ldap")
    print("Error while importing django auth ldap: \n", err)


def refresh_landing_page(request):
    return render(request, 'core/landing_page.html', {"apps": AppInformation.information.apps})


def read_config_file_data():
    nav_obj = Navigator()
    config_file_path = join_path(nav_obj.get_katana_dir(), "config.json")
    data = read_json_data(config_file_path)
    return data

class getFileExplorerData(View):

    def post(self, request):
        """
        This is a post request for getting the file explorer data. It internally calls the
        get_dir_tree_json() in navigator_utils.py to get a list of directories.

        params sent via the request:

        start_dir: Absolute path to the start directory. If not given, defaulted to "Warriorspace".
        path: Absolute path to the current directory. Send a path via this argument indicates that
              information for current directory's parent needs to be obtained. If not False, it is
              prioritized over start_dir
        lazy_loading: Indicates that jsTree lazy_loading is being used and only direct
                      sub-children's information needs to be obtained.

        """
        nav_obj = Navigator()
        lazy_loading = True if "data[lazy_loading]" in request.POST and request.POST["data[lazy_loading]"].lower() == "true" else False
        start_dir = "false"
        if "data[start_dir]" in request.POST:
            start_dir = request.POST["data[start_dir]"]

        if os.environ["pipmode"] == 'True':
            config_data = read_config_file_data()
            if config_data["pythonsrcdir"] != "" and start_dir == "false":
                start_dir = config_data["pythonsrcdir"]
            elif config_data["pythonsrcdir"] == "" and start_dir == "false":
                start_dir = config_data["userreposdir"]
        else:
            if start_dir == "false":
                start_dir = join_path(nav_obj.get_warrior_dir(), "Warriorspace")

        if "data[path]" in request.POST and request.POST["data[path]"] != "false":
            start_dir = get_parent_directory(request.POST["data[path]"])
        output = nav_obj.get_dir_tree_json(start_dir_path=start_dir, lazy_loading=lazy_loading)
        return JsonResponse(output)

    def get(self, request):
        """
        This is a get request for getting the file explorer data. It internally calls the
        get_dir_tree_json() in navigator_utils.py to get a list of directories. THIS VIEW EXISTS
        ONLY BECAUSE JSTREE DOES NOT HAVE SUPPORT FOR POST IN LAZY LOADING.

        params sent via the request:

        start_dir: Absolute path to the start directory. If not given, defaulted to "Warriorspace".
        path: Absolute path to the current directory. Send a path via this argument indicates that
              information for current directory's parent needs to be obtained. If not False, it is
              prioritized over start_dir
        lazy_loading: Indicates that jsTree lazy_loading is being used and only direct
                      sub-children's information needs to be obtained.

        """
        nav_obj = Navigator()
        start_dir = "false"
        lazy_loading = True if "lazy_loading" in request.GET and request.GET["lazy_loading"].lower() == "true" else False
        config_data = read_config_file_data()

        get_children_only = False
        if "start_dir" in request.GET:
            get_children_only = True
            start_dir = request.GET["start_dir"]

        if os.environ["pipmode"] == 'True':
            if config_data["pythonsrcdir"] != "" and start_dir == "false":
                get_children_only = False
                start_dir = config_data["pythonsrcdir"]
            elif config_data["pythonsrcdir"] == "" and start_dir == "false":
                get_children_only = False
                start_dir = config_data["userreposdir"]
        else:
            if start_dir == "false":
                get_children_only = False
                start_dir = join_path(nav_obj.get_warrior_dir(), "Warriorspace")

        if "path" in request.GET:
            get_children_only = False
            start_dir = request.GET["path"]

        output = nav_obj.get_dir_tree_json(start_dir_path=start_dir, lazy_loading=lazy_loading)
        if get_children_only:
            output = output["children"]
        return JsonResponse(output, safe=False)


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


class HomeView(View):

    def __init__(self):
        self.index_page = 'core/unified_index.html'
        self.home_page = 'core/home_page.html'
        self.userprofile  = None
        self.username = None

    def get(self, request):
        user_data = self.get_user_data()
        return render(request, self.index_page, {"apps": AppInformation.information.apps, "userData": user_data})

    def get_user_data(self):
        """
        function is still used for backward compatibility,
        can be deprecated once completely handled by client server model
        """
        userdata = {}
        json_file = Navigator().get_katana_dir() + '/user_profile.json'
        with open(json_file, 'r') as f:
            userdata = json.load(f)
            return userdata


class SiteSettingsView(UserPassesTestMixin, View,):

    def test_func(self):
        return self.request.user.is_superuser and self.request.user.is_staff and self.request.user.is_active

    def get(self, request):
        ldap_settings = LDAPSettings()
        email_settings = EMAILSettings()
        context = {
            'is_site_settings': True,
            'ldap_settings': ldap_settings.configs_to_strings(),
            'ldap_enabled': ldap_settings.enabled,
            'ldap_errors': ldap_settings.errors,
            'email_settings': email_settings.configs,
        }
        return render(request, "core/site_settings.html", context=context)

    def post(self, request):
        ldap_settings = LDAPSettings()
        email_settings = EMAILSettings()
        file_errors = {}
        if request.POST.get('action', '') == 'ldap':
            new_configs = {k.upper(): v for k, v in request.POST.items()
                           if 'auth_ldap' in k and v != ""}
            # Handle enable checkbox field - not present in POST when not checked
            if 'AUTH_LDAP_ENABLED' not in new_configs:
                new_configs['AUTH_LDAP_ENABLED'] = False
            ldap_settings.update(new_configs)
            # Send messages
            if ldap_settings.errors:
                messages.error(request, 'Error found in updated LDAP settings.')
            else:
                messages.success(request, 'Successfully updated LDAP settings.')
            if not ldap_settings.errors and 'Restart' in request.POST.get('_save', 'Save'):
                messages.warning(request, 'A server restart has been triggered.')
                Restart().restart(delay=2)
        elif request.POST.get('action', '') == 'files':
            if 'ldap_cert_file' in request.FILES:
                location = LDAPSettings.get_ldap_cert_path()
                success = FileSettings().save(request.FILES['ldap_cert_file'], location)
                if success:
                    messages.success(request, 'Successfully updated files.')
                    if LDAPSettings.requires_restart_ldap_cert_file() or 'Restart' in request.POST.get('_save', 'Save'):
                        Restart().restart(delay=2)
                        messages.warning(request, 'A server restart has been triggered.')
                else:
                    messages.error(request, 'Failed to upload file(s)')
                    file_errors['ldap_cert_file'] = 'upload failed'
        elif request.POST.get('action', '') == 'email':
            new_configs = {k.upper(): v for k, v in request.POST.items()
                           if 'email' in k and v != ""}
            # Handle use_tls field - not present in POST when not checked
            if 'EMAIL_USE_TLS' not in new_configs:
                new_configs['EMAIL_USE_TLS'] = False
            email_settings.update(new_configs)
        context = {
            'is_site_settings': True,
            'ldap_settings': ldap_settings.configs_to_strings(),
            'ldap_enabled': ldap_settings.enabled,
            'ldap_errors': ldap_settings.errors,
            'file_errors': file_errors,
            'email_settings': email_settings.configs,
        }
        return render(request, "core/site_settings.html", context=context)


class LoginView(BaseLoginView, PublicView,):
    pass


class UserProfileView(View,):

    def get(self, request):
        return render(request, 'core/user_profile.html', {'apps': AppInformation.information.apps})

    def post(self, request):
        if request.user.has_usable_password():
            # Users can change their first name, last name, and email only if their password is set locally
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, "Changes have been saved successfully.")
        else:
            messages.error(request, "Changes cannot be made. Please contact an admin.")
        return self.get(request)


class UserPasswordChangeView(View,):

    def _prep_from(self, request, form):
        """ Add bootstrap classes to the form. """
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        return form

    def get(self, request):
        form = PasswordChangeForm(request.user)
        form = self._prep_from(request, form)
        return render(request, 'core/user_password_change.html',
                      {'apps': AppInformation.information.apps, 'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if not request.user.has_usable_password():
            messages.error(request, 'Your password cannot be changed. Please contact an admin.')
        elif form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Your password could not be changed.')
        form = self._prep_from(request, form)
        context = {'apps': AppInformation.information.apps, 'form': form}
        return render(request, 'core/user_password_change.html', context=context)

# ===========================================================================
#   Old UserAuthView class which combined login, logout, and home view.
#   Now deprecated, but kept commented for posterity.
# ===========================================================================
# class UserAuthView(View):
#     """
#     User authentication view
#     """
#
#     def __init__(self):
#         """
#         constructor for the view
#         """
#         self.index_page = 'core/unified_index.html'
#         self.home_page = 'core/home_page.html'
#         self.userprofile  = None
#         self.username = None
#         self.password = None
#         self.op_dict = {'auth_status': 0, 'redirect_url': None}
#         self.action_method_map = {
#                             'login': self.get_login_page,
#                             'logout': self.logout_user,
#                             'redirect_to_home_page': self.redirect_to_home_page
#                         }
#
#     def get(self, request):
#         """
#         Render the form for user authentication
#         """
#         req_data = request.GET.get('data')
#         data_dict = json.loads(req_data) if req_data else {}
#         action = data_dict.get('action')
#         method = self.action_method_map.get(action, self.get_login_page)
#         return method(request)
#
#     def post(self, request):
#         """
#         authenticate and login a user
#         auth_status = 0 means authentication failed
#                       1 means authentication success
#                       2 means multi user supported but no home dir for user
#
#         """
#
#         data_dict = json.loads(request.POST.get('data'))
#         self.username = data_dict.get('username', None)
#         self.password = data_dict.get('password')
#         # authenticate, login  the user
#         self.userprofile = self.authenticate_user()
#         multi_user_support = getattr(settings, 'MULTI_USER_SUPPORT', False)
#         home_dir_template = getattr(settings, 'USER_HOME_DIR_TEMPLATE', None)
#         # if multi user support is False then just login user
#         if not multi_user_support:
#             self.login_user(request)
#
#         # if multi user supported then home_dir_template is mandatory
#         if multi_user_support:
#             if not home_dir_template:
#                 self.op_dict['msg'] = "Please configure HOME_DIR_TEMPLATE in settings, mandatory in case \
#                 of multi user environment."
#                 self.op_dict['auth_status'] = 2
#             else:
#                 self.login_user(request)
#
#         return JsonResponse(self.op_dict)
#
#     def authenticate_user(self):
#         """
#         authenticate the user
#         """
#         userprofile = None
#         try:
#             userprofile = authenticate(username=self.username, password=self.password)
#         except Exception as err:
#             print(err)
#             self.op_dict['msg'] = err
#         return userprofile
#
#     def login_user(self, request):
#         """
#         login an authenticated user
#
#         """
#
#         try:
#             if self.userprofile is not None:
#                 self.op_dict['msg'] = "authentication for user={0} successful.".format(self.username)
#                 home_dir = user_utils.get_user_home_dir(self.username)
#
#                 login(request, self.userprofile)
#                 request.session['home_dir'] = home_dir
#                 self.op_dict['redirect_url'] = 'home/'
#                 self.op_dict['auth_status'] = 1
#
#             else:
#                 self.op_dict['msg'] = "authentication for user={0} failed.".format(self.username)
#         except Exception as err:
#             self.op_dict['msg'] = str(err)
#
#         return
#
#     def redirect_to_home_page(self, request):
#         """
#         on successful login build the homepage for the user
#         """
#         user_data = self.get_user_data()
#         return render(request, self.index_page, {"apps": AppInformation.information.apps, "userData": user_data})
#
#     def get_login_page(self, request):
#         """
#         """
#         user_data = self.get_user_data()
#         return render(request, self.index_page, {"apps": AppInformation.information.apps, "userData": user_data})
#
#     def get_user_data(self):
#         """
#         function is still used for backward compatibility,
#         can be deprecated once completely handled by client server model
#         """
#         userdata = {}
#         json_file = Navigator().get_katana_dir() + '/user_profile.json'
#         with open(json_file, 'r') as f:
#             userdata = json.load(f)
#         return userdata
#
#     def logout_user(self, request):
#         """
#         logout the user
#         """
#         logout(request)
#         path = request.get_full_path()
#         self.op_dict['redirect_url'] = '/'
#         return JsonResponse(self.op_dict)
#
#     #===========================================================================
#     # for future use, remain commented for now
#     #
#     #
#     # def get_home_dir(self, request):
#     #     """
#     #     get the home directory associated to the user.
#     #     """
#     #     home_dir = True
#     #     auth_backend = request.session['_auth_user_backend']
#     #
#     #     if auth_backend == 'django_auth_ldap.backend.LDAPBackend':
#     #         # get home_dir of the user
#     #         attrs_req = ['homeDirectory', 'homeDrive']
#     #         home_dir = self.get_ldap_user_attrib(request, attrs_req)
#     #         print(home_dir, type(home_dir))
#     #
#     #         pass
#     #
#     #
#     #     return True
#     #===========================================================================
#
#     #===========================================================================
#     # for future use remain commented for now
#     #
#     # def get_ldap_user_attrib(self, request, attrs):
#     #     """
#     #     if attribs req is an empty list then return all the attribs
#     #     as dict
#     #     """
#     #     #print('user_dict:',request.user.__dict__)
#     #     attribs = {}
#     #     import ldap
#     #     import ldap.filter
#     #     ldap_uri = settings.AUTH_LDAP_SERVER_URI
#     #     bind_dn = settings.AUTH_LDAP_BIND_DN
#     #     bind_dn_password = settings.AUTH_LDAP_BIND_PASSWORD
#     #     ldap_search_base_dn = settings.AUTH_LDAP_SEARCH_BASE_DN
#     #     search_username = request.user.username
#     #     filter_string = '(samaccountname={0})'.format(search_username)
#     #
#     #     #from django_auth_ldap.config import LDAPSearch
#     #     #print('attrs:', self.userprofile.ldap_user.__dict__)
#     #
#     #     #results = LDAPSearch(ldap_search_base_dn, ldap.SCOPE_SUBTREE, filter_string, ['*'])
#     #     #print('results: ',results.__dict__)
#     #     #=======================================================================
#     #     import ldap
#     #     import ldap.filter
#     #     # from django_auth_ldap.config import LDAPSearch
#     #     # # direct python-ldap search
#     #     l = ldap.initialize(ldap_uri)
#     #     l.protocol_version = ldap.VERSION3
#     #     l.simple_bind_s(bind_dn, bind_dn_password )
#     #     results = l.search(ldap_search_base_dn, ldap.SCOPE_SUBTREE, filter_string, attrs)
#     #     result_type, result_data = l.result(results, 0)
#     #     op = result_data[0][1]
#     #     print (op)
#     #     attribs = {k: v[0].decode('utf8') for k, v in op.items()}
#     #     #=======================================================================
#     #     return attribs
#     #===========================================================================
#



    
    
    
    
    




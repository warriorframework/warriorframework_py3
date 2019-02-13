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
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.forms import PasswordChangeForm
import json
from utils.directory_traversal_utils import get_parent_directory, join_path, file_or_dir_exists
from utils.json_utils import read_json_data
from utils.navigator_util import Navigator
from wui.core.apps import AppInformation
from wui.users.views import PublicView
from .core_utils.core_settings import FileSettings, LDAPSettings, Restart
import logging
logger = logging.getLogger(__name__)
try:
    from django_auth_ldap.backend import LDAPBackend
except Exception as err:
    print("Please install django auth ldap to authenticate against ldap")
    print("Error while importing django auth ldap: \n", err)


def refresh_landing_page(request):
    return render(request, 'core/landing_page.html', {"apps": AppInformation.information.apps})


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
        get_children_only = False
        if "start_dir" in request.GET:
            get_children_only = True
            start_dir = request.GET["start_dir"]

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
        logger.info("Katana Log: '{0}' is viewing the Home Page".format(request.user.username))
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
        context = {
            'is_site_settings': True,
            'ldap_settings': ldap_settings.configs_to_strings(),
            'ldap_enabled': ldap_settings.enabled,
            'ldap_errors': ldap_settings.errors,
        }
        return render(request, "core/site_settings.html", context=context)

    def post(self, request):
        ldap_settings = LDAPSettings()
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
        elif request.POST.get('action', '') == 'files':
            if 'ldap_cert_file' in request.FILES:
                location = LDAPSettings.get_ldap_cert_path()
                success = FileSettings().save(request.FILES['ldap_cert_file'], location)
                if success:
                    if LDAPSettings.requires_restart_ldap_cert_file():
                        Restart().restart(delay=2)
                        messages.warning(request, 'A server restart has been triggered.')
                    messages.success(request, 'Successfully updated files.')
                else:
                    messages.error(request, 'Failed to upload file(s)')
                    file_errors['ldap_cert_file'] = 'upload failed'
        context = {
            'is_site_settings': True,
            'ldap_settings': ldap_settings.configs_to_strings(),
            'ldap_enabled': ldap_settings.enabled,
            'ldap_errors': ldap_settings.errors,
            'file_errors': file_errors,
        }
        return render(request, "core/site_settings.html", context=context)


class LoginView(BaseLoginView, PublicView,):

    def dispatch(self, request, *args, **kwargs):
        username = request.POST.get("username")
        if username:
            logger.info("Katana Log: '{0}' is trying to log in".format(username))
        return super().dispatch(request, *args, **kwargs)


class LogoutView(BaseLogoutView, PublicView,):

    def dispatch(self, request, *args, **kwargs):
        logger.info("Katana Log: '{0}' has logged out".format(request.user.username))
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(View,):

    def get(self, request):
        logger.info("Katana Log: '{0}' is viewing the Profile Settings Page.".format(request.user.username))
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

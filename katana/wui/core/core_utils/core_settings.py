import configparser
from copy import copy
import json
import os
import time
import threading
from katana.utils.navigator_util import Navigator
import sys
from django.conf import settings
try:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType, LDAPSearchUnion
except Exception:
    pass


class Restart:

    def __init__(self):
        self.settings_file = os.path.join(Navigator().get_katana_dir(), 'katana.wui', 'settings.py')
        print(self.settings_file)

    def restart(self, delay=0):
        """
        Triggers a restart.
        :param delay: Delay in seconds before restart.
        :return:
        """
        threading.Thread(target=Restart._restart_job, args=[self.settings_file, delay]).start()

    @staticmethod
    def _restart_job(settings_file, delay=0):
        time.sleep(delay)
        try:
            with open(settings_file, 'a'):
                os.utime(settings_file, None)
        except Exception as ex:
            print(ex)


class FileSettings:

    def save(self, file, location):
        """
        Save file into location.
        :param file:
        :param location:
        :return: False if unable to save
        """
        try:
            with open(location, 'wb+') as fd:
                for chunk in file.chunks():
                    fd.write(chunk)
            return True
        except Exception:
            return False


class LDAPSettings:
    CONFIG_FILE = 'config.ini'
    LDAP_IMPORT_SUCCESS = 'django_auth_ldap' in sys.modules

    REQUIRED_FIELDS = [
        'AUTH_LDAP_SERVER_URI',
        'AUTH_LDAP_SEARCH_BASE_DN',
        'AUTH_LDAP_BIND_DN',
        'AUTH_LDAP_BIND_PASSWORD',
    ]
    EITHER_REQ_FIELDS = [
        ['AUTH_LDAP_USER_DN_TEMPLATE', 'AUTH_LDAP_USER_SEARCH'],
    ]
    REQUIRED_FOR_GROUP_FIELDS = [
        'AUTH_LDAP_GROUP_TYPE',
        'AUTH_LDAP_GROUP_SEARCH'
    ]
    BOOLEAN_FIELDS = [
        'AUTH_LDAP_ENABLED',
        'AUTH_LDAP_START_TLS',
    ]
    JSON_FIELDS = [
        'AUTH_LDAP_USER_ATTR_MAP',
        'AUTH_LDAP_GROUP_MAPPING',
        'AUTH_LDAP_USER_SEARCH',
    ]
    DN_FIELDS = [
        'AUTH_LDAP_SEARCH_BASE_DN',
        'AUTH_LDAP_BIND_DN',
        'AUTH_LDAP_REQUIRE_GROUP',
        'AUTH_LDAP_DENY_GROUP',
        'AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_SUPERUSER',
        'AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_STAFF',
    ]

    def __init__(self, config_file=None):
        self.enabled = False
        self.configs = {}
        self.errors = {}
        if config_file:
            # Get from config file
            LDAPSettings.CONFIG_FILE = config_file
            self._cparser = configparser.RawConfigParser()
            self._cparser.read(LDAPSettings.CONFIG_FILE)
            self._translate_config_file()
        else:
            # Get from settings
            self._translate_from_settings()
        self._validate()
        if self.errors or not LDAPSettings.LDAP_IMPORT_SUCCESS:
            self.enabled = False

    @staticmethod
    def requires_restart_ldap_cert_file():
        """
        Boolean stating if changing the ldap_cert file requires a restart to take effect.
        :return:
        """
        return True

    @staticmethod
    def get_ldap_cert_path():
        """
        Get path to LDAP certificate used by system.
        :return:
        """
        if LDAPSettings.LDAP_IMPORT_SUCCESS:
            return ldap.get_option(ldap.OPT_X_TLS_CACERTFILE)
        return ''

    def configs_to_strings(self):
        """
        Return configs as a dictionary with object and dictionary values exported to strings
        :return:
        """
        retval = copy(self.configs)

        # Convert AUTH_LDAP_USER_SEARCH to Json
        if 'AUTH_LDAP_USER_SEARCH' in retval:
            temp, retval['AUTH_LDAP_USER_SEARCH'] = retval['AUTH_LDAP_USER_SEARCH'], []
            try:
                for search in temp.searches:
                    retval['AUTH_LDAP_USER_SEARCH'].append({"search": search.base_dn, "filter": search.filterstr})
            except AttributeError:
                pass

        for k in LDAPSettings.JSON_FIELDS:
            if k in retval:
                retval[k] = json.dumps(retval[k])
        # Handle AUTH_LDAP_GROUP_SEARCH
        if 'AUTH_LDAP_GROUP_SEARCH' in retval:
            temp = retval['AUTH_LDAP_GROUP_SEARCH']
            try:
                retval['AUTH_LDAP_GROUP_SEARCH'] = temp.base_dn
            except AttributeError:
                pass

        # Handle AUTH_LDAP_GROUP_TYPE
        if 'AUTH_LDAP_GROUP_TYPE' in retval:
            if isinstance(retval['AUTH_LDAP_GROUP_TYPE'], GroupOfNamesType):
                retval['AUTH_LDAP_GROUP_TYPE'] = 'GroupOfNames'
            elif isinstance(retval['AUTH_LDAP_GROUP_TYPE'], PosixGroupType):
                retval['AUTH_LDAP_GROUP_TYPE'] = 'PosixGroup'
            else:
                del retval['AUTH_LDAP_GROUP_TYPE']
        # Handle AUTH_LDAP_USER_FLAGS_BY_GROUP
        if 'AUTH_LDAP_USER_FLAGS_BY_GROUP' in retval:
            flags = retval['AUTH_LDAP_USER_FLAGS_BY_GROUP']
            if "is_staff" in flags:
                retval['AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_STAFF'] = flags["is_staff"]
            if "is_superuser" in flags:
                retval['AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_SUPERUSER'] = flags["is_superuser"]
            del retval['AUTH_LDAP_USER_FLAGS_BY_GROUP']
        return retval

    def _translate_from_settings(self):
        """
        Populate self.configs from Django settings
        :return:
        """
        # Get enabled
        auths = getattr(settings, 'AUTHENTICATION_BACKENDS')
        self.enabled = True if 'django_auth_ldap.backend.LDAPBackend' in auths else False
        # Get others
        ldap_attrs = {k: v for k, v in vars(settings._wrapped).items() if 'AUTH_LDAP' in k}
        self.configs.update(ldap_attrs)

    def _translate_config_file(self):
        """
        Populate self.configs from config file
        :return:
        """
        # Translate boolean fields from cparser first
        if 'ldap' in self._cparser:
            new_configs = {}
            for k, v in self._cparser['ldap'].items():
                k = k.upper()
                if k in LDAPSettings.BOOLEAN_FIELDS:
                    new_configs[k] = self._cparser['ldap'].getboolean(k)
                else:
                    new_configs[k] = v
            self._dict_to_configs(new_configs)
        # TODO Refactor user template in ini config file to a different class/method
        if 'user template' in self._cparser:
            self.configs.update(self._cparser['user template'].items())
            if 'MULTI_USER_SUPPORT' in self.configs:
                self.configs['MULTI_USER_SUPPORT'] = self._cparser['user template'].getboolean('MULTI_USER_SUPPORT')
        return self.configs

    @staticmethod
    def is_dn(string):
        """
        Checks if string is a valid dn
        :param string:
        :return: boolean
        """
        if LDAPSettings.LDAP_IMPORT_SUCCESS:
            return ldap.dn.is_dn(string)
        return True

    def _validate(self):
        """
        Validate LDAP settings
        :return:
        """
        for k in LDAPSettings.REQUIRED_FIELDS:
            if k not in self.configs:
                self.errors[k] = 'This field is missing'
        for el in LDAPSettings.EITHER_REQ_FIELDS:
            count = 0
            for k in el:
                count += (1 if k in self.configs else 0)
            else:
                if count == 0:
                    self.errors.update({k: 'At least one field in this section must be populated' for k in el if k not in self.errors})
                elif count > 1:
                    self.errors.update({k: 'Only one field in this section may be populated' for k in el if k not in self.errors})
        for k in LDAPSettings.DN_FIELDS:
            if k in self.configs and not LDAPSettings.is_dn(self.configs[k]):
                self.errors[k] = 'This field is incorrectly formatted'
        # Check user dn template is an appropriate template string
        try:
            self.configs.get('AUTH_LDAP_USER_DN_TEMPLATE', '') % {'user': 'generic_username'}
        except ValueError:
            self.errors['AUTH_LDAP_USER_DN_TEMPLATE'] = 'This field is formatted incorrectly'
        # Verify that user attribute map is setting valid user attributes
        attr_map = self.configs.get('AUTH_LDAP_USER_ATTR_MAP', {})
        accepted_keys = {'first_name', 'last_name', 'email', 'expires'}
        extra_keys = set(attr_map.keys()) - accepted_keys
        if extra_keys:
            self.errors['AUTH_LDAP_USER_ATTR_MAP'] = 'This field is incorrect'
        # Validate if AUTH_LDAP_USER_SEARCH is correctly formatted
        if "AUTH_LDAP_USER_SEARCH" in self.configs:
            for search in self.configs["AUTH_LDAP_USER_SEARCH"].searches:
                try:
                    if not LDAPSettings.is_dn(search.base_dn):
                        self.errors['AUTH_LDAP_USER_SEARCH'] = 'This field is incorrectly formatted'
                        break
                except AttributeError:
                    self.errors['AUTH_LDAP_USER_SEARCH'] = 'This field is incorrectly formatted'

        # Validate group settings if any group settings are set
        group_keys = {k for k in self.configs.keys() if 'GROUP' in k}
        if group_keys:
            for r in LDAPSettings.REQUIRED_FOR_GROUP_FIELDS:
                if r not in group_keys or self.configs[r] is None:
                    self.errors[r] = 'This field is missing'
            if 'AUTH_LDAP_GROUP_SEARCH' in self.configs:
                try:
                    if not LDAPSettings.is_dn(self.configs['AUTH_LDAP_GROUP_SEARCH'].base_dn):
                        self.errors['AUTH_LDAP_GROUP_SEARCH'] = 'This field is incorrectly formatted'
                except AttributeError:
                    self.errors['AUTH_LDAP_GROUP_SEARCH'] = 'This field is incorrectly formatted'
        self.check_connection()

    def check_connection(self):
        """
        Check connection to LDAP server.
        Populate self.errors['AUTH_LDAP_CONNECTION_CHECK'] with an error message on failure.
        :return:
        """
        if self.errors or not self.enabled:
            return False
        server = self.configs['AUTH_LDAP_SERVER_URI']
        user = self.configs['AUTH_LDAP_BIND_DN']
        password = self.configs['AUTH_LDAP_BIND_PASSWORD']
        start_tls = self.configs.get('AUTH_LDAP_START_TLS', False)
        try:
            l = ldap.initialize(server)
            l.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
            if start_tls:
                l.start_tls_s()
            l.simple_bind_s(user, password)
            return True
        except (ldap.SERVER_DOWN, ldap.CONNECT_ERROR, ldap.TIMELIMIT_EXCEEDED, ldap.TIMEOUT):
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "Error connecting to LDAP server. LDAP client is unable to connect to LDAP server"
        except ldap.CONFIDENTIALITY_REQUIRED:
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "Error connecting to LDAP server. LDAP client is missing session confidentiality (either Start TLS or ldaps)"
        except (ldap.INVALID_CREDENTIALS, ldap.INVALID_DN_SYNTAX):
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "Error connecting to LDAP server. LDAP client is using invalid credentials"
        except ldap.LDAPError as ex:
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "Error connecting to LDAP server. LDAP client is not working. Received unexpected error: {}".format(ex)
        return False

    def update(self, new_configs):
        self.errors = {}
        old_configs = self.configs
        # Translate values to configs
        remove_configs = set(old_configs.keys()) - set(new_configs.keys())
        self._dict_to_configs(new_configs)

        # Validate configs
        self._validate()
        if self.errors:
            self.enabled = False

        # Make changes to config.ini
        self._save_to_ini()

        # Make changes to running settings
        self._apply_to_django_settings(remove_configs)

    def _dict_to_configs(self, new_configs):
        """
        Turn given dictionary into self.configs.
        Clears all previous settings.
        :param new_configs: dictionary of new configs; values should be booleans or strings
        :return:
        """
        self.configs = {}
        for k, v in new_configs.items():
            k = k.upper()
            if v == "":
                continue
            if k == 'AUTH_LDAP_ENABLED':
                self.enabled = bool(v)
            # Also treat AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_STAFF or _IS_SUPERUSER differently
            elif k == 'AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_STAFF':
                group_flags = self.configs.get('AUTH_LDAP_USER_FLAGS_BY_GROUP', {})
                group_flags['is_staff'] = v
                self.configs['AUTH_LDAP_USER_FLAGS_BY_GROUP'] = group_flags
            elif k == 'AUTH_LDAP_USER_FLAGS_BY_GROUP_IS_SUPERUSER':
                group_flags = self.configs.get('AUTH_LDAP_USER_FLAGS_BY_GROUP', {})
                group_flags['is_superuser'] = v
                self.configs['AUTH_LDAP_USER_FLAGS_BY_GROUP'] = group_flags
            # AUTH_LDAP_GROUP_MAPPING and AUTH_LDAP_USER_ATTR_MAP should be imported as json
            elif k in LDAPSettings.JSON_FIELDS:
                try:
                    self.configs[k] = json.loads(v)
                except json.JSONDecodeError:
                    self.errors[k] = 'This field is not in json form'
            else:
                self.configs[k] = v
        if LDAPSettings.LDAP_IMPORT_SUCCESS:
            # Import AUTH_LDAP_USER_SEARCH as LDAPSearchUnion

            if "AUTH_LDAP_USER_SEARCH" in self.configs:
                temp = self.configs["AUTH_LDAP_USER_SEARCH"]
                ldap_searches = []
                for el in temp:
                    ldap_searches.append(LDAPSearch(
                        el["search"],
                        ldap.SCOPE_SUBTREE,
                        el["filter"]
                    ))
                self.configs["AUTH_LDAP_USER_SEARCH"] = LDAPSearchUnion(*ldap_searches)

            # Import AUTH_LDAP_GROUP_SEARCH as LDAPSearch
            temp = new_configs.get('AUTH_LDAP_GROUP_TYPE', '').lower()
            group_type = None
            if temp == 'groupofnames':
                group_type = 'groupOfNames'
            elif temp == 'posixgroup':
                group_type = 'posixGroup'
            group_search_dn = new_configs.get('AUTH_LDAP_GROUP_SEARCH', None)
            if group_search_dn and group_type:
                self.configs['AUTH_LDAP_GROUP_SEARCH'] = LDAPSearch(
                    group_search_dn,
                    ldap.SCOPE_SUBTREE,
                    "(objectClass={})".format(group_type)
                )
            # import AUTH_LDAP_GROUP_TYPE and AUTH_LDAP_GROUP_TYPE_NAME_ATTR as object
            name_attr = new_configs.get('AUTH_LDAP_GROUP_TYPE_NAME_ATTR', None)
            if group_type == 'groupOfNames':
                self.configs['AUTH_LDAP_GROUP_TYPE'] = GroupOfNamesType() \
                    if name_attr is None else GroupOfNamesType(name_attr=name_attr)
            elif group_type == 'posixGroup':
                self.configs['AUTH_LDAP_GROUP_TYPE'] = PosixGroupType() \
                    if name_attr is None else PosixGroupType(name_attr=name_attr)
            else:
                if 'AUTH_LDAP_GROUP_TYPE' in self.configs:
                    del self.configs['AUTH_LDAP_GROUP_TYPE']

    def _save_to_ini(self):
        """
        Save configs to config file.
        :return:
        """
        conf = configparser.RawConfigParser()
        conf.read(LDAPSettings.CONFIG_FILE)
        if 'ldap' in conf:
            del conf['ldap']
        conf.add_section('ldap')
        to_write = self.configs_to_strings()
        if 'AUTH_LDAP_ENABLED' not in to_write:
            to_write['AUTH_LDAP_ENABLED'] = str(int(self.enabled))
        for k, v in to_write.items():
            conf['ldap'][k] = v
        with open(LDAPSettings.CONFIG_FILE, 'w') as fd:
            conf.write(fd)

    def _apply_to_django_settings(self, remove_configs):
        """
        Apply current configs to django settings.
        :param remove_configs: A list of configs to remove from django settings
        :return:
        """
        for r in remove_configs:
            delattr(settings, r)
        if self.enabled and not self.errors:
            for k, v in self.configs.items():
                setattr(settings, k, v)
            # Add to authentication backends
            if 'django_auth_ldap.backend.LDAPBackend' not in settings.AUTHENTICATION_BACKENDS:
                settings.AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS \
                                                   + ('django_auth_ldap.backend.LDAPBackend',)
        else:
            # Remove from authentication backends
            if 'django_auth_ldap.backend.LDAPBackend' in settings.AUTHENTICATION_BACKENDS:
                settings.AUTHENTICATION_BACKENDS = tuple(x for x in settings.AUTHENTICATION_BACKENDS
                                                         if x != 'django_auth_ldap.backend.LDAPBackend')

class EMAILSettings:
    CONFIG_FILE = 'config.ini'
    REQUIRED_FIELDS = [
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_USE_TLS',
        'DEFAULT_FROM_EMAIL',
    ]
    BOOLEAN_FIELDS = [
        'EMAIL_USE_TLS',
    ]
    
    def __init__(self, config_file=None):
        self.configs = {}
        if config_file:
            # Get from config file
            EMAILSettings.CONFIG_FILE = config_file
            self._cparser = configparser.RawConfigParser()
            self._cparser.read(EMAILSettings.CONFIG_FILE)
            self._translate_config_file()
        else:
            # Get from settings
            self._translate_from_settings()
    
    def _translate_config_file(self):
        """
        Populate self.configs from config file
        :return:
        """
        # Translate boolean fields from cparser first
        self.configs = {}
        if 'email' in self._cparser:
            self.configs = {}
            for k, v in self._cparser['email'].items():
                k = k.upper()
                if k in EMAILSettings.BOOLEAN_FIELDS:
                    self.configs[k] = self._cparser['email'].getboolean(k)
                else:
                    self.configs[k] = v
        return self.configs
    
    def _translate_from_settings(self):
        """
        Populate self.configs from Django settings
        :return:
        """
        email_attrs = {k: v for k, v in vars(settings._wrapped).items() if 'EMAIL' in k}
        self.configs.update(email_attrs)
    
    def update(self, new_configs):
        old_configs = self.configs
        # Translate values to configs
        remove_configs = set(old_configs.keys()) - set(new_configs.keys())
        self.configs = {}
        for k, v in new_configs.items():
            k = k.upper()
            if k in EMAILSettings.BOOLEAN_FIELDS:
                self.configs[k] = bool(v)
            else:
                self.configs[k] = v

        # Make changes to config.ini
        self._save_to_ini()

        # Make changes to running settings
        self._apply_to_django_settings(remove_configs)
    
    def _save_to_ini(self):
        """
        Save configs to config file.
        :return:
        """
        conf = configparser.RawConfigParser()
        conf.read(EMAILSettings.CONFIG_FILE)
        if 'email' in conf:
            del conf['email']
        conf.add_section('email')
        to_write = self.configs
        for k, v in to_write.items():
            if 'EMAIL_USE_TLS' in k:
                conf['email'][k] = str(int(v))
            else:
                conf['email'][k] = v
        with open(EMAILSettings.CONFIG_FILE, 'w') as fd:
            conf.write(fd)
    
    def _apply_to_django_settings(self, remove_configs):
        """
        Apply current configs to django settings.
        :param remove_configs: A list of configs to remove from django settings
        :return:
        """
        for r in remove_configs:
            delattr(settings, r)
        for k, v in self.configs.items():
            setattr(settings, k, v)
        # Add to email backends
        setattr(settings, "EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')

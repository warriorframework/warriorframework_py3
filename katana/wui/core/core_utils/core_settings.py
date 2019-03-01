import logging

from django.conf import settings
import configparser
from copy import copy
import json
import os
import time
import threading
from utils.navigator_util import Navigator
import sys
try:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
except Exception:
    pass
logger = logging.getLogger(__name__)


class Restart:

    def __init__(self):
        self.settings_file = os.path.join(Navigator().get_katana_dir(), 'wui', 'settings.py')
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
        'AUTH_LDAP_USER_DN_TEMPLATE',
        'AUTH_LDAP_SEARCH_BASE_DN',
        'AUTH_LDAP_BIND_DN',
        'AUTH_LDAP_BIND_PASSWORD',
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
        self.errors = {}
        for k in LDAPSettings.REQUIRED_FIELDS:
            if k not in self.configs:
                self.errors[k] = 'missing'
        for k in LDAPSettings.DN_FIELDS:
            if k in self.configs and not LDAPSettings.is_dn(self.configs[k]):
                self.errors[k] = 'incorrectly formatted'
        # Check user dn template is an appropriate template string
        try:
            self.configs.get('AUTH_LDAP_USER_DN_TEMPLATE', '') % {'user': 'generic_username'}
        except ValueError:
            self.errors['AUTH_LDAP_USER_DN_TEMPLATE'] = 'formatted incorrectly'
        # Verify that user attribute map is setting valid user attributes
        attr_map = self.configs.get('AUTH_LDAP_USER_ATTR_MAP', {})
        accepted_keys = {'first_name', 'last_name', 'email', 'expires'}
        extra_keys = set(attr_map.keys()) - accepted_keys
        if extra_keys:
            self.errors['AUTH_LDAP_USER_ATTR_MAP'] = 'incorrect'
        # Validate group settings if any group settings are set
        group_keys = {k for k in self.configs.keys() if 'GROUP' in k}
        if group_keys:
            for r in LDAPSettings.REQUIRED_FOR_GROUP_FIELDS:
                if r not in group_keys or self.configs[r] is None:
                    self.errors[r] = 'missing'
            if 'AUTH_LDAP_GROUP_SEARCH' in self.configs:
                try:
                    if not LDAPSettings.is_dn(self.configs['AUTH_LDAP_GROUP_SEARCH'].base_dn):
                        self.errors['AUTH_LDAP_GROUP_SEARCH'] = 'incorrectly formatted'
                except AttributeError:
                    self.errors['AUTH_LDAP_GROUP_SEARCH'] = 'incorrectly formatted'
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
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "unable to connect to LDAP server"
        except ldap.CONFIDENTIALITY_REQUIRED:
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "missing session confidentiality (either Start TLS or ldaps)"
        except (ldap.INVALID_CREDENTIALS, ldap.INVALID_DN_SYNTAX):
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "using invalid credentials"
        except ldap.LDAPError as ex:
            self.errors['AUTH_LDAP_CONNECTION_CHECK'] = "not working. Received unexpected error: {}".format(ex)
        return False

    def update(self, new_configs):
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
            elif k == 'AUTH_LDAP_USER_ATTR_MAP' or k == 'AUTH_LDAP_GROUP_MAPPING':
                try:
                    self.configs[k] = json.loads(v)
                except json.JSONDecodeError:
                    self.errors[k] = 'not in json form'
            else:
                self.configs[k] = v
        if LDAPSettings.LDAP_IMPORT_SUCCESS:
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


class KibanaSettings(object):

    def __init__(self):
        """
        kibana_url = Initializes the kibana information file
        data = contains information stored in the file
        fields = keys that are present in the file
        """
        self.kibana_url_file = os.path.join(Navigator().get_katana_dir(), 'wui', 'core', '.data', 'kibana.json')
        self.lock = threading.Lock()
        self.data = self.get_data()
        self.fields = {"url": self._validate_url}
        self.errors = ""

    def get_data(self):
        """
        Reads data from the Kibana file
        :return: data in JSON format
        """
        data = {}
        self.lock.acquire()
        try:
            with open(self.kibana_url_file, 'r') as f:
                data = json.load(f)
        except (IOError, Exception) as e:
            self.errors = "Katana Log: Unable to read Kibana data. Exception: {0}".format(e)
            logger.exception(self.errors)
        finally:
            self.lock.release()
        return data

    def get_url(self):
        """
        :return: the kibana url, False if not set
        """
        return self.data.get("url", False)

    def update_data(self, data):
        """
        :param data: contains data to be updates
        """
        try:
            for k, v in data.items():
                _k = k.lower()
                if _k in self.fields:
                    self.data[_k] = self.fields[_k](v)
            self.lock.acquire()
            with open(self.kibana_url_file, 'w') as f:
                f.write(json.dumps(self.data))
        except (AttributeError, IOError, Exception) as e:
            self.errors = "Katana Log: Unable to save Kibana data. Exception: {0}".format(e)
            logger.exception(self.errors)
        else:
            logger.info("Katana Log: Updated Kibana data successfully.")
        finally:
            self.lock.release()

    def _validate_url(self, url):
        """
        :param url: URL to be validated
        :return: Validated URL
        """
        return url

from django.conf import settings
import configparser
import json
import sys
try:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
except Exception:
    pass


class LDAPSettings():
    CONFIG_FILE = 'config.ini'
    LDAP_IMPORT_SUCCESS = 'django_auth_ldap' in sys.modules

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
        if 'ldap' in self._cparser:
            for k, v in self._cparser['ldap'].items():
                k = k.upper()
                if k == 'AUTH_LDAP_ENABLED':
                    self.enabled = self._cparser['ldap'].getboolean(k)
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
                group_type = self._cparser['ldap'].get('AUTH_LDAP_GROUP_TYPE', 'groupOfNames').lower()
                group_type = 'groupOfNames' if group_type == 'groupofnames' else 'posixGroup'
                if 'AUTH_LDAP_GROUP_SEARCH' in self._cparser['ldap']:
                    self.configs['AUTH_LDAP_GROUP_SEARCH'] = LDAPSearch(
                        self._cparser['ldap']['AUTH_LDAP_GROUP_SEARCH'],
                        ldap.SCOPE_SUBTREE,
                        "(objectClass={})".format(group_type)
                    )
                # import AUTH_LDAP_GROUP_TYPE and AUTH_LDAP_GROUP_TYPE_NAME_ATTR as object
                name_attr = self._cparser['ldap'].get('AUTH_LDAP_GROUP_TYPE_NAME_ATTR', None)
                if group_type == 'groupOfNames':
                    self.configs['AUTH_LDAP_GROUP_TYPE'] = GroupOfNamesType() \
                        if name_attr is None else GroupOfNamesType(name_attr=name_attr)
                elif group_type == 'posixGroup':
                    self.configs['AUTH_LDAP_GROUP_TYPE'] = PosixGroupType() \
                        if name_attr is None else PosixGroupType(name_attr=name_attr)
        if 'user template' in self._cparser:
            self.configs.update(self._cparser['user template'].items())
            if 'MULTI_USER_SUPPORT' in self.configs:
                self.configs['MULTI_USER_SUPPORT'] = self._cparser['user template'].getboolean('MULTI_USER_SUPPORT')
        return self.configs

    def _validate(self):
        """
        Validate LDAP settings
        :return:
        """
        self.errors = {}
        # Return early (nothing wrong) if LDAP is disabled
        if not self.enabled:
            return
        # Check for required values
        required = [
            'AUTH_LDAP_SERVER_URI',
            'AUTH_LDAP_USER_DN_TEMPLATE',
            'AUTH_LDAP_SEARCH_BASE_DN',
            'AUTH_LDAP_BIND_DN',
            'AUTH_LDAP_BIND_PASSWORD',
        ]
        for k in required:
            if k not in self.configs:
                self.errors[k] = 'missing'
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
            required = [
                'AUTH_LDAP_GROUP_TYPE',
                'AUTH_LDAP_GROUP_SEARCH'
            ]
            for r in required:
                if r not in group_keys:
                    self.errors[r] = 'missing'


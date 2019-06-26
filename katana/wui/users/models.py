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

import logging
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from django.db import models
from django.utils import timezone

# Public  Constants
GROUP_WARRIOR_USERS = 'Warrior Users'  # Name for Warrior Users Group

# Private Constants
_LOGGER = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Custom Warrior User Class.

    Customizations include:
    * Addition of 'expires' field and expired() method.
    * Adds user to a group named Warrior Users (name accessible through the GROUP_WARRIOR_USERS global) on creation.
    * Adds user to groups imported from LDAP mapped using the setting AUTH_LDAP_GROUP_MAPPING.
        * AUTH_LDAP_GROUP_MAPPING is a dictionary with entries of the form "LDAP group DN" : "Group Name".
    """
    # Add custom user fields here
    expires = models.DateTimeField(verbose_name="User Expiry Date", null=True, blank=True)

    def expired(self):
        """
        Checks user expiry against current server time.
        :return: True/False
        """
        expires = self.expires
        now = timezone.now()
        if expires and expires < now:
            self.active = False
            self.save()
            return True
        return False

    def save(self, *args, **kwargs):
        """
        Over-ridden save method for Warrior User.
        Adds saved user to GROUP_WARRIOR_USERS on creation.
        Adds saved user to mapped groups from LDAP using the setting AUTH_LDAP_GROUP_MAPPING,
        assuming django-auth-ldap is also setup correctly.
        :param args: Same as AbstractUser args
        :param kwargs: Same as AbstractUser kwargs
        :return: Same as AbstractUser
        """
        created = False
        if not self.pk:
            created = True

        super(AbstractUser, self).save()

        # Add to Warrior Users group on creation
        if created:
            try:
                group, x = Group.objects.get_or_create(name=GROUP_WARRIOR_USERS)
                self.groups.add(group)
            except Exception as ex:
                _LOGGER.error("Failed to add {} to group {}".format(self.username, GROUP_WARRIOR_USERS))
                _LOGGER.debug("Exception thrown while adding group {} to user {}\n{}".format(GROUP_WARRIOR_USERS, self.username, ex))
        # Map LDAP roles if applicable
        if hasattr(settings, "AUTH_LDAP_GROUP_MAPPING") and hasattr(self, 'ldap_user'):
            try:
                mapping = getattr(settings, "AUTH_LDAP_GROUP_MAPPING", {})
                for ldap, django in mapping.items():
                    if ldap in self.ldap_user.group_dns:
                        group, x = Group.objects.get_or_create(name=django)
                        self.groups.add(group)
            except Exception as ex:
                _LOGGER.error("Failed to add {} to groups based on LDAP mapping".format(self.username))
                _LOGGER.debug("Exception thrown while adding LDAP-mapped groups to user {}\n{}".format(self.username, ex))

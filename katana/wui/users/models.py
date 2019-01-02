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
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Public  Constants
GROUP_WARRIOR_USERS = 'Warrior Users'  # Name for Warrior Users Group
BACKGROUND_USER_EXPIRY_CHECK = 60  # Seconds

# Private Constants
_LOGGER = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Custom Warrior User Class
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
            return True
        return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Add all created users to the base Warrior Users Group
    :return:
    """
    if created:
        try:
            instance.groups.add(Group.objects.get(name=GROUP_WARRIOR_USERS))
        except Exception as ex:
            Group.objects.get_or_create(name=GROUP_WARRIOR_USERS)
            instance.groups.add(Group.objects.get(name=GROUP_WARRIOR_USERS))

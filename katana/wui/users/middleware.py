"""
Defines custom middleware for users and user management.
"""
import re
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .views import PublicView


class UserExpiryMiddleware(object):
    """
    Django Middleware to check for user expiry.
    Does not apply to django rest framework requests.
    See rest_addons for django rest framework support.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_anonymous and request.user.expired():
            context = {
                'title': 'Error: Unauthorized',
                'message': 'User {} is expired.'.format(request.user.username),
            }
            logout(request)
            return render(request, 'core/base_error.html', context=context, status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class LoginRequiredMiddleware(object):
    """
    Middleware that makes all views require a login.

    To exempt a view from requiring a login, use @login_not_required or use the PublicView class.
    Another method is to add PUBLIC_VIEWS or PUBLIC_PATHS to the settings to set
    specific views or paths as public.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.public_patterns = []
        self.public_views = []
        if hasattr(settings, 'PUBLIC_VIEWS'):
            for view_path in settings.PUBLIC_VIEWS:
                view = self.get_view(view_path)
                self.public_views.append(view)
        if hasattr(settings, 'PUBLIC_PATHS'):
            for public_path in settings.PUBLIC_PATHS:
                self.public_patterns.append(re.compile(public_path))

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def get_view(self, view_path):
        i = view_path.rfind('.')
        module_path, view_name = view_path[:i], view_path[i + 1:]
        module = __import__(module_path, globals(), locals(), [view_name])
        return getattr(module, view_name)

    def matches_public_view(self, view):
        if self.public_views:
            for public_view in self.public_views:
                if view == public_view:
                    return True
        return False

    def matches_public_path(self, path):
        if self.public_patterns:
            for pattern in self.public_patterns:
                if pattern.match(path) is not None:
                    return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated \
                or (hasattr(view_func, 'view_class') and issubclass(view_func.view_class, (APIView,))) \
                or (isinstance(view_func, PublicView)) \
                or (hasattr(view_func, 'view_class') and issubclass(view_func.view_class, PublicView)) \
                or self.matches_public_path(request.path) \
                or self.matches_public_view(view_func):
            return None
        else:
            return login_required(view_func)(request, *view_args, **view_kwargs)

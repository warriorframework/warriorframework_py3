"""
Defines custom middleware for users.
"""
from django.http import HttpResponseForbidden


class UserExpiryMiddleware(object):
    """
    Django Middleware to check for user expiry.
    Does not apply to django rest framework requests
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_anonymous and request.user.expired():
            return HttpResponseForbidden()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

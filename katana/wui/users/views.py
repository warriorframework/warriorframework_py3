from functools import update_wrapper


class PublicView(object):
    """
    Forces a view to be public (no login required).
    Use in place of Django's View class to create a public class-based view.
    """
    login_required = False

    def __init__(self, view_func):
        self.view_func = view_func
        update_wrapper(self, view_func)

    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return PublicView(view_func)

    def __call__(self, request, *args, **kwargs):
        return self.view_func(request, *args, **kwargs)
from .views import PublicView


def login_not_required(view_func):
    """
    Decorator which marks the given view as public (no login required).
    """
    return PublicView(view_func)

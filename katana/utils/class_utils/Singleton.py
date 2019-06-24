import functools
import threading


def _synchronized(lock):
    """
    Synchronization decorator - see https://stackoverflow.com/a/50567397
    :param lock:
    :return:
    """

    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kw):
            with lock:
                return f(*args, **dict(kw))

        return inner_wrapper

    return wrapper


# Lock for creating thread-safe Singleton Class
_lock = threading.Lock()


# Singleton Pattern MetaClass
class Singleton(type):
    """
    Singleton pattern used so that only one class truly exists at any given time for a declared Singleton class
    Singleton pattern recommended by https://stackoverflow.com/a/6798042
    """
    _instances = {}

    @_synchronized(_lock)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
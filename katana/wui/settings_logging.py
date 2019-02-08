import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False


def get_log_config():
    """ Return logging dictionary config"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
        },
        "formatters": {
            "standard": {
                "format": "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
            },
            "verbose": {
                "format": "%(asctime)s\t%(levelname)s\t%(name)s\t%(pathname)s\t%(process)d\t%(thread)d\t%(message)s"
            },
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
            },
            "console": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "root_file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs", "katana.log"),
                "maxBytes": 10242880,
                "backupCount": 10,
                "formatter": "verbose",
            },
            "django_file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs", "katana.django.log"),
                "maxBytes": 10242880,
                "backupCount": 10,
                "formatter": "standard",
            },
        },
        "root": {
            "handlers": ["root_file", "mail_admins", "console"],
            "level": "DEBUG" if DEBUG else "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["django_file", "mail_admins", "console"],
                "level": "DEBUG" if DEBUG else "INFO",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["django_file", "mail_admins", "console"],
                "level": "WARNING",
                "propagate": False,
            },
        }
    }

#!/usr/bin/env python
import os
import sys
from os.path import abspath, dirname

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "katana.wui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    try:
        import katana
        os.environ["pipmode"]= "True"
    #except ModuleNotFoundError as error:
    except:
        WARRIORDIR = dirname(dirname(abspath(__file__)))
        sys.path.append(WARRIORDIR)
        try:
            import katana
            os.environ["pipmode"]= "False"
        except:
            raise
    execute_from_command_line(sys.argv)

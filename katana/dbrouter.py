import os
try:
    import katana

    os.environ["pipmode"] = "True"
# except ModuleNotFoundError as error:
except:
    WARRIORDIR = dirname(dirname(abspath(__file__)))
    sys.path.append(WARRIORDIR)
    try:
        import katana

        os.environ["pipmode"] = "False"
    except:
        raise
from katana.utils.navigator_util import Navigator
from katana.utils.json_utils import read_json_data


def read_config_file_data():
        """this function reads the data from appconfig.json file"""
        config_file_path = os.path.join(
            nav_obj.get_katana_dir(), "katana_configs", "app_config.json")
        data = read_json_data(config_file_path)
        return data

nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()
app_config_file = os.path.join(BASE_DIR, "katana_configs", "app_config.json")
app_config_data = read_config_file_data()


class DbRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model=None, **hints):
        """
        Attempts to read equinix models go to equinix database.
        """
        if model is not None:
            if len(app_config_data["apps_rely_on_postgresdb"]) > 0:
                if model._meta.app_label in app_config_data["apps_rely_on_postgresdb"]:
                    return 'postgresql'
        return None

    def db_for_write(self, model=None, **hints):
        """
        Attempts to write equinix models go to the equinix database.
        """
        if model is not None:
            if len(app_config_data["apps_rely_on_postgresdb"]) > 0:
                if model._meta.app_label in app_config_data["apps_rely_on_postgresdb"]:
                    return 'postgresql'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
        if len(app_config_data["apps_rely_on_postgresdb"]) > 0:
            if obj1._meta.app_label in app_config_data["apps_rely_on_postgresdb"] or \
            obj2._meta.app_label in app_config_data["apps_rely_on_postgresdb"]:
                return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Do not allow migrations on the equinix database
        """
        if model is not None:
            if len(app_config_data["apps_rely_on_postgresdb"]) > 0:
                if model._meta.app_label in app_config_data["apps_rely_on_postgresdb"]:
                    return "postgresql"
        return "default"

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
            if model._meta.app_label == 'equinix':
                return 'equinix'
        return 'default'

    def db_for_write(self, model=None, **hints):
        """
        Attempts to write equinix models go to the equinix database.
        """
        if model is not None:
            if model._meta.app_label == 'equinix':
                return 'equinix'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Do not allow relations involving the equinix database
        """
        if obj1._meta.app_label == 'equinix' or \
           obj2._meta.app_label == 'equinix':
           return False
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Do not allow migrations on the equinix database
        """
        if model is not None:
            if model._meta.app_label == 'equinix':
                return True
        return True

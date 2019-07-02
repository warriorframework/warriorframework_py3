from utils.class_utils import Singleton
from abc import ABCMeta, abstractmethod
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail


class WarriorMessagingBaseClass(metaclass=ABCMeta):

    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_mass_message(self, *args, **kwargs):
        pass

    @abstractmethod
    def message_admins(self, *args, **kwargs):
        pass

    @abstractmethod
    def message_managers(self, *args, **kwargs):
        pass


class WarriorLiveConnectionClass(metaclass=ABCMeta):

    @abstractmethod
    def get_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def open_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def close_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def open_all_connections(self, *args, **kwargs):
        pass

    @abstractmethod
    def close_all_connections(self, *args, **kwargs):
        pass


class WarriorMailManager(WarriorMessagingBaseClass):

    def __init__(self, server_email="root@localhost", *args, **kwargs):
        self.server_email = server_email
        self.connections_class = WarriorMailLiveConnectionsClass()

    def send_message(self, connection_name, subject="", message="", from_email=None, to=None, cc=None, bcc=None,
                     fail_silently=False, connection=None, attachments=None, headers=None, reply_to=None, html_message=False):
        """
        Warrior wrapper for the Email class in Django Mail.

        :param connection_name: Name of the connection to be used. Set in WarriorMailLiveConnectionsClass()
        Complete Documentation: https://docs.djangoproject.com/en/2.2/topics/email/#emailmessage-objects

        :return: None
        """
        email_message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to, bcc=bcc,
                                     connection=self.connections_class.get_connection(connection_name),
                                     attachments=attachments, headers=headers, cc=cc, reply_to=None)
        email_message.send(fail_silently=fail_silently)

    def send_mass_message(self, connection_name, datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
        current_conn = self.connections_class.get_connection(connection_name)

    def message_admins(self, connection_name, subject, message, fail_silently=False, connection=None, html_message=None):
        current_conn = self.connections_class.get_connection(connection_name)

    def message_managers(self, connection_name, subject, message, fail_silently=False, connection=None, html_message=None):
        current_conn = self.connections_class.get_connection(connection_name)


class WarriorMailLiveConnectionsClass(WarriorLiveConnectionClass, metaclass=Singleton):

    def __init__(self, list_of_conns=None, *args, **kwargs):
        self.all_connections = {"default":
            {
                "details": {
                    "host": None,
                    "port": None,
                    "username": None,
                    "password": None,
                    "use_tls": None,
                    "fail_silently": False,
                    "use_ssl": None,
                    "timeout": None,
                    "ssl_keyfile": None,
                    "ssl_certfile": None,
                },
                "conn_object": None
            }
        }
        if list_of_conns:
            for conn in list_of_conns:
                # add connections here
                pass
            self.open_all_connections()

    def get_connection(self, connection_name):
        if connection_name in self.all_connections:
            conn = self.all_connections[connection_name]
        else:
            print("Email Connection: {0} not found. Reverting to default connection.".format(connection_name))
            conn = self.all_connections["default"]
        return conn["conn_object"]

    def add_connection(self, connection_name, host=None, port=None, username=None, password=None, use_tls=None,
                       fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None,
                       subject_prefix=None, use_localtime=True):
        pass

    def open_connection(self, connection_name):
        pass

    def close_connection(self, connection_name):
        pass

    def open_all_connections(self):
        pass

    def close_all_connections(self):
        pass

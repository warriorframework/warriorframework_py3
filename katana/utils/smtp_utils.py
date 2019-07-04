from utils.class_utils import Singleton
from abc import ABCMeta, abstractmethod
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail, get_connection


class WarriorMessagingBaseClass(metaclass=ABCMeta):

    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_html_message(self, *args, **kwargs):
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

    def send_message(self, connection_name, subject="", message="", from_email=None, to=None,
                     cc=None, bcc=None, fail_silently=False, connection=None, attachments=None,
                     headers=None, reply_to=None):
        """
        Warrior wrapper for the Email class in Django Mail.

        :param connection_name: Name of the connection to be used. Set in WarriorMailLiveConnectionsClass()
        Complete Documentation: https://docs.djangoproject.com/en/2.2/topics/email/#emailmessage-objects

        :return: None
        """
        current_conn = self.connections_class.get_connection(connection_name)
        if current_conn:
            email_message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to, bcc=bcc,
                                         connection=current_conn, attachments=attachments,
                                         headers=headers, cc=cc, reply_to=None)
            email_message.send(fail_silently=fail_silently)

    def send_html_message(self, connection_name, subject="", message="", from_email=None, to=None, cc=None, bcc=None,
                          fail_silently=False, connection=None, attachments=None, headers=None, reply_to=None):
        """
        Warrior wrapper for the Email class in Django Mail.

        :param connection_name: Name of the connection to be used. Set in WarriorMailLiveConnectionsClass()
        Complete Documentation: https://docs.djangoproject.com/en/2.2/topics/email/#emailmessage-objects

        :return: None
        """
        current_conn = self.connections_class.get_connection(connection_name)
        if current_conn:
            email_message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to, bcc=bcc,
                                         connection=current_conn, attachments=attachments,
                                         headers=headers, cc=cc, reply_to=None)
            email_message.send(fail_silently=fail_silently)

    def send_mass_message(self, connection_name, datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
        current_conn = self.connections_class.get_connection(connection_name)

    def message_admins(self, connection_name, subject, message, fail_silently=False, connection=None, html_message=None):
        current_conn = self.connections_class.get_connection(connection_name)

    def message_managers(self, connection_name, subject, message, fail_silently=False, connection=None, html_message=None):
        current_conn = self.connections_class.get_connection(connection_name)


class WarriorMailLiveConnectionsClass(WarriorLiveConnectionClass, metaclass=Singleton):

    def __init__(self, *args, **kwargs):
        self.all_connections = {}
        self._read_email_server_file()
        for conn_name, conn_details in self.all_connections.items():
            self.add_connection(conn_name, new_connection=False)
        self.open_all_connections()

    def get_connection(self, connection_name):
        if connection_name in self.all_connections:
            conn = self.all_connections[connection_name]
            return conn["conn_object"]
        print("Email Connection: {0} not found. Email will not be sent.".format(connection_name))
        return None

    def _read_email_server_file(self):
        """
        Expected JSON format in the file is:
        {
         "default": {
            "details": {
                "host": null,
                "port": null,
                "username": null,
                "password": null,
                "use_tls": null,
                "fail_silently": null,
                "use_ssl": null,
                "timeout": null,
                "ssl_keyfile": null,
                "ssl_certfile": null
            },
            "conn_object": null
          }
        }
        :return:
        """
        pass

    def add_connection(self, connection_name, host=None, port=None, username=None, password=None, use_tls=None,
                       fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None,
                       subject_prefix=None, use_localtime=True, new_connection=True):
        if new_connection:
            self.all_connections[connection_name] = {"details": {
                    "host": host,
                    "port": port,
                    "username": username,
                    "password": password,
                    "use_tls":  use_tls,
                    "fail_silently": fail_silently,
                    "use_ssl": use_ssl,
                    "timeout": timeout,
                    "ssl_keyfile": ssl_keyfile,
                    "ssl_certfile": ssl_certfile,
                    "subject_prefix": subject_prefix,
                    "use_localtime": use_localtime
                },
                "conn_object": get_connection(host=None, port=None, username=None, password=None, use_tls=None,
                                              fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None,
                                              ssl_certfile=None, subject_prefix=None, use_localtime=True)
            }
        elif connection_name in self.all_connections:
            self.all_connections[connection_name]["conn_object"] = get_connection(**self.all_connections[connection_name])
        else:
            print("Could not find connection with the name: {0}".format(connection_name))

    def open_connection(self, connection_name):
        pass

    def close_connection(self, connection_name):
        pass

    def open_all_connections(self):
        pass

    def close_all_connections(self):
        pass

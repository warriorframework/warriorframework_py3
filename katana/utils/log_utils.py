"""
Module for logging utilities.

Does NOT provide:
    * Getting logger
        * Loggers should be retrieved using logging.getLogger(__name__)

Does provide:
    * Formatting Django request into a message string
"""
import logging
import json


def format_request_msg(request):
    """
    Formats Django request object attributes into a message string.
    :param request: Django Request object
    :return: formatted string
        e.g. request={"method": "GET", "path": "/katana/test/", "username": "admin"}
    """
    data = {
        "username": request.user.username if request.user and request.user.username else "",
        "path": request.path,
        "method": request.method,
    }
    msg = "request={}".format(json.dumps(data, sort_keys=True))
    return msg

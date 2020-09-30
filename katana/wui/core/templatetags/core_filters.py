from django import template
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
import os


nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()

register = template.Library()


@register.filter(name='get_app_name', is_safe=True)
def get_app_name(value):
    fname_file = os.path.join(BASE_DIR, "wui/core/static/core/framework_name.json")
    data = read_json_data(fname_file)
    appname = data["fr_name"]
    return appname

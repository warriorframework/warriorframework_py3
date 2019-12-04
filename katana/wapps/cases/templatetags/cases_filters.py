import collections
from django import template
from katana.wapps.cases.cases_utils.defaults import inverted_on_errors, inverted_contexts, \
    inverted_impacts, inverted_runmodes, inverted_iteration_types

register = template.Library()


@register.filter(name='convert_runmodes')
def convert_runmodes(value):
    return inverted_runmodes()[value.strip().lower()]


@register.filter(name='convert_on_errors')
def convert_on_errors(value):
    return inverted_on_errors()[value.strip().lower()]


@register.filter(name='convert_iteration_types')
def convert_iteration_types(value):
    return inverted_iteration_types()[value.strip().lower()]


@register.filter(name='convert_contexts')
def convert_contexts(value):
    return inverted_contexts()[value.strip().lower()]


@register.filter(name='convert_impacts')
def convert_impacts(value):
    return inverted_impacts()[value.strip().lower()]


@register.filter(name='get_attribute')
def get_attribute(value, attribute_name):
    return value["@" + attribute_name]

@register.filter(name='get_attribute_new')
def get_attribute_new(value):
    if type(value) == list :
        return "list"
    elif type(value) ==  None:
        pass
    elif type(value) == collections.OrderedDict:
        return "str"

@register.filter(name='get_attribute_repo')
def get_attribute_repo(value):

    sorted_fruit_list = list(value.keys())
    if "@Repo" in sorted_fruit_list:
        return "norm"
    else:
        return "empty"


@register.filter(name='check_value_is_available_or_not')
def check_value_is_available_or_not(value):
    if type(value) == list :
        return "list"
    elif type(value) == None:
        pass
    elif type(value) == collections.OrderedDict:
        for i in value:
            if "value" in i :
                return "str"
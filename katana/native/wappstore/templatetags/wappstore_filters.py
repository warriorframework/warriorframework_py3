from django import template


register = template.Library()


@register.filter(name='convert_to_fa_four')
def convert_to_fa_four(value):
    conversion = {"pencil-alt": "pencil",
                  "tachometer-alt": "tachometer",
                  "exchange-alt": "exchange",
                  "sync": "refresh",
                  "globe-americas": "globe"}
    return value if value not in conversion else conversion[value]
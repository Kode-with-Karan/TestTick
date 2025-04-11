from django import template
import json

register = template.Library()

@register.filter
def pluck(queryset, attr):
    values = []
    for obj in queryset:
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            values.append(str(val))
        elif callable(getattr(obj, attr, None)):
            val = getattr(obj, attr)()
            values.append(val)
    return json.dumps(values)

from django import template
from numpy import interp

register = template.Library()

@register.simple_tag
def map_opacity(to_map):
    return str(round(interp(to_map,[1,20],[1,0]),2))

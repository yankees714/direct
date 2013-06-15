from django import template
from numpy import interp

register = template.Library()

@register.simple_tag
def map_opacity(to_map):
    style='style="opacity:' + str(interp(to_map,[1,20],[1,0])) + '"'
    return style

from django import template
from numpy import interp

register = template.Library()

@register.simple_tag
def map_opacity(to_map):
    return str(round(interp(to_map,[1,30],[1,0]),2))

@register.simple_tag
def direct():
    return "<span class='direct'>direct</span>"

@register.simple_tag
def static_head():
    head = "\n".join([
        '<title>direct</title>',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="robots" content="index, nofollow">',

        '<link rel="apple-touch-icon" href="{{ STATIC_URL }}img/favicon.png"/>',
        '<link rel="icon" href="{{ STATIC_URL }}img/favicon.png"/>',
        '<!--[if IE]><link rel="shortcut icon" href="{{ STATIC_URL }}img/favicon.ico"><![endif]-->',

        '<link href="http://fonts.googleapis.com/css?family=Lato:300,400,700" rel="stylesheet" type="text/css">',
    ])
    return head
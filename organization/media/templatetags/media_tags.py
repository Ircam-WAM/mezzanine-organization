# -*- coding: utf-8 -*-
from mezzanine.template import Library

register = Library()

@register.filter
def get_photo_alignment(value):
    if value == 'left':
        return 0
    elif value == 'center':
        return 0.5
    return 1

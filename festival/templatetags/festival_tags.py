# -*- coding: utf-8 -*-
from mezzanine.pages.models import Page
from django import template

register = template.Library()

@register.simple_tag
def edito():
    qs = Page.objects.filter(title="Edito")
    if qs:
        return qs[0].content
    else:
        return ''

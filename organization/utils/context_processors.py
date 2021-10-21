# -*- coding: utf-8 -*-
from django.conf import settings


def static_hash(request):
    """
        Context processor to set archiprod to True
        for the main ressource menu
    """
    return {"static_hash": settings.STATIC_HASH}

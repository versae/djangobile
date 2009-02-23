# -*- coding: utf-8 -*-
from django.conf import settings


if hasattr(settings, 'WURFL_CLASS'):
    devices = getattr(__import__(settings.WURFL_CLASS, {}, {}, ['devices']),
                      'devices')
else:
    from djangobile.wurfl import devices

from djangobile.families import families

__all__ = ['devices', 'families']

from django.conf import settings


__all__ = ['devices']

if hasattr(settings, 'WURFL_CLASS'):
    devices = getattr(__import__(settings.WURFL_CLASS, {}, {}, \
                                 ['devices']), 'devices')
else:
    from djangobile.wurfl import devices


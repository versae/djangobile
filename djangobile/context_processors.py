# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson

from djangobile.utils import get_device, device_log

def mobile(request):
    crash_if_not_user_agent = getattr(settings, 'CRASH_IF_NOT_USER_AGENT', False)
    if crash_if_not_user_agent:
        default_user_agent = None
    else:
        # Report Fennec user agent in order to no crash djangobile when client
        # browser has no user agent string.
        default_user_agent = getattr(settings,
                                     'DEFAULT_USER_AGENT',
                                     "Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1")
    user_agent = request.META.get('HTTP_USER_AGENT', default_user_agent)
    if getattr(settings, 'DEBUG', False) and hasattr(request, 'device'):
        device = request.device
        if getattr(device, 'user_agent', False) != user_agent:
            device = get_device(user_agent)
            request.session['device_id'] = device.id
        device_log(request, device)
        return {'device': device}
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        device_id = request.session.get('device_id', False)
        if not device_id:
            device = get_device(user_agent)
            request.session['device_id'] = device.id
            device_log(request, device)
        else:
            device = get_device(device_id=device_id)
    else:
        device = get_device(user_agent)
        request.session['device_id'] = device.id
        device_log(request, device)
    request.session.set_test_cookie()
    return {'device': device}

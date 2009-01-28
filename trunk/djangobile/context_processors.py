# -*- coding: utf-8 -*-
from django.utils import simplejson

from djangobile.utils import get_device, device_log

def mobile(request):
    if hasattr(request, 'device'):
        device = request.device
        if device.get('user_agent', False) != request.META['HTTP_USER_AGENT']:
            device = get_device(request.META['HTTP_USER_AGENT'])
            request.session['device'] = device
        device_log(request)
    elif request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        device = request.session.get('device', False)
        if not device:
            device = get_device(request.META['HTTP_USER_AGENT'])
            request.session['device'] = device
            device_log(request)
    else:
        device = get_device(request.META['HTTP_USER_AGENT'])
        request.session['device'] = device
        device_log(request)
    request.session.set_test_cookie()
    return {'device': device}

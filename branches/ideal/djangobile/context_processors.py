# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson

from djangobile.utils import get_device, device_log

def mobile(request):
    device_detection = getattr(settings, 'DEVICE_DETECTION_VARIABLE', 'device_detection')
    if device_detection not in request.session:
        request.session[device_detection] = True
    elif device_detection in request.GET:
        if request.GET[device_detection].lower() == 'false':
            request.session[device_detection] = False
        else:
            request.session[device_detection] = True
    if not request.session[device_detection]:
        return {}
    crash_if_not_user_agent = getattr(settings, 'CRASH_IF_NOT_USER_AGENT', False)
    if crash_if_not_user_agent:
        default_user_agent = None
    else:
        default_user_agent = getattr(settings, 'DEFAULT_USER_AGENT', '')
    user_agent = request.META.get('HTTP_USER_AGENT', default_user_agent)
    if hasattr(request, 'device'):
        device = request.device
        if (getattr(settings, 'DEBUG', False) and
            getattr(device, 'user_agent', False) != user_agent):
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

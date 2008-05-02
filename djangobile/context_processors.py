# -*- coding: utf-8 -*-
from django.utils import simplejson

from djangobile.utils import get_device

def mobile(request):
    if hasattr(request, 'device'):
        device = request.device
    elif request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        device = request.session.get('device', False)
        if not device:
            device = get_device(request.META['HTTP_USER_AGENT'])
            request.session['device'] = device
    else:
        device = get_device(request.META['HTTP_USER_AGENT'])
        request.session['device'] = device
    request.session.set_test_cookie()
    return {'device': device}

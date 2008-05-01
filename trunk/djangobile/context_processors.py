# -*- coding: utf-8 -*-
from djangobile.utils import get_device

def mobile(request):
    device = get_device(request.META['HTTP_USER_AGENT'])
    return {'device': device}

# -*- coding: utf-8 -*-


def mobile(request):
    return {'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT']}

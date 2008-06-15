# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.utils.translation import gettext as _

from djangobile.shortcuts import render_to_response


def index(request):
    profile = {'getNick': 'djangobile',
                'getFirstName': 'Django Mobile Middleware'}
    l = [1, 2, 3]
    return render_to_response('test.html',
                            {'profile': profile,
                            'list': l},
                            mobile_template_name = 'test.xml',
                            context_instance = RequestContext(request))

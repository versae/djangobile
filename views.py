# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.utils.translation import gettext as _

from djangobile.shortcuts import render_to_response


def index(request):
    profile = {'getNick': 'djangobile',
               'getFirstName': 'Django Mobile Middleware'}
    l = range(1, 4)

    return render_to_response('test.xml',
                              {'profile': profile,
                               'list': l},
                              context_instance=RequestContext(request))

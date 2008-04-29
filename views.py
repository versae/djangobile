# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.utils.translation import gettext as _
from django.conf import settings

from djangobile.shortcuts import render_to_response


def index(request):
    profile = {'getNick': 'djangobile',
                'getFirstName': 'Django Mobile Middleware'}
    l = [1, 2 ,3]
    return render_to_response('test.xml',
                            {'profile': profile,
                            'list': l},
                            context_instance = RequestContext(request))

# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext as _

from djangobile.shortcuts import render_to_response


def redirect(request):
    return HttpResponseRedirect(reverse('contacts.views.list'))


def show(request):
    return HttpResponse('mostrado')


def list(request):
    return render_to_response("list.html", {}, context_instance=RequestContext(request))
    return HttpResponse('listado')


def add(request):
    return HttpResponse('adición')


def edit(request, contact_id):
    return HttpResponse('edición')


def delete(request, contact_id):
    return HttpResponse('borrado')

from django.forms.models import ModelFormMetaclass, ModelForm
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.utils.translation import ugettext
from django.contrib.auth.views import redirect_to_login
from django.views.generic import GenericViewError
from django.views.generic.create_update import (apply_extra_context, get_model_and_form_class,
                                                redirect, lookup_object)

from djangobile.template import loader

def create_object(request, model=None, template_name=None,
        template_loader=loader, extra_context=None, post_save_redirect=None,
        login_required=False, context_processors=None, form_class=None):
    """
    Generic object-creation function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save()
            if request.user.is_authenticated():
                request.user.message_set.create(message=ugettext("The %(verbose_name)s was created successfully.") % {"verbose_name": model._meta.verbose_name})
            return redirect(post_save_redirect, new_object)
    else:
        form = form_class()

    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    if hasattr(request, 'device'):
        d = getattr(request, 'device', {})
        t = template_loader.get_template(template_name, d)
    else:
        t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    }, context_processors)
    apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))

def update_object(request, model=None, object_id=None, slug=None,
        slug_field='slug', template_name=None, template_loader=loader,
        extra_context=None, post_save_redirect=None, login_required=False,
        context_processors=None, template_object_name='object',
        form_class=None):
    """
    Generic object-update function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
        object
            the original object being edited
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    model, form_class = get_model_and_form_class(model, form_class)
    obj = lookup_object(model, object_id, slug, slug_field)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            if request.user.is_authenticated():
                request.user.message_set.create(message=ugettext("The %(verbose_name)s was updated successfully.") % {"verbose_name": model._meta.verbose_name})
            return redirect(post_save_redirect, obj)
    else:
        form = form_class(instance=obj)

    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    if hasattr(request, 'device'):
        d = getattr(request, 'device', {})
        t = template_loader.get_template(template_name, d)
    else:
        t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
        template_object_name: obj,
    }, context_processors)
    apply_extra_context(extra_context, c)
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.attname))
    return response

def delete_object(request, model, post_delete_redirect, object_id=None,
        slug=None, slug_field='slug', template_name=None,
        template_loader=loader, extra_context=None, login_required=False,
        context_processors=None, template_object_name='object'):
    """
    Generic object-delete function.

    The given template will be used to confirm deletetion if this view is
    fetched using GET; for safty, deletion will only be performed if this
    view is POSTed.

    Templates: ``<app_label>/<model_name>_confirm_delete.html``
    Context:
        object
            the original object being deleted
    """
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    obj = lookup_object(model, object_id, slug, slug_field)

    if request.method == 'POST':
        obj.delete()
        if request.user.is_authenticated():
            request.user.message_set.create(message=ugettext("The %(verbose_name)s was deleted.") % {"verbose_name": model._meta.verbose_name})
        return HttpResponseRedirect(post_delete_redirect)
    else:
        if not template_name:
            template_name = "%s/%s_confirm_delete.html" % (model._meta.app_label, model._meta.object_name.lower())
        if hasattr(request, 'device'):
            d = getattr(request, 'device', {})
            t = template_loader.get_template(template_name, d)
        else:
            t = template_loader.get_template(template_name)
        c = RequestContext(request, {
            template_object_name: obj,
        }, context_processors)
        apply_extra_context(extra_context, c)
        response = HttpResponse(t.render(c))
        populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.attname))
        return response

from django.template import RequestContext
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseGone
from django.views.generic.simple import redirect_to

from djangobile.template import loader

def direct_to_template(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None: extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    if hasattr(request, 'device'):
        d = getattr(request, 'device', {})
        t = template_loader.get_template(template_name, d)
    else:
        t = loader.get_template(template)
    return HttpResponse(t.render(c), mimetype=mimetype)

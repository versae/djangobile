# -*- coding: utf-8 -*-
from os import path

from django.template import TemplateDoesNotExist
from django.template.loader import find_template_source, get_template_from_string
from django.conf import settings

from djangobile.ideal import Ideal


def get_template(template_name, device_family=None):
    """
    Returns a compiled Template object for the given template name,
    handling template inheritance recursively.
    """
    try:
        print device_family
        template_name_device = path.join(device_family, template_name)
        source, origin = find_template_source(template_name_device)
    except AttributeError, TemplateDoesNotExist:
        source, origin = find_template_source(template_name)
    template = get_template_from_string(source, origin, template_name)
    return template

def render_to_string(template_name, dictionary=None, context_instance=None):
    """
    Loads the given template_name and renders it with the given dictionary as
    context. The template_name may be a string to load a single template using
    get_template, or it may be a tuple to use select_template to find one of
    the templates in the list. Returns a string.
    """
    dictionary = dictionary or {}
    user_agent = context_instance.get('HTTP_USER_AGENT', None)
    device_family = get_device_family(user_agent)
    if isinstance(template_name, (list, tuple)):
        t = select_template(template_name, device_family)
    else:
        t = get_template(template_name, device_family)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)

    ideal = Ideal(t.render(None))
    return ideal.render(context_instance)

def select_template(template_name_list, device_family=None):
    "Given a list of template names, returns the first that can be loaded."
    for template_name in template_name_list:
        try:
            return get_template(template_name, device_family)
        except TemplateDoesNotExist:
            continue
    # If we get here, none of the templates could be loaded
    raise TemplateDoesNotExist, ', '.join(template_name_list)


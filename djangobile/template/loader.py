# -*- coding: utf-8 -*-
from os import path

from django.conf import settings
from django.template import TemplateDoesNotExist, add_to_builtins
from django.template.loader import find_template_source, get_template_from_string

from djangobile.template import Ideal
from djangobile.template.ideal import MalformedIdealTemplateException
from djangobile.utils import (get_device_template_paths, is_ideal_template,
                              template_log)


def get_template(template_name, device=None, log=None):
    """
    Returns a compiled Template object for the given template name,
    handling template inheritance recursively.
    """
    source, origin = None, None
    exceptions_list = []
    if device:
        device_path_list = get_device_template_paths(device, template_name)
        for device_path in device_path_list:
            try:
                source, origin = find_template_source(device_path)
            except TemplateDoesNotExist:
                exceptions_list.append(device_path)
            if source:
                template_log(device_path, log=log)
                break
    if not source:
        try:
            source, origin = find_template_source(template_name)
            template_log(template_name, log=log)
        except TemplateDoesNotExist:
            exceptions_list.append(template_name)
            raise TemplateDoesNotExist, exceptions_list
    template = get_template_from_string(source, origin, template_name)
    return template

def render_to_string(template_name, dictionary=None, context_instance=None, \
                     processor_class=None):
    """
    Loads the given template_name and renders it with the given dictionary as
    context. The template_name may be a string to load a single template using
    get_template, or it may be a tuple to use select_template to find one of
    the templates in the list. Returns a string.
    """
    dictionary = dictionary or {}
    device = context_instance.get('device', None)

    if isinstance(template_name, (list, tuple)):
        t = select_template(template_name, device)
    else:
        t = get_template(template_name, device)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)

    rendered_template = t.render(context_instance)
    if hasattr(settings, 'IDEAL_LANGUAGE_SUPPORT') and \
       settings.IDEAL_LANGUAGE_SUPPORT:
        try:
            is_ideal_template(rendered_template, template_name)
        except AssertionError, e:
            raise MalformedIdealTemplateException("(%s) %s: %s" % (device.get('user_agent', None), template_name, e.message))
        ideal = Ideal(rendered_template)
        return ideal.render(context_instance, cls=processor_class)
    else:
        return rendered_template

def select_template(template_name_list, device=None, log=None):
    "Given a list of template names, returns the first that can be loaded."
    for template_name in template_name_list:
        try:
            return get_template(template_name, device, log)
        except TemplateDoesNotExist:
            continue
    # If we get here, none of the templates could be loaded
    raise TemplateDoesNotExist, ', '.join(template_name_list)

add_to_builtins('djangobile.template.loader_tags')

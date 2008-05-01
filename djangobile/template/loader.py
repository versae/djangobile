# -*- coding: utf-8 -*-
from os import path

from django.template import TemplateDoesNotExist
from django.template.loader import find_template_source, get_template_from_string
from django.conf import settings

from djangobile.ideal import Ideal


def get_template(template_name, device=None):
    """
    Returns a compiled Template object for the given template name,
    handling template inheritance recursively.
    """
    source, origin = None, None
    exception_list = []
    if device:
        if hasattr(settings, 'DEVICE_SEARCH_ORDER'):
            device_path_dic = {'id': path.join(device.devid, template_name),
                        'user_agent': path.join(device.devua, template_name),
                        'fall_back': path.join(device.fall_back, template_name),
                        'preferred_markup': path.join(device.preferred_markup, template_name),
                        'model_name': path.join(device.model_name, template_name),
                        'brand_name': path.join(device.brand_name, template_name)}
            device_path_list = []
            for device_path in settings.DEVICE_SEARCH_ORDER:
                if device_path in device_path_dic:
                    device_path_list.append(device_path_dic.pop(device_path))
            for device_path in device_path_dic:
                device_path_list.append(device_path_dic.get(device_path))
        else:
            device_path_list = [path.join(device.devid, template_name),
                        path.join(device.devua, template_name),
                        path.join(device.fall_back, template_name),
                        path.join(device.preferred_markup, template_name),
                        path.join(device.model_name, template_name),
                        path.join(device.brand_name, template_name)]
        for device_path in device_path_list:
            try:
                source, origin = find_template_source(device_path)
            except TemplateDoesNotExist:
                exception_list.append(device_path)
            if source and origin:
                break
    if not source or not origin:
        try:
            source, origin = find_template_source(template_name)
        except TemplateDoesNotExist:
            exception_list.append(template_name)
            raise TemplateDoesNotExist, exception_list
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
    device = context_instance.get('device', None)

    if isinstance(template_name, (list, tuple)):
        t = select_template(template_name, device)
    else:
        t = get_template(template_name, device)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)

    rendered_temlate = t.render(context_instance)
    ideal = Ideal(rendered_template)
    return ideal.render(context_instance)

def select_template(template_name_list, device=None):
    "Given a list of template names, returns the first that can be loaded."
    for template_name in template_name_list:
        try:
            return get_template(template_name, device)
        except TemplateDoesNotExist:
            continue
    # If we get here, none of the templates could be loaded
    raise TemplateDoesNotExist, ', '.join(template_name_list)


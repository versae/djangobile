# -*- coding: utf-8 -*-
import re
from os import path

from django.conf import settings
from django.utils.translation import gettext as _

from wurfl import devices
from pywurfl.algorithms import Tokenizer


def get_device(user_agent=None, device_id=None):
    assert(((user_agent and not device_id) or (not user_agent and device_id)), _('user_agent or device_id must be passed, but not both.'))
    if user_agent:
        device = devices.select_ua(user_agent, filter_noise=True, search=Tokenizer(), instance=True)
    else:
        device = devices.select_id(user_agent, instance=True)
    device_dic = {}
    for device_property in device:
        capability = device_property[1]
        value = device_property[2]
        device_dic[capability] = value
    device_dic['id'] = device.devid
    device_dic['user_agent'] = device.devua
    device_dic['fall_back'] = device.fall_back
    return device_dic


def get_device_template_paths(device, template_name):
    device_properties = ['id', 'user_agent', 'fall_back', 'preferred_markup', 'model_name', 'brand_name']
    device_path_list = []
    if hasattr(settings, 'DEVICE_SEARCH_ORDER'):
        for device_property in settings.DEVICE_SEARCH_ORDER:
            if device_property in device_properties:
                device_path_list.append(path.join(device.get(device_property), template_name))
                device_properties.remove(device_property)
    for device_property in device_properties:
        device_path_list.append(path.join(device.get(device_property), template_name))
    return device_path_list

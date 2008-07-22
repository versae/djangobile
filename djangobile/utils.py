# -*- coding: utf-8 -*-
from mimetypes import guess_type
from os import path

from django.conf import settings
from django.utils.translation import gettext as _


def get_device(user_agent=None, device_id=None):
    assert(((user_agent and not device_id) or (not user_agent and device_id)), \
            _('user_agent or device_id must be passed, but not both.'))
    if hasattr(settings, 'WURFL_CLASS'):
        devices = getattr(__import__(settings.WURFL_CLASS, {}, {}, \
                                     ['devices']), 'devices')
    else:
        from djangobile.wurfl import devices
    if hasattr(settings, 'USER_AGENT_SEARCH_ALGORITHM'):
        search_algorithm = getattr(__import__('pywurfl.algorithms', {}, {}, \
                                      [settings.USER_AGENT_SEARCH_ALGORITHM]), \
                                      settings.USER_AGENT_SEARCH_ALGORITHM)()
    else:
        from pywurfl.algorithms import Tokenizer
        search_algorithm = Tokenizer()
    if user_agent:
        device = devices.select_ua(user_agent, filter_noise=True, \
                                   search=search_algorithm, instance=True)
    else:
        device = devices.select_id(device_id, instance=True)
    device_dic = {}
    for group, capability, value in device:
        device_dic[capability] = value
    device_dic['id'] = device.devid
    device_dic['user_agent'] = device.devua
    device_dic['fall_back'] = device.fall_back
    # TODO: Make real these values!
    device_user_agent = device.devua.lower()
    device_dic['is_pc_device'] = ('firefox' in device_user_agent) or \
                                 ('explorer' in device_user_agent) or \
                                 ('opera' in device_user_agent) or \
                                 ('safari' in device_user_agent)
    device_dic['is_pda_device'] = device_dic['is_pc_device'] and \
                                  ('windows mobile' in device_user_agent)
    device_dic['is_mobile_device'] = not device_dic['is_pc_device'] and \
                                     not device_dic['is_pda_device']
    return device_dic

def get_device_template_paths(device, template_name):
    device_properties = ['id', 'user_agent', 'fall_back', 'preferred_markup', \
                         'model_name', 'brand_name']
    device_path_list = []
    if hasattr(settings, 'DEVICE_SEARCH_ORDER'):
        for device_property in settings.DEVICE_SEARCH_ORDER:
            if device_property in device_properties:
                device_path = path.join(device.get(device_property), template_name)
                device_path_list.append(device_path)
                device_property_lower = device.get(device_property).lower()
                if device_property_lower != device.get(device_property):
                    device_path = path.join(device_property_lower, template_name)
                    device_path_list.append(device_path)
                device_properties.remove(device_property)
    for device_property in device_properties:
        device_path = path.join(device.get(device_property), template_name)
        device_path_list.append(device_path)
        device_property_lower = device.get(device_property).lower()
        if device_property_lower != device.get(device_property):
            device_path = path.join(device_property_lower, template_name)
            device_path_list.append(device_path)
    return device_path_list

def is_ideal_template(rendered_template, template_name=None):
    validates_xml_schema = True
    if hasattr(settings, 'IDEAL_XML_SCHEMA_FILE'):
        xsd_file = open(settings.IDEAL_XML_SCHEMA_FILE)
    else:
        xsd_file = open(path.join('djangobile', 'transformations', 'cmt.xsd'))
    try:
        import lxml.etree as etree
        from StringIO import StringIO
        xml_schema_doc = etree.parse(xsd_file)
        xml_schema = etree.XMLSchema(xml_schema_doc)
        ideal_file = StringIO(rendered_template.encode("utf-8"))
        ideal_doc = etree.parse(ideal_file)
        validates_xml_schema = xml_schema.validate(ideal_doc)
    except ImportError:
        pass
    xsd_file.close()
    if not validates_xml_schema and xml_schema and xml_schema.error_log:
        raise AssertionError("Document does not comply with schema:\n%s"
                             % xml_schema.error_log.last_error)
    if template_name:
        mime_type = guess_type(template_name)
        return (mime_type[0] == 'application/xml') and validates_xml_schema
    else:
        return validates_xml_schema

# -*- coding: utf-8 -*-
import os

from datetime import datetime
from mimetypes import guess_type
from pywurfl import algorithms

from django.conf import settings
from django.template import TemplateSyntaxError, Variable
from django.utils.datastructures import SortedDict

try:
    from extra_devices import devices
except ImportError:
    from djangobile import devices


def get_device(user_agent=None, device_id=None):
    assert(((user_agent and not device_id) or (not user_agent and device_id)),
            'User_agent or device_id must be passed, but not both.')
    if hasattr(settings, 'USER_AGENT_SEARCH_ALGORITHM'):
        if settings.USER_AGENT_SEARCH_ALGORITHM == 'JaroWinkler':
            kwaccuracy = {'accuracy': getattr(settings, 'JARO_WINKLER_ACCURACY', 0.9)}
        else:
            kwaccuracy = {}
        search_algorithm = getattr(__import__('pywurfl.algorithms', {}, {},
                                              [settings.USER_AGENT_SEARCH_ALGORITHM]),
                                              settings.USER_AGENT_SEARCH_ALGORITHM)(**kwaccuracy)
    else:
        search_algorithm = algorithms.Tokenizer()
    try:
        if user_agent:
            device = devices.select_ua(user_agent, filter_noise=True,
                                       search=search_algorithm, instance=True)
        else:
            device = devices.select_id(device_id, instance=True)
    except algorithms.DeviceNotFound:
        device = devices.select_id('generic', instance=True)
    setattr(device, 'user_agent', device.devua)
    setattr(device, 'real_user_agent', user_agent)
    setattr(device, 'id', device.devid)
    setattr(device, 'real_id', device_id)
    if getattr(settings, 'QUERY_LANGUAGE_SUPPORT', False):
        from pywurfl.ql import QL
        device_query = getattr(device, 'query', None)
        if not callable(device_query):
            query = getattr(devices, 'query', None)
            if not query:
                query = QL(devices)
            setattr(device, 'query', query)
    device_families = get_device_families(device)
    setattr(device, 'family', device_families)
    setattr(device, 'belongs_to',
            lambda family: device.family.get(family, False))
    return device


def get_device_directories(device):
    device_properties = ['id', 'user_agent', 'fall_back', 'preferred_markup',
                         'model_name', 'brand_name', 'family']
    device_path_list = []
    if hasattr(settings, 'DEVICE_SEARCH_ORDER'):
        for device_property in settings.DEVICE_SEARCH_ORDER:
            if device_property in device_properties:
                if device_property == 'family':
                    for family in getattr(device, device_property):
                        device_family = device.family.get(family, False)
                        if device_family and family:
                            device_path_list.append(family)
                else:
                    device_path = getattr(device, device_property)
                    if device_path:
                        device_path_list.append(device_path)
                    device_path_lower = device_path.lower()
                    if device_path_lower != device_path and device_path_lower:
                        device_path_list.append(device_path_lower)
                device_properties.remove(device_property)
    for device_property in device_properties:
        if device_property == 'family':
            for family in getattr(device, device_property):
                device_family = device.family.get(family, False)
                if device_family and family:
                    device_path_list.append(family)
            break;
        device_path = getattr(device, device_property)
        if device_path:
            device_path_list.append(device_path)
        device_path_lower = device_path.lower()
        if device_path_lower != device_path and device_path_lower:
            device_path_list.append(device_path_lower)

    return device_path_list


def get_device_template_paths(device, template_name):
    device_path_directories = get_device_directories(device)
    device_path_list = []
    for directory in device_path_directories:
        device_path_list.append(os.path.join(directory, template_name))

    return device_path_list


def get_device_families(device):
    family_dic = SortedDict()
    try:
        from extra_families import families
    except ImportError:
        from djangobile import families
    for (family, query) in families.items():
        if callable(query):
            family_dic[family] = bool(query(device))
        elif hasattr(device, 'query'):
            ql = """select id where %s""" % query
            family_dic[family] = False
            for device_id in devices.query(ql):
                if device.id == device_id:
                    family_dic[family] = True
                    break;
        else:
            family_dic[family] = False
    return family_dic


def parse_args_kwargs_and_as_var(parser, token):
    """
    Parse uniformly args and kwargs from a templatetag

    Taken from cmsutils: https://tracpub.yaco.es/cmsutils/browser/branches/change_media_directory/tag_utils.py

    Usage::

      For parsing a template like this:

      {% footag my_contents, height=10, zoom=20 as myvar %}

      You simply do this:

      @register.tag
      def footag(parser, token):
          args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, token)
    """
    bits = token.contents.split(' ')

    if len(bits) <= 1:
        raise TemplateSyntaxError("'%s' takes at least one argument" % bits[0])

    args = []
    kwargs = {}
    as_var = None

    bits = iter(bits[1:])
    for bit in bits:
        if bit == 'as':
            as_var = bits.next()
            break
        else:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    try:
                        kwargs[str(k)] = eval(v, None, None)
                    except NameError:
                        kwargs[k] = Variable(v.strip())
                elif arg:
                    try:
                        args.append(eval(arg, None, None))
                    except NameError:
                        args.append(Variable(arg.strip()))
    return args, kwargs, as_var


def device_log(request, device):
    show_log = getattr(settings, 'DEVICE_SHOW_LOG', False)
    if (show_log and device and hasattr(request, 'device')):
        today = datetime.today().strftime("%d/%b/%Y %H:%M:%S")
        properties = []
        families = getattr(device, 'family', {})
        device_properties = ['fall_back', 'preferred_markup', 'model_name',
                             'brand_name']
        for device_property in device_properties:
            prop = getattr(device, device_property, False)
            if prop:
                properties.append(prop)
        for family in families:
            if families[family]:
                properties.append(family)
        print "[%s] \"HTTP_USER_AGENT %s\"" % (today,
                                   request.META.get('HTTP_USER_AGENT', 'No user agent!')
        )
        print "[%s] \"DEVICE %s\" (%s)" % (today,
                                            device.devid,
                                            ", ".join(properties))


def template_log(template_name, log=None):
    show_log = getattr(settings, 'DEVICE_SHOW_LOG', False)
    if show_log:
        today = datetime.today().strftime("%d/%b/%Y %H:%M:%S")
        log_type = log and "(%s) " % log or ''
        print "[%s] \"TEMPLATE %s%s\"" % (today, log_type, template_name)


def is_ideal_template(rendered_template, template_name=None):
    validates_xml_schema = True
    if hasattr(settings, 'IDEAL_XML_SCHEMA_FILE'):
        xsd_file = open(settings.IDEAL_XML_SCHEMA_FILE)
    else:
        xsd_file = open(os.path.join('djangobile', 'transformations', 'cmt.xsd'))
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

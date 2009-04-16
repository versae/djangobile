# -*- coding: utf-8 -*-
from django.utils.datastructures import SortedDict


class FamiliesException(Exception):
    pass


class Families(SortedDict):
    def add(self, func):
        if callable(func):
            self.update({func.func_name: func})
        elif isinstance(func, dict):
            self.update(func)
        else:
            raise FamiliesException('func is not function neither dict instance.')

families = Families()


@families.add
def wap_device(device):
    return (device.preferred_markup == 'wml_1_1' or
            device.preferred_markup == 'wml_1_2' or
            device.preferred_markup == 'wml_1_3')

@families.add
def imode_device(device):
    return (device.preferred_markup == 'html_wi_imode_html_1' or
            device.preferred_markup == 'html_wi_imode_html_2' or
            device.preferred_markup == 'html_wi_imode_html_3' or
            device.preferred_markup == 'html_wi_imode_html_4' or
            device.preferred_markup == 'html_wi_imode_html_5' or
            device.preferred_markup == 'html_wi_imode_htmlx_1' or
            device.preferred_markup == 'html_wi_imode_htmlx_1_1')

@families.add
def xhtml_mp_device(device):
    return (device.preferred_markup == 'html_wi_oma_xhtmlmp_1_0' or
            (device.preferred_markup == 'html_wi_w3_xhtmlbasic' and 
             device.html_wi_oma_xhtmlmp_1_0 == True))

@families.add
def pda_device(device):
    return (device.preferred_markup == 'html_web_3_2' and
            device.rows > 8 and device.rows < 15 and device.columns < 40 and
            device.is_wireless_device == True)

@families.add
def pc_device(device):
    return (device.preferred_markup == 'html_web_4_0' and
            device.is_wireless_device == False)

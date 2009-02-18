from django.conf import settings


__all__ = ['devices', 'families']

if hasattr(settings, 'WURFL_CLASS'):
    devices = getattr(__import__(settings.WURFL_CLASS, {}, {}, ['devices']),
                      'devices')
else:
    from djangobile.wurfl import devices

families = {}

def pc_device(device):
    return (device.preferred_markup == 'html_web_4_0' and
            device.is_wireless_device == False)
families['pc_device'] = pc_device

def pda_device(device):
    return (device.preferred_markup == 'html_web_3_2' and
            device.rows > 8 and device.rows < 15 and device.columns < 40 and
            device.is_wireless_device == True)
families['pda_device'] = pda_device

def wap_device(device):
    return (device.preferred_markup == 'wml_1_1' or
            device.preferred_markup == 'wml_1_2' or
            device.preferred_markup == 'wml_1_3')
families['wap_device'] = wap_device

def imode_device(device):
    return (device.preferred_markup == 'html_wi_imode_html_1' or
            device.preferred_markup == 'html_wi_imode_html_2' or
            device.preferred_markup == 'html_wi_imode_html_3' or
            device.preferred_markup == 'html_wi_imode_html_4' or
            device.preferred_markup == 'html_wi_imode_html_5' or
            device.preferred_markup == 'html_wi_imode_htmlx_1' or
            device.preferred_markup == 'html_wi_imode_htmlx_1_1')
families['imode_device'] = imode_device

def xhtml_mp_device(device):
    return (device.preferred_markup == 'html_wi_oma_xhtmlmp_1_0' or
            (device.preferred_markup == 'html_wi_w3_xhtmlbasic' and 
             device.html_wi_oma_xhtmlmp_1_0 == True))
families['xhtml_mp_device'] = xhtml_mp_device

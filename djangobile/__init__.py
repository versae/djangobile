from django.conf import settings


__all__ = ['devices', 'families']

if hasattr(settings, 'WURFL_CLASS'):
    devices = getattr(__import__(settings.WURFL_CLASS, {}, {}, ['devices']),
                      'devices')
else:
    from djangobile.wurfl import devices

families = {}
families['pc_device'] = """preferred_markup = 'html_web_4_0' and """ \
                        """is_wireless_device = false"""
families['pda_device'] = """preferred_markup = 'html_web_3_2' and """ \
                         """rows > 8 and rows < 15 and columns < 40 and """ \
                         """is_wireless_device = true"""
families['wap_device'] = """preferred_markup = 'wml_1_1' or """ \
                         """preferred_markup = 'wml_1_2' or """ \
                         """preferred_markup = 'wml_1_3'"""
families['imode_device'] = """preferred_markup = 'html_wi_imode_html_1' or """ \
                           """preferred_markup = 'html_wi_imode_html_2' or """ \
                           """preferred_markup = 'html_wi_imode_html_3' or """ \
                           """preferred_markup = 'html_wi_imode_html_4' or """ \
                           """preferred_markup = 'html_wi_imode_html_5' or """ \
                           """preferred_markup = 'html_wi_imode_htmlx_1' or """ \
                           """preferred_markup = 'html_wi_imode_htmlx_1_1'"""
def xhtml_mp_device(device):
    return (device.preferred_markup == 'html_wi_oma_xhtmlmp_1_0' or
            (device.preferred_markup == 'html_wi_w3_xhtmlbasic' and 
             device.html_wi_oma_xhtmlmp_1_0 == True))
families['xhtml_mp_device'] = xhtml_mp_device

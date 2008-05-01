# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.utils.translation import gettext as _

from wurfl import devices
from pywurfl.algorithms import Tokenizer


def get_device(user_agent=None, device_id=None):
    assert(((user_agent and not device_id) or (not user_agent and device_id)), _('user_agent or device_id must be passed, but not both.'))
    if user_agent:
        device = devices.select_ua(user_agent, filter_noise=True, search=Tokenizer(), instance=True)
    else:
        deice = devices.select_id(user_agent, instance=True)
    return device

#    user_agents_ignore_case = hasattr(settings, 'MOBILE_USER_AGENTS_IGNORE_CASE') and settings.MOBILE_USER_AGENTS_IGNORE_CASE    
#    if hasattr(settings, 'MOBILE_USER_AGENTS_PATTERNS') and isinstance(settings.MOBILE_USER_AGENTS_PATTERNS, (list, tuple)):
#        for user_agent_pattern in settings.MOBILE_USER_AGENTS_PATTERNS:
#            if isinstance(user_agent_pattern, (list, tuple)) and len(user_agent_pattern) == 2:
#                pattern = user_agent_pattern[0]
#                fall_back = user_agent_pattern[1]
#                if not user_agents_ignore_case:
#                    if re.compile(pattern).match(user_agent):
#                        return fall_back
#                    else:
#                        continue
#                else:
#                    if re.compile(pattern, re.I).match(user_agent.lower()):
#                        return fall_back
#                    else:
#                        continue
#            else:
#                raise UserAgentPatternException
#    if "firefox" in user_agent:
#        return "firefox"
#    elif "konqueror" in user_agent:
#        return "konqueror"
#    elif "nokia" in user_agent:
#        return "nokia"
#    else:
#        return None

#class UserAgentPatternException(Exception):
#    pass

# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings

from djangobile.context_processors import mobile


class DjangoMobileMiddleware(object):
    def process_response(self, request, response):
        if (hasattr(settings, 'DEBUG') and settings.DEBUG
            and hasattr(request, 'device')):
            print "[%s] From %s (%s): %s (%s)" % (
                    datetime.today().strftime("%d/%b/%Y %H:%M:%S"),
                    request.device.get('id', ''),
                    request.device.get('preferred_markup', ''),
                    request.device.get('user_agent', ''),
                    request.META.get('HTTP_USER_AGENT', '')
                )
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_request(self, request):
        device = mobile(request)['device']
        setattr(request, 'device', device)
        return None


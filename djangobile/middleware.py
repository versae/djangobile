# -*- coding: utf-8 -*-
from django.conf import settings

from djangobile.context_processors import mobile


class DjangoMobileMiddleware(object):
    def process_request(self, request):
        full_path = request.get_full_path()
        is_media_request = (full_path.startswith(settings.MEDIA_URL) and
                            full_path.startswith(settings.ADMIN_MEDIA_PREFIX))
        if not hasattr(request, 'device') and not is_media_request:
            device = getattr(mobile(request), 'device', None)
            setattr(request, 'device', device)
        return None


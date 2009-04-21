# -*- coding: utf-8 -*-
from django.conf import settings

from djangobile.context_processors import mobile
from djangobile.utils import translation


class DevicesMiddleware(object):
    def process_request(self, request):
        full_path = request.get_full_path()
        is_media_request = (full_path.startswith(settings.MEDIA_URL) and
                            full_path.startswith(settings.ADMIN_MEDIA_PREFIX))
        device = getattr(request, 'device', None)
        if not device and not is_media_request:
            device = mobile(request).get('device', None)
            setattr(request, 'device', device)
        return None


# Added to ensure backwards compatibility
class DjangoMobileMiddleware(DevicesMiddleware):
    pass


class LocaleMiddleware(object):
    """
    This is a very simple middleware that adds new catalogs to active
    translation objects according to device in the request.
    """

    def process_request(self, request):
        device = getattr(request, 'device', None)
        translation.add_device_locale(device)

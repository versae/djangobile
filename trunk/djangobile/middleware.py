# -*- coding: utf-8 -*-
from django.conf import settings 
try:
    MOBILE_IGNORE_ADMIN = settings.MOBILE_IGNORE_ADMIN
except AttributeError:
    MOBILE_IGNORE_ADMIN = False


class DjangoMobileMiddleware(object):
    def process_response(self, request, response):
        if MOBILE_IGNORE_ADMIN and request.user.is_authenticated() and request.user.is_staff:
            return response
        else:
            content = response.content
            index = content.upper().find('</BODY>')
            if index == -1:
                return response
            else:
                response.content =  content[:index] + '<h3>'+str(request.META['HTTP_USER_AGENT'])+'</h3>' + content[index:]
                return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_request(self, request):
        return None


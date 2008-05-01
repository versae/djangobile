# -*- coding: utf-8 -*-
from django.conf import settings 


class DjangoMobileMiddleware(object):
    def process_response(self, request, response):
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_request(self, request):
        return None


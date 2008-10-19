from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('contacts.views',
    (r'^$', 'redirect'),

    (r'^list/$', 'list'),
    (r'^add/$', 'add'),

    (r'^show/(?P<contact_id>\d+)/$', 'show'),
    (r'^edit/(?P<contact_id>\d+)/$', 'edit'),
    (r'^delete/(?P<contact_id>\d+)/$', 'delete'),

)

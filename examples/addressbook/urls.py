from os import path

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Static content
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': path.join(settings.BASEDIR, 'media')}),

    # Contacts
    (r'^$', 'contacts.views.redirect'),
    (r'^contacts/', include('contacts.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),


    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

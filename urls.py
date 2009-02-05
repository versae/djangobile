from os import path

from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    # Static content
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': path.join(settings.BASEDIR, 'media')}),

    # Django contrib
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^admin/', include('django.contrib.admin.urls')),
    
    # Default
    (r'^$', 'views.index'),

)

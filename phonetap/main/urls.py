from django.conf.urls.defaults import *

urlpatterns = patterns('phonetap.main.views',
    url(r'^$', 'homepage', name="phonetap-main-homepage")
)

from django.conf.urls.defaults import *

urlpatterns = patterns('PhoneTap.main.views',
    url(r'^$', 'homepage', name="PhoneTap-main-homepage")
)

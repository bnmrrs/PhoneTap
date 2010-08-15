from django.conf.urls.defaults import *

urlpatterns = patterns('phonetap.main.views',
	url(r'^make_call$', 'make_call', name="phonetap-main-make_call"),
    url(r'^$', 'homepage', name="phonetap-main-homepage"),
)

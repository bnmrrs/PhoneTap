from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^make_call$', 'phonetap.main.views.make_call', name="phonetap-main-make_call"),
    url(r'^$', 'phonetap.main.views.homepage', name="phonetap-main-homepage"),
	#(r'^$', include('phonetap.main.urls')),
)

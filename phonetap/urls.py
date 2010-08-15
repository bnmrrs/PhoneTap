from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^make_call$', 'phonetap.main.views.make_call', name="phonetap-main-make_call"),
	url(r'^outgoing_callback$', 'phonetap.main.views.outgoing_callback', name="phonetap-main-outgoing_inprogress"),
	url(r'^outgoing_recording_callback$', 'phonetap.main.views.outgoing_recording_callback', name="phonetap-main-outgoing_recording"),
    url(r'^$', 'phonetap.main.views.homepage', name="phonetap-main-homepage"),
	#(r'^$', include('phonetap.main.urls')),
)

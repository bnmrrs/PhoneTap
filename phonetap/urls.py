from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^make_call$', 'phonetap.main.views.make_call', name="phonetap-main-make_call"),
	url(r'^call/(?P<call_sid>\w{34})$', 'phonetap.main.views.view_call', name="phonetap-main-view_call"),
	url(r'^outgoing_callback$', 'phonetap.main.views.outgoing_callback', name="phonetap-main-outgoing_inprogress"),
	url(r'^outgoing_recording_callback$', 'phonetap.main.views.outgoing_recording_callback', name="phonetap-main-outgoing_recording"),
	url(r'^check_call_status/(?P<call_sid>\w{34})$', 'phonetap.main.views.check_call_status', name="phonetap-main-check_call_status"),
    url(r'^$', 'phonetap.main.views.homepage', name="phonetap-main-homepage"),
	#(r'^$', include('phonetap.main.urls')),
)

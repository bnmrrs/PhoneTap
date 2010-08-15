from django.utils import simplejson as json
from twiliosimple import Twilio, Utils

from phonetap.main.forms import CallForm

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

def homepage(request):
	form = CallForm()
	
	return render_to_response('index.html', {
		'form': form,
	})
	
def make_call(request):
	if request.is_ajax():
		form = CallForm(request.POST)
		
		if form.is_valid():
			callback = request.build_absolute_uri(
				reverse('phonetap-main-outgoing_inprogress')
			)
			
			twilio = Twilio(settings.TWILIO_ACCOUNT_SID, \
				settings.TWILIO_ACCOUNT_TOKEN)
				
			call = twilio.call(settings.TWILIO_SANDBOX_NUM, \
				form.cleaned_data['caller_num'], callback)
			
			response = json.dumps({'success':True})
		else:
			response_dict = {
				'success': False,
				'errors': form.errors
			}
			
			response = json.dumps(response_dict)
		
		return HttpResponse(response, 'application/javascript')
	else:
		return HttpResponse(status=400)
		
def outgoing_callback(request):
	if is_valid_twilio_request(request):
		callback = request.build_absolute_uri(
			reverse('phonetap-main-outgoing_recording')
			)
	
		return render_to_response('outgoing_callback.html', {
			'callback': callback
		})
	else:
		return HttpResponse(status=400)
	
def outgoing_recording_callback(request):
	return render_to_response('outgoing_recording_callback.html', {})
	

def is_valid_twilio_request(request):
	if not request.method == 'POST':
		return False

	twilio_utils = Utils(settings.TWILIO_ACCOUNT_SID,
		settings.TWILIO_ACCOUNT_TOKEN)

	postvars = request.POST
	signature = request.META['HTTP_X_TWILIO_SIGNATURE']
	url = request.build_absolute_uri()

	return twilio_utils.validateRequest(url, postvars, signature)
from datetime import datetime
import simplejson as json
import logging

from twiliosimple import Twilio, Utils
from django_twilio_utils.decorators import twilio_request

from phonetap.main.forms import CallForm
from phonetap.main.documents import Call

from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

def homepage(request):
	form = CallForm()
	
	return render_to_response('index.html', {
		'form': form,
	})
	
def view_call(request, call_sid):
	call = get_call(call_sid)
	
	return render_to_response('call.html', {
		'call': call
	})
	
def make_call(request):
	if request.is_ajax():
		form = CallForm(request.POST)
		
		if form.is_valid():
			callback = request.build_absolute_uri(
				reverse('phonetap-main-outgoing_inprogress')
			)
			
			twilio = Twilio(settings.TWILIO_API_SID, \
				settings.TWILIO_API_TOKEN)
				
			twilio_response = twilio.call(settings.TWILIO_SANDBOX_NUM, \
				form.cleaned_data['caller_num'], callback).get_response()
				
			call = Call(
				call_sid=twilio_response['call_sid'],
				caller_number=form.cleaned_data['caller_num'],
				callee_number=form.cleaned_data['callee_num'],
				caller_email=form.cleaned_data['caller_email'],
				current_status='Dialing'
			)
			
			call.save()
			
			response = json.dumps({
				'success': True,
				'call_page_url': request.build_absolute_uri(
					reverse('phonetap-main-view_call', args=[call.call_sid])
				)
			})
		else:
			response = json.dumps({
				'success': False,
				'errors': form.errors
			})
		
		return HttpResponse(response, 'application/javascript')
	else:
		return HttpResponse(status=400)
		
@twilio_request
def outgoing_callback(request):
	if request.POST['CallStatus'] == 'completed':
		return HttpResponse(status=200)
			
	call = get_call(request.POST['CallSid'])
			
	call.current_status = 'In Progress'
	call.save()
							
	callback = request.build_absolute_uri(
		reverse('phonetap-main-outgoing_recording')
	)
	
	return render_to_response('outgoing_callback.html', {
		'callback': callback,
		'number': call.callee_number
	})

@twilio_request	
def outgoing_recording_callback(request):
	call = get_call(request.POST['CallSid'])
		
	call.current_status = 'Completed'
	call.end_time = datetime.now()
	call.recording_url = request.POST['RecordingUrl']
	call.duration = request.POST['DialCallDuration']
	call.save()
		
	msg = mail.EmailMessage()
	msg.sender = settings.SENDER_EMAIL
	msg.to = call.caller_email
	msg.subject = "PhoneTap - Call Recording"
	msg.body = """Dear %s,
		
Your call recording has been processed and is now avaliable.  
You can now vist %s to listen to and download an .MP3 of your call.
	
The PhoneTap Team
""" % (call.caller_email, request.build_absolute_uri(
				reverse('phonetap-main-view_call', args=[call.call_sid])
	))

	msg.send()
		
	return render_to_response('outgoing_recording_callback.html', {})
		

def check_call_status(request, call_sid):
	call = get_call(call_sid)
	
	response = json.dumps({
		'call_status': call.current_status,
	})
	return HttpResponse(response, 'application/javascript')
	
		
def get_call(sid):
	print sid
	try:
		call = Call.objects(call_sid=sid)[0]
	except IndexError:
		raise Http404
	return call
from twiliosimple import Twilio, Utils
from datetime import datetime
import logging

from phonetap.main.forms import CallForm
from phonetap.main.models import Call
from phonetap.main.mail import CallMessage

from google.appengine.ext import db
from google.appengine.api import mail

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import simplejson as json

def homepage(request):
	form = CallForm()
	
	return render_to_response('index.html', {
		'form': form,
	})
	
def view_call(request, call_sid):
	call = get_call({ 'CallSid': call_sid })
	
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
			
			twilio = Twilio(settings.TWILIO_ACCOUNT_SID, \
				settings.TWILIO_ACCOUNT_TOKEN)
				
			twilio_response = twilio.call(settings.TWILIO_SANDBOX_NUM, \
				form.cleaned_data['caller_num'], callback)
				
			call = Call(
				call_sid=twilio_response.call_sid,
				caller_number=form.cleaned_data['caller_num'],
				callee_number=form.cleaned_data['callee_num'],
				caller_email=form.cleaned_data['caller_email'],
				current_status='Dialing'
			)
			
			call.put()
			
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
		
def outgoing_callback(request):
	if is_valid_twilio_request(request):
		if request.POST['CallStatus'] == 'completed':
			return HttpResponse(status=200)
			
		call = get_call(request.POST)
			
		call.current_status = 'In Progress'
		call.put()
							
		callback = request.build_absolute_uri(
			reverse('phonetap-main-outgoing_recording')
		)
	
		return render_to_response('outgoing_callback.html', {
			'callback': callback,
			'number': call.callee_number
		})
		
	else:
		return HttpResponse(status=400)
	
def outgoing_recording_callback(request):
	if is_valid_twilio_request(request):
		logging.debug('recording')
		call = get_call(request.POST)
		
		call.current_status = 'Completed'
		call.end_time = datetime.now()
		call.recording_url = request.POST['RecordingUrl']
		call.duration = request.POST['DialCallDuration']
		call.put()

		
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
	#	msg = CallMessage()
#		msg.initialize(call.caller_email, request.build_absolute_uri(
#			reverse('phonetap-main-homepage')
#		))
		
		return render_to_response('outgoing_recording_callback.html', {})
	else:
		return HttpResponse(status=400)
		
		
def get_call(request):
	q = db.GqlQuery('SELECT * FROM Call ' +
					'WHERE call_sid = :1 ',
					request['CallSid'])
	call = q.get()
	
	if not call:
		raise Http404
	return call
	

def is_valid_twilio_request(request):
	if not request.method == 'POST':
		return False

	twilio_utils = Utils(settings.TWILIO_ACCOUNT_SID,
		settings.TWILIO_ACCOUNT_TOKEN)

	postvars = request.POST
	signature = request.META['HTTP_X_TWILIO_SIGNATURE']
	url = request.build_absolute_uri()

	return twilio_utils.validateRequest(url, postvars, signature)
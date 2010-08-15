import json
import phonetap.twiliosimple

from phonetap.main.forms import CallForm

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response

def homepage(request):
	form = CallForm()
	
	return render_to_response('index.html', {
		'form': form,
	})
	
def make_call(request):
	if request.is_ajax():
		form = CallForm(request.POST)
		
		if form.is_valid():
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
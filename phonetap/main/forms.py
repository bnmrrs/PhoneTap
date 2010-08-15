from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField

class CallForm(forms.Form):
	caller_number = USPhoneNumberField()
	callee_number = USPhoneNumberField()
	caller_email = forms.EmailField()
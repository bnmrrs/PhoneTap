from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField

class CallForm(forms.Form):
	caller_num = USPhoneNumberField()
	callee_num = USPhoneNumberField()
	caller_email = forms.EmailField()
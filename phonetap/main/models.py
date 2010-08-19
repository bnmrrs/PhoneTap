from mongoengine import *
from datetime import datetime

class Call(Document):
	call_sid = StringField(required=True)
	caller_number = StringField(required=True)
	callee_number = StringField(required=True)
	caller_email = StringField(required=True)
	recording_url = URLField()
	current_status = StringField(required=True)
	start_time = DateTimeField(required=True, default=datetime.now)
	end_time = DateTimeField()
	recording_duration = IntField()
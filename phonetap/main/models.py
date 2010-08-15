from google.appengine.ext import db

class Call(db.Model):
	caller_number = db.StringProperty(required=True)
	callee_number = db.StringProperty(required=True)
	caller_email = db.EmailProperty(required=True)
	call_sid = db.StringProperty()
	recording_url = db.StringProperty()
	current_status = db.StringProperty()
	start_time = db.DateTimeProperty(auto_now_add=True)
	end_time = db.DateTimeProperty()
	recording_duration = db.IntegerProperty()
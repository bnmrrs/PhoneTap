from google.appengine.api import mail

class CallMessage(mail.EmailMessage):
	def initialize(self, call_url, to):
		self.sender = "app@phonetapapp.appspot.com"
		self.to = to
		self.subject = "PhoneTap - Call Recording"
		self.body = """
		Dear %s,
		
		Your call recording has been processed and is now avaliable.  You can
		now vist %s to listen to and download an .MP3 of your call.
		
		The PhoneTap Team
		""" % (to, call_url)
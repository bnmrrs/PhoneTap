from django import template

def tel(value):
  value = str(value)
  return '(%s) %s-%s' % (value[0:3], value[4:7], value[8:12])

def duration(duration):
	if not duration:
		return 'No duration'
	else:
		return value
	
def listen_to_recording(recording_url):
	if not recording_url:
		return 'No recording was found'
	
def recording_download(recording_url):
	if not recording_url:
		return 'No recording was found'
	else:
		return '<a href="%s">Recording</a>' % (recording_url)

register = template.Library()

register.filter('tel', tel)
register.filter('duration', duration)
register.filter('listen_to_recording', listen_to_recording)
register.filter('recording_download', recording_download)
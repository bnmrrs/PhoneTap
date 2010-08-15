from django import template

def tel(value):
  value = str(value)
  return '(%s) %s-%s' % (value[0:3], value[4:7], value[8:12])

def duration(duration):
	if not duration:
		return 'Unknown duration'
	else:
		return value

register = template.Library()

register.filter('tel', tel)
register.filter('duration', duration)
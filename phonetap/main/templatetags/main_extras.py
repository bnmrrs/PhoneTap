from django import template

def tel(value):
  value = str(value)
  return '(%s) %s-%s' % (value[0:3], value[4:7], value[8:12])

register = template.Library()
register.filter('tel', tel)
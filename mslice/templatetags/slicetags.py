from django import template
register = template.Library()

@register.filter("mongo_id")
def mongo_id(value):
    try:
    	return str(value['_id'])
    except:
    	return "Unknown"

@register.filter("dtype")
def dtype(value):
	try:
		return value.__class__.__name__
	except:
		return "Unknown"
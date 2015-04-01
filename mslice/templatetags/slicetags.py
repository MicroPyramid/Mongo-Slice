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


@register.assignment_tag(takes_context=True)
def get_page(context,page,no_pages):
	if page <= 5:
		start_page = 1
	else:
		start_page = page-5

	if no_pages <= 10:
		end_page = no_pages
	else:
		end_page = start_page + 10
	if end_page > no_pages:
		end_page=no_pages

	pages = range(start_page, end_page+1)
	return pages
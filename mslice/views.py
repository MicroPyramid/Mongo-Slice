import json
import django.shortcuts.render_to_response

def index(request):
    if request.method == "POST":
        # we need to check auth status here then render index page

        return render_to_response('index.html')
    else:
        return render_to_response('login.html')


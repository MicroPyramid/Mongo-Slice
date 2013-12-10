
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import httpResponseRedirect

def index(request):
    if request.method == "POST":
        # we need to check auth status here then render index page

        return render_to_response('index.html')
    else:
        return render_to_response('login.html')

def mlogout(request):
    logout(request)
    return httpResponseRedirect('/')


from django.shortcuts import render_to_response
from django.http import HttpResponse
import json



def index(request):

    if request.method == "POST":
        from mpcomp.views import mongoauth
        db = mongoauth(request.POST.get('host'), request.POST.get('port'), request.POST.get('db'), request.POST.get('uid'), request.POST.get('pwd'))
        if not db:
            data = {'login':False}
            return HttpResponse(json.dumps(data))

        else:
            request.session['host']=request.POST.get('host')
            request.session['port']=request.POST.get('port')
            request.session['db']=request.POST.get('db')
            request.session['uid']=request.POST.get('uid')
            request.session['pwd']=request.POST.get('pwd')
            request.session['login']=True

            data = {'login':True}
            return HttpResponse(json.dumps(data))

    elif 'login' in request.session:
        return render_to_response('index.html')

    else:
        return render_to_response('login.html')



def mlogout(request):
    from django.http import HttpResponseRedirect
    request.session.flush()
    return HttpResponseRedirect('/')


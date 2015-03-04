from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import Connection
import json
def index(request):
    if request.method == "POST":
        from mpcomp.views import mongoauth
        db = mongoauth(request.POST.get('host'), request.POST.get('port'), request.POST.get('db'), request.POST.get('uid'), request.POST.get('pwd'))
        if not db:
            data = {'login':False}
            return HttpResponse(json.dumps(data))

        else:        #Return a list of collections in 'testdb1'

            request.session['host']=request.POST.get('host')
            request.session['port']=request.POST.get('port')
            request.session['db']=request.POST.get('db')
            request.session['uid']=request.POST.get('uid')
            request.session['pwd']=request.POST.get('pwd')
            request.session['login']=True

            data = {'login':True}
            return HttpResponse(json.dumps(data))

    elif 'login' in request.session:
        ctx = {}
        
        connection = Connection(request.session['host'], int(request.session['port'])) #Connect to mongodb
        db = connection[request.session['db']]   
        #print db.collection_names()   #equal to: > use testdb1
        ctx['collections'] = db.collection_names()
        ctx['db'] = request.session['db']
        return render_to_response('index.html',ctx)

    else:
        return render_to_response('login.html')

def mlogout(request):
    from django.http import HttpResponseRedirect
    request.session.flush()
    return HttpResponseRedirect('/')

def info(request,coll_name):
    print coll_name
    ctxc = {}
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    ctxc['count']=db[coll_name].count()
    ctxc['documents'] = list(db[coll_name].find())
    print list(db[coll_name].find())
    #ctxc['collstats'] = db.command("collstats", coll_name)
    ctxc['collections'] = db.collection_names()
    ctxc['db'] = request.session['db']   
    ctxc['name'] = coll_name
    return render_to_response('index.html',ctxc)

def insert_doc(request):
    if request.method == 'GET':
        return render_to_response('index.html')
    print request.POST.get('ta')
    query=request.POST.get('ta')
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    print connection.db.studentdetails.insert({'author':'mike'})  
    return render_to_response('index.html')

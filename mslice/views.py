from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import Connection
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import re
import os


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
    
        ctx = {}
        connection = Connection(request.session['host'], int(request.session['port'])) #Connect to mongodb
        db = connection[request.session['db']]   
        ctx['collections'] = db.collection_names()
        ctx['db'] = request.session['db']
        return render_to_response('wireframe_robo.html',ctx)

    else:
        c={}
        c.update(csrf(request))
        return render_to_response('login.html',{'csrf_token':c['csrf_token']})


def mlogout(request):
    from django.http import HttpResponseRedirect
    request.session.flush()
    return HttpResponseRedirect('/')


def info(request,coll_name):
    content = {}
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    content['count']=db[coll_name].count()
    content['documents'] = list(db[coll_name].find())
    content['collstats'] = db.command("collstats", coll_name)
    content['collections'] = db.collection_names()
    content['db'] = request.session['db']   
    content['name'] = coll_name
    content['read'] = True
    print content['documents']
    #db[coll_name].insert({'Name':'Charan','College':'SNIST'})
    return render_to_response('wireframe_robo.html',content)

@csrf_exempt
def insert_doc(request):
    if request.method == 'GET':
        c={}
        c.update(csrf(request))
        return render_to_response('wireframe_robo.html',{'csrf_token':c['csrf_token']})
    content = {}
    coll_name = request.POST.get('collection')  
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    content['count']=db[coll_name].count()
    content['documents'] = list(db[coll_name].find())
    content['collstats'] = db.command("collstats", coll_name)
    content['collections'] = db.collection_names()
    content['db'] = request.session['db']   
    content['name'] = coll_name
    query=request.POST.get('ta')

    try:
        c = db[query.split('.')[1]]

    except:
        c = db.createCollection(query.split('.')[1])

    #exec(query)

    q = query
    m=re.search("({.*})",q)
    d =m.group(0)
    res = os.system('mongo' + db.name + '--eval' + "printjson(" + q + ")"'')
    print res
    try:    
        if 'insert' in q:
            d= ast.literal_eval(d)
            try:
                resp = c.save(d)
            except InvalidSyntax:
                exec(q)
        if 'remove' in q:
            d= ast.literal_eval(d)
            resp = c.remove(d)
    except:
        if q.startswith('db'):
            res = os.system('mongo slice --eval' + "printjson(" + q + ")"'')
            #exec(q)
        else:
            resp = "Please Enter Valid MongoDB Query"

    return render_to_response('wireframe_robo.html',content)


def wireframe_robo(request):
    return render_to_response('wireframe_robo.html')


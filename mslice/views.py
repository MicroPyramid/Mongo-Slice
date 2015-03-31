from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import Connection
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from mpcomp.views import mongoauth
from bson.json_util import dumps
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
    content['connection'] = connection
    content['coll_name'] = coll_name
    
    #db[coll_name].insert({'Name':'Charan','College':'SNIST'})
    return render_to_response('wireframe_robo.html',content)

@csrf_exempt
def query_process(request):
    content = {}
    coll_name = request.POST.get('collection')  
    connection = Connection(request.session['host'], int(request.session['port']))
    db = connection[request.session['db']]
    content['collections'] = db.collection_names()
    content['db'] = request.session['db']   
    content['connection'] = connection

    if request.method == 'GET':
        c={}
        c.update(csrf(request))
        return render_to_response('wireframe_robo.html',{'csrf_token':c['csrf_token'], 'content':content})
    
    q = request.POST.get('ta')
    if not q.startswith('db'):
        resp = 'Please Enter Valid Query:'
        return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})

    m=re.search("({.*})",q)
    if m == None :
        d = None
    else:
        d=m.group(0)
    resp = None
    
    try:

        if 'insert' in q:
            print 'inser'
        
            try:
                c = db[q.split('.')[1]]
            except:
                c = db.createCollection(q.split('.')[1])
            
            # if not d:
            #     return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})
            
            try:
                d= ast.literal_eval(d)
            except (SyntaxError, TypeError, ValueError, NameError):
                resp = 'Please Enter Valid Query'
                return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})

            # try:
            #     resp = c.save(d)
            # except SyntaxError:
            #     #exec(q)
            resp = c.save(d)
            return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content}) 
        
        if 'remove' in q:
            print 'removexxxxxxxxxxxxxxxxxxx'
            try:
                c = db[q.split('.')[1]]
            except:
                pass

            try:
                d= ast.literal_eval(d)
            except (SyntaxError, TypeError, ValueError, NameError):
                resp = 'Please Enter valid Query'
                return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})           
            print d
            resp = c.remove(d)
            resp = 'Document ' + str(d) + ' removed' 
            return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})
        
        if 'update' in q:
            try:
                c = db[q.split('.')[1]]
            except:
                pass

            try:
                d= ast.literal_eval(d)
            except (SyntaxError, TypeError, ValueError, NameError):
                return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})
            
            resp = c.update( d[0], d[1])
            resp = 'Document Updated'
            return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})
        
        if 'find' in q:
            c = db[q.split('.')[1]]
            if d:
                d = ast.literal_eval(d)

                if c is None:
                    resp =  'Collection not found'
                else:
                    if 'findOne' in q: 
                        resp = dumps(c.find_one(d))
                        resp = dumps(resp)
                    else:
                        resp = c.find(d)
                        resp = dumps(resp)

                    return render_to_response('wireframe_robo.html',{'documents':resp, 'content':content})
            resp = dumps(c.find())
            print 'ok'
            return render_to_response('wireframe_robo.html',{'documents':resp, 'content':content})

    except:
        return render_to_response('wireframe_robo.html',{'resp':resp, 'content':content})

    #exec(query)

    # q = query
    # m=re.search("({.*})",q)
    # d =m.group(0)
    # res = os.system('mongo' + db.name + '--eval' + "printjson(" + q + ")"'')
    # print res
    # try:    
    #     if 'insert' in q:
    #         d= ast.literal_eval(d)
    #         try:
    #             resp = c.save(d)
    #         except InvalidSyntax:
    #             exec(q)
    #     if 'remove' in q:
    #         d= ast.literal_eval(d)
    #         resp = c.remove(d)
    # except:
    #     if q.startswith('db'):
    #         res = os.system('mongo slice --eval' + "printjson(" + q + ")"'')
    #         #exec(q)
    #     else:
    #         resp = "Please Enter Valid MongoDB Query"

    # return render_to_response('wireframe_robo.html',content)






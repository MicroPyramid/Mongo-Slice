from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from bson.json_util import dumps
import json
import ast
import re
from mpcomp.views import getConn, mongoauth
import math


def index(request):
    if request.method == "POST":
        db = mongoauth(request.POST.get('host'), request.POST.get('port'), request.POST.get('db'), request.POST.get('uid'), request.POST.get('pwd'))

        if not db:
            data = {'login': False}
            return HttpResponse(json.dumps(data))

        else:
            request.session['host'] = request.POST.get('host')
            request.session['port'] = request.POST.get('port')
            request.session['db'] = request.POST.get('db')
            request.session['uid'] = request.POST.get('uid')
            request.session['pwd'] = request.POST.get('pwd')
            request.session['login'] = True
            data = {'login': True}
            return HttpResponse(json.dumps(data))

    elif 'login' in request.session:
        content = {}
        db = getConn(request)
        content['collections'] = db.collection_names()
        content['request'] = request
        return render_to_response('home.html', content)

    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', {'csrf_token': c['csrf_token']})


def mlogout(request):
    from django.http import HttpResponseRedirect
    request.session.flush()
    return HttpResponseRedirect('/')


def info(request, coll_name):
    content = {}
    db = getConn(request)

    # db = connection[request.session['db']]
    items_per_page = 10
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(db[coll_name].find().count()) / items_per_page))

    content = {
        'count': db[coll_name].count(),
        'documents': list(db[coll_name].find())[(page - 1) * items_per_page:page * items_per_page],
        'collstats': db.command("collstats", coll_name),
        'collections': db.collection_names(),
        'db': request.session['db'],
        'name': coll_name,
        'read': True,
        'coll_name': coll_name,
        'dbstats': db.command("dbstats"),
        'current_page': page,
        'last_page': no_pages,
        'request': request,
    }
    return render_to_response('home.html', content)


@csrf_exempt
def query_process(request):
    content = {}
    coll_name = request.POST.get('collection')
    # db = connection[request.session['db']]
    db = getConn(request)
    content = {
        'collections': db.collection_names(),
        'db': request.session['db'],
        'request': request,
    }
    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        return render_to_response('home.html', {'csrf_token': c['csrf_token'], 'request': request, 'content': content})

    q = request.POST.get('ta')
    if not q.startswith('db'):
        resp = 'Please Enter Valid Query:'
        return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})

    m = re.search("({.*})", q)
    if m is None:
        d = None
    else:
        d = m.group(0)
    resp = None

    try:

        if 'insert' in q:

            try:
                c = db[q.split('.')[1]]
            except Exception as e:
                c = db.createCollection(q.split('.')[1])
            try:
                d = ast.literal_eval(d)
                resp = c.save(d)
                resp = 'Status: Document Inserted Succesfully ' + str(resp)
            except (SyntaxError, TypeError, ValueError, NameError):
                resp = 'Please Enter Valid Query'
            return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})
        if 'remove' in q:
            try:
                c = db[q.split('.')[1]]
            except Exception as e:
                pass
            if d is None:
                c.remove()
                resp = 'Status: Documents Removed Succesfully'
                return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})
            try:
                d = ast.literal_eval(d)
                resp = c.remove(d)
                resp = 'Status: ' + str(resp)
            except (SyntaxError, TypeError, ValueError, NameError):
                resp = 'Please Enter valid Query'
            return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})
        if 'update' in q:
            try:
                c = db[q.split('.')[1]]
            except Exception as e:
                pass

            try:
                d = ast.literal_eval(d)
                resp = c.update(d[0], {'$set': d[1]})
                resp = 'Status: ' + str(resp)
            except (SyntaxError, TypeError, ValueError, NameError):
                resp = "Please Enter valid Query"

            return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})

        if 'find' in q:
            c = db[q.split('.')[1]]
            if d:
                d = ast.literal_eval(d)

                if c is None:
                    resp = 'Collection not found'
                else:
                    if 'findOne' in q:
                        resp = dumps(c.find_one(d))
                        resp = list(resp)
                    else:
                        resp = c.find(d)

                        resp = list(resp)

                    return render_to_response('home.html', {'documents': resp, 'request': request, 'coll_name': c.name, 'content': content})
            resp = list(c.find())
            return render_to_response('home.html', {'documents': resp, 'request': request, 'coll_name': c.name, 'content': content})

        if 'drop' in q:
            try:
                c = db[q.split('.')[1]]
                c.drop()
                resp = "Status: Collection Dropped Succesfully"
            except Exception as e:
                resp = "Please Enter Valid Collection Name or Query"
            return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})
        resp = "'Please Enter valid Query'"
        return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})

    except Exception as e:
        return render_to_response('home.html', {'resp': resp, 'request': request, 'content': content})

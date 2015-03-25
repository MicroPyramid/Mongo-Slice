from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'mslice.views.index'),
    url(r'^logout/$', 'mslice.views.mlogout'),
    url(r'^info/(?P<coll_name>[a-zA-Z0-9_-]+)/$', 'mslice.views.info'),
	url(r'^operations/$','mslice.views.insert_doc'),
	url(r'^wireframe/$','mslice.views.wireframe'),
    url(r'^wireframe_robo/$', 'mslice.views.wireframe_robo')
)
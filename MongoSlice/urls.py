from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'mslice.views.index'),
    url(r'^logout/$', 'mslice.views.mlogout'),
    url(r'^info/(?P<coll_name>[a-zA-Z0-9_-]+)/$', 'mslice.views.info'),
    url(r'^query-process/$', 'mslice.views.query_process'),
)

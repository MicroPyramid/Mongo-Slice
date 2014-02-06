from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'mslice.views.index'),
    url(r'^logout/$', 'mslice.views.mlogout'),
)

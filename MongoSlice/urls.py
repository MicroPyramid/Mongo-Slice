from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'mscice.views.index'),
)

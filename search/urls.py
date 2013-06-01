from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/detail/$', views.DetailView.as_view(), name='detail')
)
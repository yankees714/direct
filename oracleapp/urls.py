from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

from search import views

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #to repopulate the database
    url(r'^repopulate/', views.RepopView, name='repopulate'),

    #for search views
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^info/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)

handler404 = 'views.handler404'
handler500 = 'views.handler500'
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', 'gameshow.views.home', name='home'),
                       # url(r'^gameshow/', include('gameshow.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       url(r'^buzzer/', include('buzzer.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
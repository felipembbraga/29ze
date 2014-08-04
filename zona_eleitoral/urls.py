from django.conf.urls import patterns, include, url
from django.contrib import admin
from utils import custom_admin
from views import home
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zona_eleitoral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', home),
    url(r'^home/$', home, name='home'),
    url(r'^core/', include('core.urls', app_name='core')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^custom_admin/', include(custom_admin.site.urls)),
    url(r'^eleicao/', include('eleicao.urls', app_name='eleicao')),
)

from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list_files/$', views.list_files, name='list_files'),
    url(r'^delete_files/$', views.delete_files, name='delete_files'),
    url(r'^ftp_files/$', views.ftp_files, name='ftp_files'),
    url(r'^scp_files/$', views.scp_files, name='scp_files'),
    url(r'^rename_files/$', views.rename_files, name='rename_files'),
    url(r'^save/$', views.save, name='save'),
    url(r'^cache_list/$', views.cache_list, name='cache_list'),
    url(r'^read_cache/$', views.read_cache, name='read_cache'),
]

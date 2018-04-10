from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^terminal-stream', views.terminal_stream, name='terminal_stream'),
]

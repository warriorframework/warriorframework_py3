from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WappStoreView.as_view(), name='wappstore'),
    url(r'^expand_wapp$', views.expand_wapp, name='expand_wapp'),
    url(r'^install_terminal_app', views.install_terminal_app, name='install_terminal_app'),
]

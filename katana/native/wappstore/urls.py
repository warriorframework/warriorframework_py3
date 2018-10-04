from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WappStoreView.as_view(), name='wappstore'),
    url(r'^expand_wapp/$', views.expand_wapp, name='expand_wapp'),
    url(r'^install_app', views.install_app, name='install_app'),
    url(r'^go_to_account', views.go_to_account, name='go_to_account'),
    url(r'^go_to_home_page/', views.go_to_home_page, name='go_to_home_page'),
    url(r'^see_more_wapps/', views.see_more_wapps, name='see_more_wapps'),
]

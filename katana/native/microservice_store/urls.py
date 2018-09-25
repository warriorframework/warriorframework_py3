from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'deploy', views.deploy, name='deploy'),
    url(r'load', views.load, name='load'),
    url(r'save', views.save, name='save'),
    url(r'get_dir_path', views.get_dir_path, name='get_dir_path'),
]

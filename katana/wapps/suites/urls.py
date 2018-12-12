from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SuitesView.as_view(), name='index'),
    url(r'^get_list_of_suites/$', views.get_list_of_suites, name='get_list_of_suites'),
    url(r'^get_file/$', views.get_file, name='get_file'),
    url(r'^save_file/$', views.save_file, name='save_file'),
]

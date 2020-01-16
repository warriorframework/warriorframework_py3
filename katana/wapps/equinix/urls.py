from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EquinixView.as_view(), name='index'),
    url(r'^set/$', views.set_api, name='set_api'),
    url(r'^measure/$', views.measure_api, name='measure_api'),
]

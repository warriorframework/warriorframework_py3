from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.KwSequencerIndex.as_view(), name='index'),
    url(r'^create_new_kw/$', views.KwSequencerCreate.as_view(), name='create_new_kw'),
    url(r'^create_new_subkw/$', views.create_new_subkw, name='create_new_subkw'),
]

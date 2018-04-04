from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.KwSequencerIndex.as_view(), name='index')
]

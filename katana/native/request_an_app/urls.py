from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RequestAnAppView.as_view(), name='request_an_app'),
]

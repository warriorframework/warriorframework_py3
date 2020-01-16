"""katana.wui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^katana/', include('katana.wui.core.urls')),
    url(r'^$', RedirectView.as_view(url='/katana/')),
    # url(r'^katana/settings/', include('katana.native.settings.urls')),
    # url(r'^katana/wapp_management/', include('katana.native.wapp_management.urls')),
    # url(r'^katana/wappstore/', include('katana.native.wappstore.urls')),
    # url(r'^katana/microservice_store/', include('katana.native.microservice_store.urls')),
    # url(r'^katana/assembler/', include('katana.wapps.assembler.urls')),
    # url(r'^katana/cli_data/', include('katana.wapps.cli_data.urls')),
    # url(r'^katana/suites/', include('katana.wapps.suites.urls')),
    # url(r'^katana/cases/', include('katana.wapps.cases.urls')),
    # url(r'^katana/wdf/', include('katana.wapps.wdf_edit.urls')),
    # url(r'^katana/execution/', include('katana.wapps.execution.urls')),
    # url(r'^katana/projects/', include('katana.wapps.projects.urls')),
    # url(r'^katana/testwrapper/', include('katana.wapps.testwrapper.urls')),
      url(r'^katana/equinix/', include('katana.wapps.equinix.urls')),
]

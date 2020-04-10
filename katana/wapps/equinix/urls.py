from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EquinixView.as_view(), name='index'),
    url(r'^set/$', views.set_api, name='set_api'),
    url(r'^measure/$', views.measure_api, name='measure_api'),
    url(r'^add_new_group/$', views.add_group, name='add_group'),
    url(r'^get_group_list/$', views.get_group_list, name='get_group_list'),
    url(r'^fetch_group_details/$', views.fetch_group_details, name='fetch_group_details'),
    url(r'^edit_group/$', views.edit_group, name='edit_group'),
    url(r'^add_transponder/$', views.add_transponder, name='add_transponder'),
    url(r'^add_ops/$', views.add_ops, name='add_ops'),
    url(r'^fetch_devices/$', views.fetch_devices, name='fetch_devices'),
    url(r'^get_device_details/$', views.get_device_details, name='get_device_details'),
    url(r'^edit_transponder/$', views.edit_transponder, name='edit_transponder'),
    url(r'^edit_ops/$', views.edit_ops, name='edit_ops'),
    url(r'^get_list_of_transponders/$', views.get_list_of_transponders, name='ediget_list_of_transponderst_ops'),
    url(r'^get_list_of_ops/$', views.get_list_of_ops, name='get_list_of_ops'),
    url(r'^fetch_all_groups/$', views.fetch_all_groups, name='fetch_all_groups'),
    url(r'^delete_group/$', views.delete_group, name='delete_group'),
    url(r'^fetch_devices_details_for_table/$', views.fetch_devices_details_for_table, name='fetch_devices_details_for_table'),
    url(r'^delete_device/$', views.delete_device, name='delete_device'),
    
]

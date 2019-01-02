from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'^accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # url(r'^accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # url(r'^accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^accounts/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_complete'),
    url(r'^get_file_explorer_data/$', views.getFileExplorerData.as_view(), name='get_file_explorer_data'),
    url(r'^read_config_file/$', views.read_config_file, name='read_config_file'),
    url(r'^check_if_file_exists/$', views.check_if_file_exists, name='check_if_file_exists'),
    url(r'^refresh_landing_page/$', views.refresh_landing_page, name='refresh_landing_page'),
]

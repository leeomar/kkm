from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from kekemen.account import views as account_view
from django.contrib.auth import views as auth_views
from registration.views import activate
from django.views.generic.simple import direct_to_template
from registration.views import register

urlpatterns = patterns('',
    # Examples:
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^activate/(?P<activation_key>\w+)/$', activate, { 'backend': 'registration.backends.default.DefaultBackend' }, name='registration_activate'),
    url(r'^activate/(?P<activation_key>\w+)/$', account_view.auth_activate, name='registration_activate'),
    #url(r'^register/$', register, { 'backend': 'registration.backends.default.DefaultBackend' }, name='registration_register'),
    url(r'^register/$', account_view.auth_register, name='registration_register'),
    url(r'^register/complete/$', direct_to_template, { 'template': 'registration/registration_complete.html' }, name='registration_complete'),
    url(r'^register/closed/$', direct_to_template, { 'template': 'registration/registration_closed.html' }, name='registration_disallowed'),
    url(r'^login/$', account_view.auth_login, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
)

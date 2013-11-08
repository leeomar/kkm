from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kuaidian.diancan.views.index'),
    # url(r'^kuaidian/', include('kuaidian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/clear_cache/$', 'diancan.views.clear_cache'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/list_order/$', 'diancan.views.list_order'),
    url(r'^order/confirm-order/$', 'diancan.views.confirm_order'),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'kuaidian/template/login.html'}),
    url(r'^user/register/$', 'diancan.views.register'),
    url(r'^user/modifyinfo/$', 'diancan.views.modify_contact_info'),
    url(r'^user/login/$', 'diancan.views.login'),
    url(r'^user/logout/$', 'diancan.views.logout'),
    url(r'^product/(?P<regionID>\d+)/list/$', 'diancan.views.show_product'),
    url(r'^common/help$', direct_to_template, { 'template': 'article/help.html' }, 'help'),
    url(r'^common/gift$', direct_to_template, { 'template': 'article/gift.html' }, 'gift'),
    # Static
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/lijian/tuanzz/kuaidian/kuaidian/static/'}),
)

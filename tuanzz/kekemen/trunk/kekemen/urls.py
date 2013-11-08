from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kekemen.views.home', name='home'),
    # url(r'^kekemen/', include('kekemen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^$', direct_to_template, { 'template': 'index.html' }, 'index'),
    url(r'^$', 'views.home.home', name='index'),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('kekemen.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shop/(?P<shopID>\d+)/$', 'views.shop.shop'),
    url(r'^shop/(?P<shopID>\d+)/menu/(?P<menuID>\d+)/$', 'views.shop.getDishByMenu'),
    url(r'^shop/customer/$', 'views.shop.getCustomer'),
    url(r'^action/(?P<action>.*)/(?P<dishID>\d+)/$', 'views.shop.action'),
    url(r'^home/', 'views.home.home'),
    url(r'^search/', 'views.search.search'),
    url(r'^info/search/', 'views.search.search_info'),
    url(r'^ajax/hot/', 'views.index.getHotDish'),
    url(r'^ajax/new/', 'views.index.getNewDish'),
    url(r'^ajax/pop/', 'views.index.getPopFollowing'),
    url(r'^ajax/wall/', 'views.index.getNewDish'),
    url(r'^ajax/feed/$', 'views.index.getFeed'),
    url(r'^ajax/twitter/$', 'views.index.getTwitter'),
    url(r'^comment/add/', 'views.shop.addComment'),
    url(r'^comment/get/', 'views.shop.getComment'),
    url(r'^friend/comment/get/', 'views.shop.getFriendComment'),
    url(r'^follow/(?P<userID>\d+)/$', 'views.index.follow'),
    url(r'^unfollow/(?P<userID>\d+)/$', 'views.index.unfollow'),
    url(r'^order/new/', 'views.order.new'),
    url(r'^order/add/dish/', 'views.order.addItem'),
    url(r'^order/get/', 'views.order.getOrderInfo'),
    url(r'^order/confirm/', 'views.order.confirm'),
    url(r'^order/list/$', 'views.order.list'),
    url(r'order/view/(?P<orderID>.+)/$', 'views.order.view'),
    url(r'^chat/get/', 'views.order.getChat'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'media').replace('\\','/')}),
    url(r'^user/(?P<userID>\d+)/$', 'views.user.home'),
    url(r'^confirm/(?P<orderID>.+)/$', 'views.confirm.confirmShop'),
    url(r'^confirm_action/(?P<orderID>.+)/$', 'views.confirm.confirmForm'),
    url(r'^fresh/(?P<orderID>.+)/$', 'views.confirm.fresh'),
    url(r'^user/(?P<userID>\d+)/follower/$', 'views.user.getFollower'),
    url(r'^user/(?P<userID>\d+)/following/$', 'views.user.getFollowing'),
    url(r'^invite/(?P<orderID>.+)/$', 'views.order.invite'),
    url(r'^test/', 'views.order.test'), 
    url(r'^image/save', 'views.order.save_image'),
    url(r'^newest/comment/$', 'views.shop.newest'),
)


# coding : utf-8

#from django.test import TestCase
from kekemen.Biz import *
from sns.constant import *
import datetime

ts = datetime.datetime.now()

class UserBizTest():
    def __init__(self):
        self.userBiz = UserBiz()

    def init_date():
        region = Region(name = 'wuhan', createTime = ts)
        region.save()

        user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user1.save()
        profile1 = Profile(phone = '13482131096', picture = '1.jpg', region = region, user = user1)
        profile1.save()

        user2 = User.objects.create_user('Tina', 'tina@thebeatles.com', 'tinapassword')
        user2.save()
        profile2 = Profile(phone = '13288979678', picture = '2.jpg', region = region, user = user2)
        profile2.save()

    def test_get_basic_profile(self, userid = 2):
        print 'test get basic profile'
        print self.userBiz.getBasicProfile( userid )

    def test_get_profile(self, userid = 2):
        print 'test get profile'
        print self.userBiz.getProfile( userid )

class FollowBizTest():
    def __init__(self):
        self.followBiz = FollowBiz()

    def test_following(self, userid, followingid):
        print 'test add following'
        self.followBiz.following(userid, followingid)

    def test_get_follower(self, userid ):
        print 'test get follower'
        print self.followBiz.getFollower(userid)

    def test_get_following(self, userid ):
        print 'test get following'
        print self.followBiz.getFollowing(userid)

class FeedBizTest():
    def __init__(self):
        self.feedBiz = FeedBiz()

    def test_add_feed(self, userid):
        print 'FeedBizTest.test_add_feed()'
        res = self.feedBiz.addFeed(userid, ts, \
                CONSTANT_FEED_TYPE_COMMENT, CONSTANT_FEED_FROM_WEB, \
                'new test feed')

    def test_get_his_feed(self, userid):
        print 'FeedBizTest.test_getHisFeed()'
        feeds = self.feedBiz.getHisFeed(userid, datetime.datetime.now())
        print 'feeds ', feeds
        for feed in feeds:
            print feed

class OrderBizTest():
    orderBiz = OrderBiz()

    def test_new_order(self):
        oid = OrderBizTest.orderBiz.newOrder( 1, ts)
        for i in range(1, 5):
            OrderBizTest.orderBiz.addItem(oid, i, 8, 1, i)

        OrderBizTest.orderBiz.updateItem(oid, 3, 5)
        OrderBizTest.orderBiz.delItem(oid, 4)

        for j in range(223, 226):
            OrderBizTest.orderBiz.addMember(oid, j)

        OrderBizTest.orderBiz.confirmOrder(oid, ts, 3, 1, 'lee', 1, 13456789876, 1, 'no remark')

        print OrderBizTest.orderBiz.getSingleOrder(oid)

def print_line(msg):
    print '-------------------------------------------'
    print msg

class DishBizTest():
    def __init__(self):
        self.dishBiz = DishBiz()

    def test_get_dish(self, dishID):
        print_line('test get dish')
        print self.dishBiz.getDish(dishID)

    def test_get_hot_dish(self, regionID):
        print_line('test get hot dish')
        print self.dishBiz.getHotDishes( regionID )

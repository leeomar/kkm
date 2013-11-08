#!/usr/bin/python
# -*- coding: utf-8 -*-
from kekemen.biz.relation import *
import datetime


class FollowBizTest:

    def test_follow(self, userID1, userID2):
        assert FollowBiz.follow(userID1, userID2)

    def test_unfollow(self, userID1, userID2):
        assert FollowBiz.unfollow(userID1, userID2)

    def test_get_following(self, userID):
        following = FollowBiz.getFollowing(userID)
        print following
        assert len(following) > 0

    def test_get_follower(self, userID):
        follower = FollowBiz.getFollower(userID)
        print follower
        assert len(follower) > 0

    def test_get_pop_following(self):
        popFollowing = FollowBiz.getPopFollowing()
        print popFollowing
        assert len(popFollowing) > 0

    def test_suite(self, userID1, userID2):
        self.test_follow(userID1, userID2)
        self.test_get_following(userID1)
        self.test_get_follower(userID2)
        self.test_get_pop_following()
        self.test_unfollow(userID1, userID2)


def console(msg):
    print '-----------------------------------'
    for item in msg:
        print item


class FeedBizTest:

    def test_add(userID):
        ts = datetime.datetime.now()
        FeedBiz.add(userID, ts, 1, 1, 'i love feed')
        console('add feed')

    def test_get(userID):
        ts = datetime.datetime.now()
        feeds = FeedBiz.getHisFeed(userID, ts)
        console(('get feed', feeds))


from kekemen.biz.comment import VoteBiz


class VoteBizTest:

    def test_like(self, dishID, userID):
        ret = VoteBiz.like(dishID, userID)
        assert ret == True
        console(('VoteBiz test like', ))

    def test_eat(self, dishID, userID):
        ret = VoteBiz.eat(dishID, userID)
        console(('VoteBiz test eat', ))

    def test_comment(self, dishID, userID):
        ret = VoteBiz.comment(dishID, userID)
        console(('VoteBiz test comment', ))

    def test_want(self, dishID, userID):
        ret = VoteBiz.want(dishID, userID)
        console(('VoteBiz test want', ))

    def test_suite(self, dishID, userID):
        self.test_like(dishID, userID)
        self.test_eat(dishID, userID)
        self.test_want(dishID, userID)
        self.test_comment(dishID, userID)


from kekemen.biz.comment import CommentBiz


class CommentBizTest:

    def test_add(self, userID, goodID):
        ts = datetime.datetime.now()
        CommentBiz.add(userID, goodID, '', 'this is delicious', ts)
        console(('ComentBiz test add', ))

    def test_get(self, goodID):
        ts = datetime.datetime.now()
        comments = CommentBiz.get(goodID, ts)
        console(('CommentBiz test get', comments))

    def test_get_friend_comment(self, goodID, userID):
        ts = datetime.datetime.now()
        comments = CommentBiz.getFriendComment(goodID, userID, ts)
        console(('CommentBiz test get friend comments', comments))

    def test_suite(self, userID, goodID):
        self.test_add(userID, goodID)
        self.test_get(goodID)


from kekemen.biz.feed import FeedBiz


class FeedBizTest:

    def test_add(self, userID):
        ts = datetime.datetime.now()
        ret = FeedBiz.add(userID, ts, 1, 1, 'my first share')
        assert ret == True
        console(('FeedBizTest test add', ))

    def test_get(self, userID):
        ts = datetime.datetime.now()
        feeds = FeedBiz.get(userID, ts)
        console(('FeedBizTest test get ', feeds))

    def test_suite(self, userID):
        self.test_add(userID)
        self.test_get(userID)


from kekemen.biz.shop import DishBiz


class DishBizTest:

    def test_get_dish(self, dishID):
        dish = DishBiz.getDish(dishID)
        console(('DishBizTest test get dish', dish))

    def test_get_new_dish(self, regionID):
        dishes = DishBiz.getNewDishes(regionID)
        console(('DishBizTest test get new dishes', dishes))

    def test_get_hot_dish(self, regionID):
        dishes = DishBiz.getHotDishes(regionID)
        console(('DishBizTest test get hot dishes', dishes))

    def test_get_by_menu(self, shopID, menuID):
        dishes = DishBiz.getByMenu(shopID, menuID)
        console(('DishBizTest test get by menu', dishes))

    def test_get_dish_statistic(self, dishID):
        info = DishBiz.getDishStatistic(dishID)
        console(('DishBizTest test get statistic', info))

    def test_search(self, kw):
        pass

    def test_suite(
        self,
        dishID,
        regionID,
        shopID,
        menuID,
        ):
        self.test_get_dish(dishID)
        self.test_get_dish_statistic(dishID)
        self.test_get_by_menu(shopID, menuID)
        self.test_get_new_dish(regionID)
        self.test_get_hot_dish(regionID)


from kekemen.biz.order import OrderBiz


class OrderBizTest:

    def test_add(self, userID, shopID):
        ts = datetime.datetime.now()
        oid = OrderBiz.add(userID, shopID, ts)
        console(('OrderBizTest test add', oid))
        return oid

    def test_addItem(
        self,
        orderID,
        goodID,
        amount,
        userID,
        ):
        OrderBiz.addItem(orderID, goodID, amount, userID)
        console(('OrderBizTest test add item', orderID))

    def test_update(
        self,
        orderID,
        goodID,
        amount,
        userID,
        ):
        OrderBiz.updateItem(orderID, goodID, amount, userID)
        console(('OrderBizTest test update item', ))

    def test_delItem(
        self,
        orderID,
        goodID,
        userID,
        ):
        OrderBiz.delItem(orderID, goodID, userID)
        console(('OrderBizTest test del item', ))

    def test_add_member(self, orderID, userID):
        OrderBiz.addMember(orderID, userID)
        console(('OrderBizTest test add member', ))

    def test_confirm(self, orderID):
        ts = datetime.datetime.now()
        OrderBiz.confirm(
            orderID,
            ts,
            3,
            1,
            'Mr ass',
            5001,
            13245678967,
            1,
            'no words',
            )
        console(('OrderBizTest test confirm ', ))

    def test_get(self, orderID):
        order = OrderBiz.get(orderID)
        console(('OrderBizTest test get ', orderID, order))
        detail = OrderBiz.get(orderID, True)
        console(('OrderBizTest test get detail ', orderID, detail))

    def test_suite(self):
        oid = self.test_add(1, 1)
        self.test_addItem(oid, 1, 1, 1)
        self.test_addItem(oid, 1, 2, 1)

        self.test_update(oid, 1, 2, 4)
        self.test_delItem(oid, 2, 1)

        self.test_add_member(oid, 4)
        self.test_add_member(oid, 7)

        self.test_confirm(oid)
        self.test_get(oid)


from kekemen.biz.shop import ShopBiz


class ShopBizTest:

    def test_search(self, keyword):
        ShopBiz.search(keyword)

    def test_suite(self):
        self.test_search('KFC')



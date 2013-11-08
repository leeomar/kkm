#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding : utf-8

from kekemen.biz.commons import *
from kekemen.biz.shop import ShopBiz, DishBiz
from django.core.exceptions import ObjectDoesNotExist
from kekemen.biz.relation import UserBiz
from kekemen.sns.constant import *


class OrderBiz:

    @staticmethod
    def addEvaluate(orderID):
        OrderMongoDAO.addEvaluate(orderID)

    @staticmethod
    def getEvaluate(orderID_list):
        count = 0
        if len(orderID_list) == 0 :
            return count

        for orderID in orderID_list:
            ev = OrderMongoDAO.getEvaluate(orderID)
            if ev == 0:
                count += 1
        return count

    @staticmethod
    def add(userID, shopID, createTime):
        try:
            shop = ShopBiz.get(shopID)
            return OrderMongoDAO.add(userID, shopID, shop.name,
                    createTime)
        except ObjectDoesNotExist, err:
            raise IllegalParamException('shopID', shopID,
                    'shop not exist ')

    @staticmethod
    def allowModify(orderID):
        status = OrderMongoDAO.getStatus(orderID)

        # if not status:
        #    raise IllegalParamException('orderID', orderID, 'order not exist')

        if status is None:
            return CONSTANT_ORDER_STATUS_INIT
        st = status.get('basic', {}).get('st',
                CONSTANT_ORDER_STATUS_INIT)
        if st > CONSTANT_ORDER_STATUS_NEW:
            raise OrderLockedException(orderID, st)
        return st

    @staticmethod
    def updateStatus(orderID, status):
        OrderMongoDAO.updateStatus(orderID, status)

    @staticmethod
    def addItem(
        orderID,
        dishID,
        amount,
        userID,
        ):
        try:
            status = OrderBiz.allowModify(orderID)
            dish = DishBiz.getDish(dishID)
            if status == CONSTANT_ORDER_STATUS_INIT:
                shopID = int(dish['detail']['shopID'])
                shopName = dish['detail']['shopName']
                OrderMongoDAO.addShopInfo(orderID, shopID, shopName,
                        CONSTANT_ORDER_STATUS_NEW)
                print 'add shop info'
            OrderMongoDAO.addItem(
                orderID,
                dishID,
                dish['detail']['name'],
                dish['detail']['pic'],
                dish['detail']['price'],
                amount,
                userID,
                )
            log.debug('order %s add dish(%s), userID %s, amount %s'
                      % (orderID, dishID, userID, amount))
        except ObjectDoesNotExist, err:
            raise IllegalParamException('shopID', shopID,
                    'shop not exist ')

    @staticmethod
    def updateItem(
        orderID,
        dishID,
        amount,
        userID,
        ):
        OrderBiz.allowModify(orderID)
        OrderMongoDAO.updateItem(orderID, dishID, amount)
        log.debug('order %s update dish(%s), userID %s, amount %s'
                  % (orderID, dishID, userID, amount))

    @staticmethod
    def delItem(orderID, dishID, userID):
        OrderBiz.allowModify(orderID)
        OrderMongoDAO.delItem(orderID, dishID)
        log.debug('order %s remove dish(%s), userID %s' % (orderID,
                  dishID, userID))

    @staticmethod
    def get(orderID, needDetail=False):
        '''
            return
            [
                {
                    'dish' : ,
                    'user' : ,
                }
            ]
        '''

        order = OrderMongoDAO.getSingleOrder(orderID)
        if order is None:
            raise IllegalParamException('orderID', orderID,
                    'order not exist')

        dishes = []
        for item in order.get('items', []):
            user = UserBiz.getBasicProfile(item['uid'])
            del item['uid']
            item['user'] = user
            dishes.append(item)

        if needDetail:
            del order['items']
            order['items'] = dishes
            return (order, order['basic']['st'])

        status = order.get('basic', {}).get('st', 1)
        return (dishes, status)

    @staticmethod
    def getShop(orderID):
        res = OrderMongoDAO.getShop(orderID)
        if not res:
            raise IllegalParamException('orderID', orderID,
                    'order not exist')
        return res['shop']

    @staticmethod
    def addMember(orderID, userID):
        OrderMongoDAO.addMember(orderID, userID)

    @staticmethod
    def getHisOrder(userID):
        tmpOrders = OrderMongoDAO.getHisOrder(userID)
        orders = []
        for item in tmpOrders:
            item['id'] = str(item['_id'])
            item['basic']['ts'] = item['basic']['ts'
                    ].strftime('%y-%m-%d %H:%M:%S')
            orders.append(item)
        return orders

    # todo: append order ID , shop ID, and createTime to order

    @staticmethod
    def confirm(
        orderID,
        userID,
        createTime,
        expectTime,
        consumerNum,
        compartmentRequire,
        contact,
        gender,
        phone,
        orderType,
        remark,
        ):
        OrderMongoDAO.addOrderDetail(
            orderID,
            userID,
            createTime,
            expectTime,
            consumerNum,
            compartmentRequire,
            contact,
            gender,
            phone,
            orderType,
            remark,
            CONSTANT_ORDER_STATUS_COMFIRMED,
            )

        # sync confirmed order to mysql

        order = OrderMongoDAO.getSingleOrder(orderID)
        newOrder = Order()
        newOrder.orderID = str(order['_id'])
        newOrder.status = CONSTANT_ORDER_STATUS_COMFIRMED
        newOrder.user = User.objects.get(pk=order['basic']['uid'])
        newOrder.shop = Shop.objects.get(pk=order['shop']['id'])
        newOrder.consumerNum = order['detail']['csn']
        newOrder.compartment = order['detail']['cpt']
        newOrder.contact = order['contact']['name']
        newOrder.gender = order['contact']['gdr']
        newOrder.phone = order['contact']['ph']
        newOrder.orderType = order['detail']['type']
        newOrder.remark = order['contact']['rmk']
        newOrder.expectTime = order['detail']['ept']
        newOrder.createTime = order['basic']['ts']
        newOrder.save()

        for item in order['items']:
            orderItem = OrderDetail()
            orderItem.order = newOrder
            orderItem.dish = Dish.objects.get(pk=item['gid'])  # item['gid']
            orderItem.price = item['pe']

            # orderItem.discount = item['ds']

            orderItem.discount = 1
            orderItem.ammount = item['at']
            orderItem.total = 0
            orderItem.placer = User.objects.get(pk=item['uid'])
            orderItem.save()


class ChatBiz(ChatMongoDAO):

    @staticmethod
    def get(orderID, chatID=None):
        records = ChatMongoDAO.getChat(orderID, chatID)
        chats = []
        for item in records:
            profile = UserBiz.getBasicProfile(item['uid'])
            item['user'] = profile
            item['ts'] = item['ts'].strftime('%y-%m-%d %H:%M:%S')
            del item['uid']
            item['_id'] = str(item['_id'])
            chats.append(item)
        return chats

    @staticmethod
    def add(
        userID,
        orderID,
        content,
        createTime,
        ctype,
        ):
        return ChatMongoDAO.add(orderID, content, createTime, ctype,
                                int(userID))

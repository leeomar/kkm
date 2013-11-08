#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo.connection import Connection
from pymongo import DESCENDING, ASCENDING
from pymongo import objectid
from pymongo.code import Code
import constant
import datetime

# Create your models here.

db = Connection('192.168.1.254', 27017).kkm_sns


class FeedMongoDAO:
    '''
        feed storage format:
        {
            'uID' : '12345',    # user ID
            'sID' : '54321',    # people who generate the feed
            'ts' : '',  # time stamp
            'ft' : 1,   # feed type: 1 comment; 2 consumer
            'fr' : 1,   # from : 1 web; 2 android; 3 iphone
            'cont' : '',  # feed content
        }
    '''

    @staticmethod
    def createIndex():
        db.feed.create_index([('ts', DESCENDING), ('uID', ASCENDING)])

    @staticmethod
    def add(
        userID,
        sID,
        ctime,
        ftype,
        sfrom,
        content,
        ):
        record = {
            'uID': userID,
            'sID': sID,
            'ts': ctime,
            'ft': ftype,
            'fr': sfrom,
            'cont': content,
            }
        db.feed.insert(record)
        return str(record['_id'])

    @staticmethod
    def batchAdd(records):
        db.feed.insert(records)
        return True

    @staticmethod
    def getHisFeed(userID, btime, onlySelf=False):
        if onlySelf:
            records = db.feed.find({'uID': userID, 'sID': userID, 'ts'
                                   : {'$lt': btime}}).sort('ts',
                    DESCENDING).limit(20)
        else:
            records = db.feed.find({'uID': userID, 'ts': {'$lt'
                                   : btime}}).sort('ts',
                    DESCENDING).limit(20)
        return records

    @staticmethod
    def getNewFeed(userID, btime, limit=20):
        records = db.feed.find({'uID': userID, 'ts': {'$gt'
                               : btime}}).sort('ts',
                ASCENDING).limit(limit)
        return records


class CommentMongoDAO:

    '''
        comment storage format:
        {
            'uID' : '12345',    #user id
            'gID' ; '2',        #dish id
            'pt' : 'jis223o2l35.jpg', #photo
            'cont' : 'delicous food', #feed content
            'ts' : '20110521324',   #time stamp
            'gs' : '2',             #great shot
        }
    '''

    @staticmethod
    def createIndex():
        db.comment.create_index([('ts', DESCENDING), ('gID',
                                ASCENDING)])
        return True

    @staticmethod
    def addComment(
        userID,
        dishID,
        photo,
        content,
        createTime,
        ):
        comment = {
            'uID': userID,
            'gID': dishID,
            'pt': photo,
            'cont': content,
            'ts': createTime,
            'gs': 0,
            }
        db.comment.insert(comment)
        return str(comment['_id'])

    @staticmethod
    def greatShot(commentID):
        db.comment.update({'_id': objectid.ObjectId(commentID)}, {'$inc'
                          : {'gs': 1}})
        return True

    @staticmethod
    def getComment(dishID, btime, num=20):
        comments = db.comment.find({'gID': dishID, 'ts': {'$lt'
                                   : btime}}).sort('ts',
                DESCENDING).limit(num)
        return comments

    @staticmethod
    def getFriendComment(dishID, btime, idArray):
        comments = db.comment.find({'gID': dishID, 'ts': {'$lt'
                                   : btime}, 'uID': {'$in'
                                   : idArray}}).sort('ts',
                DESCENDING).limit(20)
        return comments


class DishRankingListDAO:

    '''
        this class will generate the hottest dish in certain period
        hottest weight = 4 * like + 2 * comment + 3 * wanted + 1 * eated
        {
            '_id' : '2', #dish id
            'value' : {
                'weight' : 10, #weight
                'commenters' : '277674,2889764,', #commenters
                'count' : 2, #num of commenters
                'rid' : 1, #region id
            }
        }
    '''

    @staticmethod
    def caculateHotDish(beginTime, endTime):
        m = Code("function() { "
                " var weight = 0; "
                " var commenters = ''; "
                " switch(this.tp){ "
                " case 'lk' : weight = 4; break; "
                " case 'ct' : weight = 2; commenters = commenters.concat( this.uid ).concat( ',' ); break; "
                " case 'et' : weight = 1; break; "
                " case 'wt' : weight = 3; break; "
                " }"
                " emit(this.tid, { weight: weight, commenters: commenters, count: 1, rid: this.rid } ); "
                " } ")
        r = Code("function(key, values) { "
                " var result = { weight : 0, commenters : '', count : 0 , rid : 0 }; "
                " for( var i = 0; i < values.length; i++ ){ "
                "   result.weight += values[i].weight; "
                "   result.commenters = result.commenters.concat( values[i].commenters ); "
                "   result.count += values[i].count; "
                "   result.rid = values[i].rid; "
                " }"
                " return result; "
                " } ")
        f = Code("function(key, value) {"
                " value.commenters = '['.concat( value.commenters ).concat( ']' ); "
                " return value; "
                "} ")

        db.vote.map_reduce(m, r, query={'ts': {'$gt': beginTime, '$lt'
                           : endTime}}, out='dish_ranking_list')

    @staticmethod
    def ensureIndex():
        pass

        # db.vote.ensure_index('ts')

    @staticmethod
    def getHotDish(regionID, weight=-1):
        if weight == -1:
            return db.dish_ranking_list.find({'value.rid'
                    : regionID}).sort('value.weight', DESCENDING).limit(20)
        else:
            return db.dish_ranking_list.find({'value.rid': regionID,
                    'value.weight': {'$lt': weight}}).sort('weight',
                    DESCENDING).limit(20)


class VoteMongoDAO:

    '''
        there are two kind of statistic, detail & overview
        dish statistic storage format:
        {
            'tid' : 12345, #target id
            'rid' : 1, #region id
            'sid' : 1, #shop id
            'lk' : 1,  #like
            'et' : 23, #eated
            'wt' : 19, #want
            'ct' : 100, #comment
        }
        shop statistic storage format:
        {
           'sid' : 1 , #shop Id
           'lk' : 1,  #like
           'et' : 23, #eated
           'wt' : 19, #want
           'ct' : 100, #comment
        }

        vote storage detail list:
        {
            'tid' : 12345, #target id
            'rid' : 11, #region id
            'sid' : 1, #shop id
            'uid' : 22, #user id
            'tp' : , #type, 1, eated; 2 comment; 3 wanted; 4 like
            'ts' : 20110623, #timestamp
        }
    '''

    @staticmethod
    def createIndex():
        db.dish_statistic.create_index('tid', unique=True)
        db.vote.create_index('tid')

    # def add(targetID, regionID, shopID):
    #    item = { 'tid' : targetID, 'rid' : regionID, 'sid' : shopID, 'lk' : 0, 'et' : 0, 'wt' : 0, 'ct' : 0 }
    #    db.dish_statistic.insert(item)
    #    return str(item['_id'])

    @staticmethod
    def like(
        targetID,
        regionID,
        shopID,
        userID,
        ):
        print type(targetID)
        print targetID, regionID, shopID, userID
        db.dish_statistic.update({'tid': targetID}, {'$inc': {'lk'
                                 : 1}}, upsert=True)
        db.shop_statistic.update({'sid': shopID}, {'$inc': {'lk': 1}},
                                 upsert=True)
        db.vote.insert({
            'tid': targetID,
            'uid': userID,
            'rid': regionID,
            'sid': shopID,
            'tp': 'lk',
            'ts': datetime.datetime.now(),
            })
        return True

    @staticmethod
    def eat(
        targetID,
        regionID,
        shopID,
        userID,
        ):
        db.dish_statistic.update({'tid': targetID}, {'$inc': {'et'
                                 : 1}}, upsert=True)
        db.shop_statistic.update({'sid': shopID}, {'$inc': {'et': 1}},
                                 upsert=True)
        db.vote.insert({
            'tid': targetID,
            'uid': userID,
            'rid': regionID,
            'sid': shopID,
            'tp': 'et',
            'ts': datetime.datetime.now(),
            })
        return True

    @staticmethod
    def want(
        targetID,
        regionID,
        shopID,
        userID,
        ):
        db.dish_statistic.update({'tid': targetID}, {'$inc': {'wt'
                                 : 1}}, upsert=True)
        db.shop_statistic.update({'sid': shopID}, {'$inc': {'wt': 1}},
                                 upsert=True)
        db.vote.insert({
            'tid': targetID,
            'uid': userID,
            'rid': regionID,
            'sid': shopID,
            'tp': 'wt',
            'ts': datetime.datetime.now(),
            })
        return True

    @staticmethod
    def comment(
        targetID,
        regionID,
        shopID,
        userID,
        ):
        db.dish_statistic.update({'tid': targetID}, {'$inc': {'ct'
                                 : 1}}, upsert=True)
        db.shop_statistic.update({'sid': shopID}, {'$inc': {'ct': 1}},
                                 upsert=True)
        db.vote.insert({
            'tid': targetID,
            'uid': userID,
            'rid': regionID,
            'sid': shopID,
            'tp': 'ct',
            'ts': datetime.datetime.now(),
            })
        return True

    @staticmethod
    def getDishStatistic(targetID):
        return db.dish_statistic.find_one({'tid': targetID})

    @staticmethod
    def getShopStatistic(shopID):
        return db.shop_statistic.find_one({'sid': shopID})


class OrderMongoDAO:

    '''
        order storage format:
        {
            'basic' : {
                'uid' : 12344,  #user id
                'ts' : 201105,  #timestamp
                'st' : 1,       #status: 1 new; 2 confirmed 3 paid 4 finished 5 discard 6 locked
            }
            'shop': {
                'id' : 1,      #shopid
                'name' : ,     #shopname
            }
            'contact' : {
                'name'  : 'wang',
                'gdr'   : ,         #gender
                'ph' : ,            #phone
                'rmk'   : 'call',   #remark
            }
            'detail' : {
                'cpt' : 1,      #compartment : 1 包间优先; 2 大厅优先; 3 只定包间; 4 只定大厅
                'csn' : 3,      #consumer num
                'type' : 1,       #order type: 1 自己订餐, 2 代人订餐
                'ept' : ,       #expect time
            }
            'items' :
            [
                {
                    'gid' : 1123,   #good id
                    'gname':  ,     #good name
                    'pic':  ,       #good picture
                    'pe' : 12,      #price
                    'ds' : 1,       #discount
                    'at' : 1,       #ammount
                    'uid' : 12344,  #user id who order the good
                },
            ]
            'mrs' : [1234, 23435],  #members
        }
    '''
    @staticmethod
    def addEvaluate(orderID):
        db.order.  b({'_id': objectid.ObjectId(orderID)}, {'$set':{
                'ev': 1}})

    @staticmethod
    def getEvaluate(orderID):
        ev = db.order.find_one({'_id': objectid.ObjectId(orderID)}).get('ev', 0)
        return ev

    @staticmethod
    def createIndex():
        db.order.create_index([('mrs', DESCENDING), ('ts', DESCENDING)])
        return True

    @staticmethod
    def add(
        userID,
        shopID,
        shopName,
        createTime,
        ):
        basic = {'uid': userID, 'ts': createTime, 'st': 1}
        shop = {'id': shopID, 'name': shopName}
        orderItem = {'basic': basic, 'shop': shop, 'mrs': [userID]}
        db.order.insert(orderItem)
        return str(orderItem['_id'])

    @staticmethod
    def addShopInfo(
        orderID,
        shopID,
        shopName,
        status,
        ):
        shop = {'id': shopID, 'name': shopName}
        db.order.update({'_id': objectid.ObjectId(orderID)}, {'$set'
                        : {'shop': shop, 'basic.st': status}},
                        upsert=True)

    @staticmethod
    def addOrderDetail(
        orderID,
        userID,
        createTime,
        expectTime,
        consumerNum,
        compartmentRequire,
        contant,
        gender,
        phone,
        orderType,
        remark,
        status,
        ):

        contact = {
            'name': contant,
            'gdr': gender,
            'ph': phone,
            'rmk': remark,
            }
        detail = {
            'cpt': compartmentRequire,
            'csn': consumerNum,
            'ept': expectTime,
            'type': orderType,
            }
        basic = {'uid': userID, 'ts': createTime, 'st': status}
        db.order.update({'_id': objectid.ObjectId(orderID)}, {'$set'
                        : {'contact': contact, 'detail': detail, 'basic'
                        : basic}})
        return True

    @staticmethod
    def addItem(
        orderID,
        dishID,
        goodName,
        picture,
        price,
        amount,
        userID,
        ):
        exist = db.order.find({'_id': objectid.ObjectId(orderID),
                              'items.gid': dishID}).count()
        if exist == 1:
            return False

        item = {
            'gid': dishID,
            'gname': goodName,
            'pic': picture,
            'pe': price,
            'at': amount,
            'uid': userID,
            }
        db.order.update({'_id': objectid.ObjectId(orderID)}, {'$push'
                        : {'items': item}}, upsert=True)
        return True

    @staticmethod
    def updateItem(orderID, dishID, amount):
        db.order.update({'_id': objectid.ObjectId(orderID), 'items.gid'
                        : dishID}, {'$inc': {'items.$.at': amount}})
        return True

    @staticmethod
    def delItem(orderID, dishID):
        db.order.update({'_id': objectid.ObjectId(orderID)}, {'$pull'
                        : {'items': {'gid': dishID}}})
        return True

    @staticmethod
    def getSingleOrder(orderID):
        return db.order.find_one({'_id': objectid.ObjectId(orderID)})

    @staticmethod
    def getStatus(orderID):
        return db.order.find_one({'_id': objectid.ObjectId(orderID)},
                                 {'basic.st': 1})

    @staticmethod
    def getShop(orderID):
        return db.order.find_one({'_id': objectid.ObjectId(orderID)},
                                 {'shop': 1})

    @staticmethod
    def updateStatus(orderID, status):
        db.order.update({'_id': objectid.ObjectId(orderID)}, {'$set'
                        : {'basic.st': status}})

    @staticmethod
    def getHisOrder(userID):
        return db.order.find({'basic.uid': userID}, {'shop': 1, 'basic'
                             : 1}).sort('ts', DESCENDING)

    @staticmethod
    def addMember(orderID, userID):
        db.order.update({'_id': objectid.ObjectId(orderID)},
                        {'$addToSet': {'mrs': userID}})
        return True

    @staticmethod
    def getCustomer(shopID):
        return db.order.find({'shop.id': shopID, 'basic.st' : { '$gte' : 1 }},
                             {'basic.uid': 1, '_id': 1}).sort('basic.ts', DESCENDING).limit(15)\
                             .distinct('basic.uid')


class ChatMongoDAO:

    '''
        chat storage format:
        {
            'oid' : 'aaa', #order id
            'cont' : 'its delicous', #content
            'ts' : 20110123, #timestamp
            'ty' : 1, #type: 1 chat; 2* sys msg
            'uid' : 12344, #user id
        }
        there are 3 types of sys message:
        add item
        {
            'cont'  : '123,1', #cont contains one dish ID
            'type' : 21,  #21 add item;
            ...
        }
        remove item
        {
            'cont'  : '123', #cont contains one dish ID
            'type' : 22,  #22 remove item
            ...
        }
        update item
        {
            'cont' : '123,-2', #dishID,amount
            'tp' : 23, #update item
        }
    '''

    @staticmethod
    def createIndex():
        db.chat.create_index('oid')

    @staticmethod
    def add(
        orderID,
        content,
        createTime,
        ctype,
        userID,
        ):
        chat = {
            'oid': orderID,
            'cont': content,
            'ts': createTime,
            'ty': ctype,
            'uid': userID,
            }
        db.chat.insert(chat)
        return str(chat['_id'])

    @staticmethod
    def getHisChat(orderID, btime):
        return db.chat.find({'oid': orderID, 'ts': {'$lt'
                            : btime}}).sort('ts', DESCENDING).limit(50)

    @staticmethod
    def getChat(orderID, chatID=None):
        if chatID is None:
            return db.chat.find({'oid': orderID, 'ty': 'chat'
                                }).sort('ts', ASCENDING)
        else:
            return db.chat.find({'oid': orderID, 'ty': 'chat', '_id'
                                : {'$gt'
                                : objectid.ObjectId(chatID)}}).sort('ts'
                    , ASCENDING)

    @staticmethod
    def getMaxChatID(orderID):
        res = db.chat.find({'oid': orderID}, {'_id': 1}).sort('ts', DESCENDING).limit(1)
        if res.count() > 0:
            return str(res[0]['_id'])
        return None

    @staticmethod
    def getNewChat(orderID, btime):
        return db.chat.find({'oid': orderID, 'ts': {'$gt'
                            : btime}}).sort('ts', ASCENDING)


class FollowMongoDAO:

    '''
        record the follower num and following num
        follow
        {
            'uid' : 123, #user id
            'following' : [12, 33], #following ids
            'follower' : [22, 34],  #follower ids
        }
        follow_statistic
        {
            'uid' : 123,
            'num' : 1,  #following number
            'rnum': 2,  #follower number
        }
    '''

    @staticmethod
    def createIndex():
        db.follow_statistic.create_index('rnum')

    @staticmethod
    def follow(userID1, userID2):
        '''
           add new relation: userID1 following userID2
        '''

        db.follow.update({'uid': userID1}, {'$addToSet': {'following'
                         : userID2}}, upsert=True)
        db.follow_statistic.update({'uid': userID1}, {'$inc': {'num'
                                   : 1}}, upsert=True)

        db.follow.update({'uid': userID2}, {'$addToSet': {'follower'
                         : userID1}}, upsert=True)
        db.follow_statistic.update({'uid': userID2}, {'$inc': {'rnum'
                                   : 1}}, upsert=True)

    @staticmethod
    def unfollow(userID1, userID2):
        '''
            delete relation: userID1 cancle following userID2
        '''

        db.follow.update({'uid': userID1}, {'$pull': {'following'
                         : userID2}})
        db.follow_statistic.update({'uid': userID1}, {'$inc': {'num'
                                   : -1}})

        db.follow.update({'uid': userID2}, {'$pull': {'follower'
                         : userID1}})
        db.follow_statistic.update({'uid': userID2}, {'$inc': {'rnum'
                                   : -1}})

    @staticmethod
    def get(userID):
        return db.follow.find_one({'uid': userID})

    @staticmethod
    def getFollowing(userID):
        record = db.follow.find_one({'uid': userID})
        if record == None:
            return None
        else:
            return record.get('following', None)

    @staticmethod
    def getFollower(userID):
        record = db.follow.find_one({'uid': userID})
        if record == None:
            return None
        else:
            return record.get('follower', None)

    @staticmethod
    def getStatistic(userID):
        record = db.follow_statistic.find_one({'uid': userID})
        return record

    @staticmethod
    def getPopFollowings():
        return db.follow_statistic.find().sort('rnum',
                DESCENDING).limit(15)



#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding : utf-8

from kekemen.biz.commons import *
from kekemen.biz.relation import UserBiz


class CommentBiz:

    @staticmethod
    def add(
        userID,
        goodID,
        photo,
        content,
        createTime,
        ):
        CommentMongoDAO.addComment(userID, goodID, photo, content,
                                   createTime)
        VoteBiz.comment(goodID, userID)

    @staticmethod
    def get(goodID, beginTime, num=20):
        '''
        {
            'uID' : '12345',    //user id
            'user' : {}, //user name
            'gID' ; '2',      //good id
            'pt' : 'jis223o2l35.jpg', //photo
            'cont' : 'delicous food',
            'ts' : '20110521324'  //time stamp
            'gs' : '2',  //great shot
        }

        '''

        comments = CommentMongoDAO.getComment(goodID, beginTime, num)
        results = []
        for comment in comments:
            profile = UserBiz.getBasicProfile(comment['uID'])
            comment['user'] = profile
            comment['_id'] = str(comment['_id'])
            comment['ts'] = comment['ts'].strftime('%y-%m-%d %H:%M:%S')
            del comment['uID']
            results.append(comment)

        return results

    @staticmethod
    def getFriendComment(goodID, userID, beginTime):
        '''
            get friend comments, return the same as getComment()
        '''

        IDs = FollowMongoDAO.getFollowing(userID)
        if IDs == None or len(IDs) == 0:
            log.debug('get none friend comments,user(%s) does not following anyone'
                      )
            return []

        comments = CommentMongoDAO.getFriendComment(goodID, beginTime,
                IDs)
        results = []
        for comment in comments:
            profile = UserBiz.getBasicProfile(comment['uID'])
            comment['user'] = profile

            # comment['pic'] = profile['pic']

            comment['_id'] = str(comment['_id'])
            comment['ts'] = comment['ts'].strftime('%y-%m-%d %H:%M:%S')
            results.append(comment)

        return results


class VoteBiz:

    @staticmethod
    def getLocation(dishID):
        try:
            shop = Dish.objects.get(pk=dishID).shop
            regionID = shop.region.distinct()[0].parent.regionID
            return (shop.shopID, regionID)
        except ObjectDoesNotExist, err:
            log.error(err)
            log.error(traceback.format_exc())
            raise IllegalParamException('dishID', dishID,
                    'dish not eixst')

    @staticmethod
    def like(dishID, userID):
        (shopID, regionID) = VoteBiz.getLocation(dishID)
        VoteMongoDAO.like(dishID, regionID, shopID, userID)

    @staticmethod
    def eat(dishID, userID):
        (shopID, regionID) = VoteBiz.getLocation(dishID)
        VoteMongoDAO.eat(dishID, regionID, shopID, userID)

    @staticmethod
    def want(dishID, userID):
        (shopID, regionID) = VoteBiz.getLocation(dishID)
        VoteMongoDAO.want(dishID, regionID, shopID, userID)

    @staticmethod
    def comment(dishID, userID):
        (shopID, regionID) = VoteBiz.getLocation(dishID)
        VoteMongoDAO.comment(dishID, regionID, shopID, userID)



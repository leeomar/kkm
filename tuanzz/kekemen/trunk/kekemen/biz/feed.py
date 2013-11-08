#!/usr/bin/python
# -*- coding: utf-8 -*-
from kekemen.biz.commons import *
from kekemen.biz.relation import UserBiz, FollowBiz


class FeedBiz:

    @staticmethod
    def add(
        userID,
        ctime,
        ftype,
        sfrom,
        content,
        ):
        '''
            add feed,
            this function will push feed all followers
        '''

        feeds = [{
            'uID': userID,
            'sID': userID,
            'ts': ctime,
            'ft': ftype,
            'fr': sfrom,
            'cont': content,
            }]

        followers = FollowMongoDAO.getFollower(userID)
        for follower in followers:
            record = {
                'uID': follower,
                'sID': userID,
                'ts': ctime,
                'ft': ftype,
                'fr': sfrom,
                'cont': content,
                }
            feeds.append(record)

        log.debug('add feed, %s' % feeds)
        FeedMongoDAO.batchAdd(feeds)
        return True

    @staticmethod
    def get(userID, beginTime, onlySelf=False):
        '''
            get feeds before beginTime,
            return feed format:
            {
                'user'  : {}  , #username

                'ts' : '201105210918', #time stamp
                'ft' : 1,  #feed type: 1 comment; 2 consumer
                'fr' : 1, #from : 1 web; 2 android; 3 iphone
                'cont'  : 'feed content', #content
            }
        '''

        feeds = FeedMongoDAO.getHisFeed(userID, beginTime, onlySelf)
        result = []
        for feed in feeds:
            basicProfile = UserBiz.getBasicProfile(feed['sID'])
            feed['user'] = basicProfile
            feed['ts'] = datetime.datetime.strftime(feed['ts'],
                    '%y-%m-%d %H:%M:%S')
            feed['id'] = str(feed['_id'])
            del feed['_id']
            del feed['uID']
            del feed['sID']
            result.append(feed)

        log.debug('get %s feed before %s, return %d records '
                  % (userID, beginTime, feeds.count()))
        return result



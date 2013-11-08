#!/usr/bin/python
# -*- coding: utf-8 -*-
from kekemen.biz.commons import *
from kekemen.settings import MEDIA_PATH
from kekemen.sns.mongo import FeedMongoDAO

# log = logging.getLogger('project')


class UserBiz:

    @staticmethod
    def getBasicProfile(userID):
        '''
            get basic profile, return
            {
                'uid' : '',
                'username' : '',
                'pic' : {
                    'large' : ,
                    'middle': ,
                    'small' : ,
                }
            }
        '''

        log.debug('get basic profile %s' % userID)
        profile = UserBiz.getProfile(userID)
        return {'uid': profile['uid'], 'username': profile['username'],
                'pic': profile['pic']}

    @staticmethod
    def getStatisticProfile(userID):
        '''
            {
                'uid' : '',
                'username' : '',
                'pic' : {
                    'large' : ,
                    'middle': ,
                    'small' : ,
                }
                'num' : 1,  #following num
                'fnum' : 4, #follower num
            }
        '''

        profile = UserBiz.getProfile(userID)
        statistic = FollowMongoDAO.getStatistic(userID)
        if statistic is None:
            statistic = {}

        return {
            'uid': profile['uid'],
            'username': profile['username'],
            'pic': profile['pic'],
            'num': statistic.get('num', 0),
            'rnum': statistic.get('rnum', 0),
            }

    @staticmethod
    def getProfile(userID):
        '''
            get user profile, return
            {
                'uid' : '111',
                'username' : 'wangzz',
                'name' : 'xiao wang',
                'email' : '',
                'phone' : '',
                'account' : '',
                'pic' : {
                    'large' : ,
                    'middle': ,
                    'small' : ,
                }
                'regionID' : '',
            }
        '''

        try:
            log.debug('get profile %s' % userID)
            cachedUserKey = 'user_' + str(userID)
            cachedUser = cache.get(cachedUserKey)
            if cachedUser != None:
                return cachedUser

            user = User.objects.get(pk=userID)
            profile = user.get_profile()
            cachedUser = {
                'uid': userID,
                'username': user.username,
                'name': user.first_name,
                'email': user.email,
                'phone': profile.phone,
                'account': profile.account,
                'regionID': profile.region.regionID,
                }
            pic = {'large': MEDIA_PATH['large'] + profile.picture,
                   'middle': MEDIA_PATH['middle'] + profile.picture,
                   'small': MEDIA_PATH['small'] + profile.picture}
            cachedUser['pic'] = pic

            cache.set(cachedUserKey, cachedUser)
            log.debug('cache user %s, %s' % (cachedUserKey, cachedUser))
            return cachedUser
        except ObjectDoesNotExist, err:
            raise IllegalParamException('userID', userID,
                    'user not exist')


class FollowBiz:

    @staticmethod
    def follow(userID1, userID2):
        '''
            add relation: 'userID1' follows 'userID2'
        '''
        try:
            ts = datetime.datetime.now()
            following = Follow(userID=userID1, createTime=ts)
            following.following = User.objects.get(pk=userID2)

            followReverse = FollowReverse(userID=userID2, createTime=ts)
            followReverse.follower = User.objects.get(pk=userID1)

            followReverse.save()
            following.save()

            # update mongo follow

            FollowMongoDAO.follow(userID1, userID2)
            log.debug('add relation, %s follows %s' % (userID1,
                      userID2))

            # update cache

            key1 = 'following_' + str(userID1)
            key2 = 'follower_' + str(userID2)
            cache.delete_many([key1, key2])
            
            #update 5 feeds
            btime = datetime.datetime.now() - datetime.timedelta(days=30)
            hisfeeds = FeedMongoDAO.getNewFeed(userID=userID2, btime=btime, limit=5);
            myfeeds = []

            for feed in hisfeeds :
                record = {
                    'uID' : userID1,
                    'sID' : userID2,
                    'ts' : feed['ts'],
                    'ft' : feed['ft'],
                    'fr' : feed['fr'],
                    'cont' : feed['cont'],
                }
                myfeeds.append(record)
            FeedMongoDAO.batchAdd(myfeeds)

        except ObjectDoesNotExist, err:
            log.error(err)
            log.error(traceback.format_exc())
            raise IllegalParamException('userID(,)', (userID1,
                    userID2), 'user not exist')
        except IntegrityError, err:
            log.warn('duplicate following (%s, %s)' % (userID1,
                     userID2))

    @staticmethod
    def unfollow(userID1, userID2):
        '''
            delete relation: userID1 cancle following userID2
        '''

        try:

            # ts = datetime.datetime.now()

            user1 = User.objects.get(pk=userID1)
            user2 = User.objects.get(pk=userID2)
            follow = Follow.objects.get(userID=userID1, following=user2)

            # follow.status = 2

            follow.delete()

            followReverse = FollowReverse.objects.get(userID=userID2,
                    follower=user1)

            # followReverse.status = 2

            followReverse.delete()

            FollowMongoDAO.unfollow(userID1, userID2)

            # update cache

            key1 = 'following_' + str(userID1)
            key2 = 'follower_' + str(userID2)
            cache.delete_many([key1, key2])
        except ObjectDoesNotExist, err:
            log.error(err)
            log.error(traceback.format_exc())
            raise IllegalParamException('userID(,)', (userID1,
                    userID2), 'user not exist')

    @staticmethod
    def getFollower(userID):
        '''
        get user's followers, return:
        [
            {
                'uid' : '',
                'username' : '',
                'pic' : '',
            },
        ]
        '''

        key = 'follower_' + str(userID)
        value = cache.get(key)
        if value == None:
            followerIDs = FollowMongoDAO.getFollower(userID)
            if followerIDs is None or len(followerIDs) == 0:
                log.debug('user(%s) has no followers' % userID)
                return []

            value = []
            for uid in followerIDs:
                user = UserBiz.getBasicProfile(uid)
                if user is not None:
                    value.append(user)

            cache.set(key, value)
            log.debug('cache  %s, %s' % (key, value))

        return value

    @staticmethod
    def getFollowing(userID):
        '''
            get following list, return:
            [
                {
                    'uid' : '',
                    'username' : '',
                    'pic' : '',
                },
            ]
        '''

        key = 'following_' + str(userID)
        value = cache.get(key)
        if value == None:
            followingIDs = FollowMongoDAO.getFollowing(userID)
            if followingIDs is None or len(followingIDs) == 0:
                log.debug('user(%s) does not follow anyone' % userID)
                return []

            value = []
            for uid in followingIDs:
                user = UserBiz.getBasicProfile(uid)
                if user is not None:
                    value.append(user)
            cache.set(key, value)
            log.debug('cache ( %s, %s ) ' % (key, value))
        return value

    @staticmethod
    def getPopFollowing(userID=None):
        '''
            get popular people to follow, return:
            [
                {
                    'uid' : '123',
                    'username' : '',
                    'pic' : '',
                    'num' : 4,      #following num
                    'fnum' : 5,     #follower num
                }
            ]
        '''

        key = 'pop_follower'
        value = cache.get(key)
        if value == None:
            value = []
            users = FollowMongoDAO.getPopFollowings()

            for item in users:
                user = UserBiz.getBasicProfile(item['uid'])
                user['rnum'] = item.get('rnum', 0)
                user['num'] = item.get('num', 0)
                user['follow'] = False
                value.append(user)
            cache.set(key, value)
            log.debug('cache %s pop people' % len(value))

        value = FollowBiz.appendIfFollow(userID, value)
        return value

    @staticmethod
    def appendIfFollow(userID, users):
        if userID is None:
            return users

        friends = FollowMongoDAO.getFollowing(userID)
        if not friends:
            return users

        fset = set(friends)
        for user in users:
            if userID == user['uid']:
                user['follow'] = None
            elif user['uid'] in fset:
                user['follow'] = True
        return users


    @staticmethod
    def isFollowing(userID1, userID2):
        '''
        If userID1 follows userID2, return true;
        Otherwise return false
        '''
        followings = FollowMongoDAO.getFollowing(userID1)
        if not followings:
            return False;

        if userID2 in followings:
            return True

        return False

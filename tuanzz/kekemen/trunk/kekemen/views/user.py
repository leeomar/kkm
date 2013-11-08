#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import RequestContext

from kekemen.views.common import *
from kekemen.biz.relation import UserBiz, FollowBiz


def home(request, userID):
    profile = UserBiz.getProfile(userID)
    userID = int(userID)
    isOwner = request.user.id and request.user.id == userID
    print isOwner

    isFollowing = False
    if request.user.id and request.user.id != userID:
        isFollowing = FollowBiz.isFollowing(request.user.id, userID)

    context = RequestContext(request)
    return render_to_response('user_index.html', {'profile': profile, 'isOwner': isOwner,
            'isFollowing': isFollowing}, context_instance=context)

def getFollower(request, userID):
    followers = FollowBiz.getFollower(int(userID))
    return HttpResponse(json.dumps({'ret': 200, 'data': followers}))


def getFollowing(request, userID):
    followings = FollowBiz.getFollowing(int(userID))
    return HttpResponse(json.dumps({'ret': 200, 'data': followings}))



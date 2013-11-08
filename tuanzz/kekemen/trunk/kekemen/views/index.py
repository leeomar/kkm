#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import traceback

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import simplejson as json

from kekemen.biz.shop import DishBiz
from kekemen.biz.feed import FeedBiz
from kekemen.biz.relation import FollowBiz
from kekemen.views.common import *
from kekemen.biz.commons import IllegalParamException


def index(request):
    '''
    init index page,
    '''

    # followBiz = FollowBiz()
    # popStars = followBiz.getPopToFollow()

    return render_to_response('index.html')


def getHotDish(request):
    '''
    get hot dishes for certain,
    param:
        weight, default -1
    return: ref to Biz.py, return the same as DishBiz.getHotDishes
    '''

    try:
        weight = request.GET.get('anchor', -1)
        regionID = request.COOKIES.get('region_id', 1)
        hotDishes = DishBiz.getHotDishes(int(regionID), int(weight))
        if not hotDishes:
            return HttpResponse(json.dumps({'ret': 200, 'type': 'hot',
                                'data': []}))

        anchor = hotDishes[-1]['weight']
        return HttpResponse(json.dumps({
            'ret': 200,
            'type': 'hot',
            'anchor': anchor,
            'data': hotDishes,
            }))
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(json.dumps({
            'ret': 200,
            'type': 'hot',
            'anchor': anchor,
            'data': [],
            }))
    except BaseException, err:

        # return HttpResponse( ajax_error_illegal_param )

        log.error(err)
        return HttpResponse(ajax_error_server_failed)


def getNewDish(request):
    '''
    get new dishes for certain area,
    param:
        page, default 1
    return: ref to DishBiz.getNewDishes()
    '''

    try:
        page = int(request.GET.get('anchor', 1))
        if page < 0:
            page = 1
        regionID = int(request.COOKIES.get('region_id', 1))
        newDishes = DishBiz.getNewDishes(regionID, page)
        return HttpResponse(json.dumps({
            'ret': 200,
            'type': 'new',
            'anchor': page + 1,
            'data': newDishes,
            }))
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


def getFeed(request):
    '''
    get feed before beginTime,
    return: ref to Biz.FeedBiz.getHisFeed()
    '''

    if not request.user.is_authenticated():
        return HttpResponse(ajax_error_not_login)

    try:
        beginTime = request.GET.get('anchor', '')
        beginTime = datetime.datetime.strptime(beginTime,
                '%y-%m-%d %H:%M:%S')
    except ValueError, err:
        log.debug(err)
        beginTime = datetime.datetime.now()

    try:
        feeds = FeedBiz.get(request.user.id, beginTime)
        if not feeds:
            anchor = ''
        else:
            anchor = feeds[-1]['ts']
        return HttpResponse(json.dumps({
            'ret': 200,
            'type': 'feed',
            'anchor': anchor,
            'data': feeds,
            }))
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_server_failed)


def getTwitter(request):
    '''
    get feed before beginTime,
    return: ref to Biz.FeedBiz.getHisFeed()
    '''

    userID = int(request.GET['user_id'])
    try:
        beginTime = request.GET.get('anchor', '')
        beginTime = datetime.datetime.strptime(beginTime,
                '%y-%m-%d %H:%M:%S')
    except ValueError, err:
        log.debug(err)
        beginTime = datetime.datetime.now()

    try:
        feeds = FeedBiz.get(userID, beginTime, True)
        if not feeds:
            anchor = ''
        else:
            anchor = feeds[-1]['ts']
        return HttpResponse(json.dumps({
            'ret': 200,
            'type': 'twitter',
            'anchor': anchor,
            'data': feeds,
            }))
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_server_failed)


def getPopFollowing(request):
    '''
    get pop following
    '''

    try:
        userID = request.user.id
        users = FollowBiz.getPopFollowing(userID)
        return HttpResponse(json.dumps({'ret': 200, 'data': users}))
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_server_failed)


def follow(request, userID):
    try:
        if not request.user.is_authenticated():
            return HttpResponse(ajax_error_not_login)

        hostID = int(request.user.id)
        FollowBiz.follow(hostID, int(userID))
        return HttpResponse(ajax_suc_response)
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)


def unfollow(request, userID):
    try:
        if not request.user.is_authenticated():
            return HttpResponse(ajax_error_not_login)

        hostID = int(request.user.id)
        FollowBiz.unfollow(hostID, int(userID))
        return HttpResponse(ajax_suc_response)
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)

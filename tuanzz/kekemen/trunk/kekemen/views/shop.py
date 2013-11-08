#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template import RequestContext

from kekemen.views.common import *
from kekemen.biz.shop import ShopBiz, DishBiz
from kekemen.biz.comment import CommentBiz, VoteBiz
from kekemen.settings import MEDIA_PATH
from kekemen.biz.commons import *
from kekemen.biz.feed import FeedBiz
from pymongo import objectid
from django.core.cache import cache
from kekemen.sns.mongo import CommentMongoDAO

def shop(request, shopID):
    shop = ShopBiz.get(shopID)
    menus = ShopBiz.getMenu(shopID)
    statistic = ShopBiz.getStatistic(int(shopID))
    objectid_ = request.REQUEST.get('order_id', objectid.ObjectId())

    context = RequestContext(request)
    return render_to_response('shop.html', {
        'username': request.user.username,
        'shop': shop,
        'menus': menus,
        'objectid': objectid_,
        'static_media_path': MEDIA_PATH,
        'shopStatistic': statistic,
        }, context_instance=context)


def getCustomer(request):
    try:
        shopID = int(request.GET['shop_id'])
        # userID = request.user.id
        customers = ShopBiz.getCustomer(shopID)
        return HttpResponse(json.dumps({'ret': 200, 'data': customers}))
    except KeyError, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_server_failed)


def getDishByMenu(request, shopID, menuID):
    '''
    get dish menu
    '''

    # shopID = request.GET.get('shop_id')
    # menuID = request.GET.get('menu_id')

    try:
        page = request.GET.get('page', 1)
        dishes = DishBiz.getByMenu(shopID, menuID, page)
        return HttpResponse(json.dumps({'ret': 200, 'menuID': menuID,
                            'data': dishes}))
    except IllegalParamException, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        log.error(traceback.format_exc())
        return HttpResponse(ajax_error_server_failed)


lambdaFunction = {'like': lambda x, y: VoteBiz.like(x, y),
                  'eat': lambda x, y: VoteBiz.eat(x, y),
                  'want': lambda x, y: VoteBiz.want(x, y)}


def action(request, action, dishID):
    '''
    actions (like, eat, want)
    '''

    try:
        userID = request.user.id
        if userID == None:
            userID = -1
        lambdaFunction[action](int(dishID), userID)
        return HttpResponse(ajax_suc_response)
    except KeyError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)


def addComment(request):
    try:
        if not request.user.is_authenticated():
            return HttpResponse(ajax_error_not_login)
        userID = int(request.user.id)
        goodID = int(request.GET['dish_id'])
        pic = request.GET.get('pic', '')
        content = request.GET['content']
        createTime = datetime.datetime.now()

        ret = CommentBiz.add(userID, goodID, pic, content, createTime)
        key = 'statistic_' + str(goodID)
        print key
        value = DishBiz.getDishStatistic(goodID)
        cache.set(key, value)

        return HttpResponse(ajax_suc_response)
    except KeyError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)


def getComment(request):
    try:
        goodID = int(request.GET['dish_id'])
        beginTime = request.GET.get('begin_time', None)
        if beginTime == None:
            beginTime = datetime.datetime.now()
        else:
            beginTime = datetime.datetime.strptime(beginTime,
                    '%y-%m-%d %H:%M:%S')

        comments = CommentBiz.get(goodID, beginTime)
        return HttpResponse(json.dumps({'ret': 200, 'data': comments}))
    except KeyError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)
    except ValueError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_inllegal_param)


def getFriendComment(request):
    try:
        if not request.user.is_authenticated():
            return HttpResponse(ajax_error_not_login)

        userID = int(request.user.id)
        goodID = int(request.GET['dish_id'])
        beginTime = request.GET.get('begin_time', None)
        if beginTime == None:
            beginTime = datetime.datetime.now()
        else:
            beginTime = datetime.datetime.strptime(beginTime,
                    '%y-%m-%d %H:%M:%S')
        comments = CommentBiz.getFriendComment(goodID, userID,
                beginTime)
        return HttpResponse(json.dumps({'ret': 200, 'data': comments}))
    except KeyError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)
    except ValueError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        return HttpResponse(ajax_error_illegal_param)

def newest(request):
    dishID = request.GET.get('dish_id', None)
    if dishID == None:
       return HttpResponse(ajax_error_illegal_param) 
    
    btime = datetime.datetime.now()
    comment = CommentBiz.get(goodID=int(dishID), beginTime=btime, num=1)
    return HttpResponse(json.dumps({'ret': 200, 'data': comment}))

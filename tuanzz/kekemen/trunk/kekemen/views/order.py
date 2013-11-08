#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template import RequestContext
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from kekemen.settings import MEDIA_PATH

from kekemen.views.common import *
from kekemen.biz.order import OrderBiz
from kekemen.biz.commons import IllegalParamException
from django.template import RequestContext
from kekemen.sns.mongo import OrderMongoDAO
from kekemen.views.forms import UploadFileForm
from kekemen.biz.comment import CommentBiz
from kekemen.biz.feed import FeedBiz
from kekemen.dao.models import *

@login_required
def new(request):
    try:
        userID = request.user.id
        shopID = request.GET['shop_id']
        createTime = datetime.datetime.now()
        oid = OrderBiz.add(userID, shopID, createTime)
        return HttpResponse(json.dumps({'ret': 200, 'order_id': oid}))
    except KeyError, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


@login_required
def addItem(request):
    try:
        userID = request.user.id
        orderID = request.GET['order_id']
        goodID = request.GET['good_id']
        amount = request.GET['amount']
        OrderBiz.addItem(orderID, goodID, amount, userID)
        return HttpResponse(ajax_suc_response)
    except KeyError, err:
        log.error(error)
        return HttpResponse(ajax_error_illegal_param)
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


def updateItem(request):
    try:
        userID = request.user.id
        orderID = request.GET['order_id']
        goodID = request.GET['good_id']
        amount = request.GET['amount']
        OrderBiz.updateItem(orderID, goodID, amount, userID)
        return HttpResponse(ajax_suc_response)
    except KeyError, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


def delItem(request):
    try:
        userID = request.user.id
        orderID = request.GET['order_id']
        goodID = request.GET['good_id']
        OrderBiz.delItem(orderID, goodID, userID)
        return HttpResponse(ajax_suc_response)
    except KeyError, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


def getOrderInfo(request):

    def formatData(x):
        dish = {
            'name': x['gname'],
            'price': x['pe'],
            'pic': x['pic'],
            'discount': x['at'],
            }
        data = {'cont': x['gid'], 'user': x['user'], 'dish': dish}
        return data

    try:
        orderID = request.GET['order_id']
        (data, status) = OrderBiz.get(orderID)
        dataMap = [formatData(x) for x in data]
        return HttpResponse(json.dumps({'ret': 200, 'data': dataMap}))
    except KeyError, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except IllegalParamException, err:
        log.error(err)
        return HttpResponse(ajax_error_illegal_param)
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


from kekemen.biz.order import ChatBiz


def getChat(request):

    def formatData(x):
        data = {'cont': x['cont'], 'user': x['user'], 'time': x['ts']}
        return data

    try:
        orderID = request.GET['order_id']
        chatID = request.GET.get('chat_id', None)
        chats = ChatBiz.get(orderID, chatID)
        chatsMap = [formatData(x) for x in chats]
        response = HttpResponse(json.dumps({'ret': 200, 'data'
                                : chatsMap}))
        maxID = ChatBiz.getMaxChatID(orderID)
        if maxID:
            response.set_cookie(str(orderID), maxID)
        return response
    except BaseException, err:
        log.error(err)
        return HttpResponse(ajax_error_server_failed)


from views.forms import ConfirmOrderForm


def confirm(request):
    if request.method == 'POST':
        form = ConfirmOrderForm(request.POST)
        if form.is_valid():
            OrderBiz.confirm(
                form.orderID,
                form.cleaned_data['expectTime'],
                form.cleaned_data['consumerNum'],
                form.cleaned_data['compartmentRequire'],
                form.cleaned_data['contact'],
                form.cleaned_data['gender'],
                form.cleaned_data['phone'],
                form.cleaned_data['orderType'],
                form.cleaned_data['remark'],
                )
            return render_to_reponse('order_success.html', {'order_id'
                    : form.orderID})
    else:
        orderid = request.GET['order_id']
        form = ConfirmOrderForm(orderID=orderid)
        (order_list, status) = OrderBiz.get(orderid)
        if status != 1:
            return render_to_response('orderid.html', {'error'
                    : u'订单已经成交了'})

            # order status is not new

    context = RequestContext(request)
    return render_to_response('cart.html', {'form': form, 'order_list'
                              : order_list}, context_instance=context)


@login_required
def list(request):
    context = RequestContext(request)
    userID = request.user.id
    orders = OrderBiz.getHisOrder(userID)
    return render_to_response('order_list.html', {'orders': orders}, 
            context_instance=context)


@login_required
def invite(request, orderID):
    shop = OrderBiz.getShop(orderID)
    context = RequestContext(request)
    return render_to_response('invite.html', {'shopID': shop['id'],
                              'orderID': orderID},
                              context_instance=context)

@login_required
def view(request, orderID):
    dishes, status = OrderBiz.get(orderID)
    order = OrderMongoDAO.getSingleOrder(orderID) 
    orderTypeMap = {'1':'包间优先','2':'大厅优先', 
        '3': '只定包间', '4':'只定大厅'}
    
    orderType = orderTypeMap.get(order['detail']['cpt'], '包间优先')
    time = order['basic']['ts'].strftime('%Y-%m-%d, %H:%M:%S')
    count = len(dishes)
    price = 0
    for dish in dishes:
        price += dish['pe'] * dish['at']
        
    context = RequestContext(request)

    return render_to_response('order_view.html', {
            'dishes': dishes, 
            'order': order,
            'time':time,
            'count': count,
            'price': price,
            'orderType': orderType,
            'orderID' : orderID,
            }, 
            context_instance=context
        )

def test( request):
    return render_to_response('test.html')

def save_image(request):
    try:
        if not request.user.is_authenticated():
            return HttpResponse(ajax_error_not_login)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                userID = int(request.user.id)
                content = form.cleaned_data['content']
                dishID = form.cleaned_data['dishID']
                imgfile = form.cleaned_data['imgfile']
                createTime = datetime.datetime.now()
                orderID = form.cleaned_data['orderID']

                register_openers()
                datagen, headers = multipart_encode({ 'imgfile' : imgfile })
                URL = 'http://192.168.1.254/media/add'
                req = urllib2.Request(URL, datagen, headers) 
                imageID = urllib2.urlopen(req).read()
                ret = CommentBiz.add(userID, dishID, imageID, content, createTime)

                #add feed
                dish = Dish.objects.get(dishID = dishID)
                shop = Shop.objects.get(shopID = dish.shop_id)
                feedContent = { 'did': dish.dishID, 'dname' :dish.name,
                    'sid': shop.shopID, 'sname': shop.name,
                    'pic': { 'small': MEDIA_PATH['small'] + imageID, 
                            'middle': MEDIA_PATH['middle'] + imageID, 
                            'large': MEDIA_PATH['large'] + imageID},
                    'content' :content}
                print FeedBiz.add(userID, createTime, 1, 1, feedContent)
                
                #evaluated the order
                OrderMongoDAO.addEvaluate(orderID)
                return HttpResponse(ajax_suc_response)            

    except KeyError, err:
        log.debug(err)
        log.debug(traceback.format_exc())
        
    return HttpResponse(imageID)




from django.template import RequestContext

from django.http import HttpResponse
from kekemen.biz.order import OrderBiz
from kekemen.views.common import *
from django.shortcuts import render_to_response
from kekemen.views.forms import ConfirmOrderForm
from kekemen.biz.order import OrderBiz
from kekemen.sns.constant import *
from kekemen.biz.commons import *
from django.template import RequestContext

import datetime

def confirmShop(request, orderID):
    dishes, status  = OrderBiz.get(orderID)
    if not status:
        raise IllegalParamException('orderID', orderID, 'order not exist')

    if status != CONSTANT_ORDER_STATUS_NEW : 
        raise OrderLockedException(orderID, status)
    context = RequestContext(request)

    OrderBiz.updateStatus(orderID, CONSTANT_ORDER_STATUS_LOCKED)    
    return render_to_response('cart.html',
            {'dishes': dishes, 'orderID': orderID, 
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().strftime('%H:%M:%S')} 
            , context_instance = context)

@login_required
def confirmForm(request, orderID):
    if request.method == 'POST':
        form = ConfirmOrderForm( request.POST )

        if form.is_valid():
            orderID = orderID
            userID = int (request.user.id)
            createTime = datetime.datetime.now()
            consumerNum = form.cleaned_data['consumerNum']
            gender = form.cleaned_data['gender']
            contact = form.cleaned_data['contact']
            phone_num = form.cleaned_data['phone_num']
            order_type = form.cleaned_data['orderType']
            input_date = form.cleaned_data['input_date'].strftime('%Y-%m-%d')
            input_time = form.cleaned_data['input_time'].strftime('%H:%M:%S')
            remark = ""
            compartmentRequire = 1
            time = datetime.datetime.strptime(input_date + input_time, '%Y-%m-%d%H:%M:%S')
            
            OrderBiz.confirm(orderID=orderID, userID=userID, createTime = createTime, 
                    expectTime=time, consumerNum=consumerNum, 
                    compartmentRequire=compartmentRequire, 
                    contact=contact, gender=gender,
                    phone=phone_num, orderType=order_type, 
                    remark=remark)
        else:
            dishes, status = OrderBiz.get(orderID)
            return render_to_response('cart.html', 
                    {"form":form,
                    'dishes': dishes,
                    'orderID': orderID,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.datetime.now().strftime('%H:%M:%S'),
                    })
    message = "success"
    return render_to_response('notify.html', { 'message' : message})

@login_required
def fresh(request, orderID):
    shop = OrderBiz.getShop(orderID)
    print shop
    context = RequestContext(request)
    OrderBiz.updateStatus(orderID, CONSTANT_ORDER_STATUS_NEW)
    return render_to_response('invite.html', {'shopID': shop['id'],
                                'orderID': orderID },
                                context_instance=context)

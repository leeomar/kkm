# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from diancan.models import *
from diancan.forms import *
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import simplejson as json
import datetime, time
import logging
import traceback
import re

logger = logging.getLogger('diancan')

ajax_notlogin_msg = json.dumps({'ret' : u'notlogin'})
ajax_invalid_msg = json.dumps({'ret' : u'格式不正确'})
ajax_fail_msg = json.dumps({'ret' : 'fail'})
ajax_suc_msg = json.dumps({'ret' : 'ok'})

def clear_cache(request):
    cache.clear()
    return HttpResponse('suc clear cache')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        #return HttpResponseRedirect('/product/1/list') # Redirect after POST

        if form.is_valid():
            #save user information
            user = UserInfo()
            user.name = form.cleaned_data['name']
            user.pwd = form.cleaned_data['pwd']
            user.email = form.cleaned_data['email']
            user.createTime = datetime.datetime.now()
            user.lastModifyTime = user.createTime
            user.regionID = Region(regionID = form.data.get('regionID'))
            user.save()

            #save session data
            request.session['login'] = True
            request.session['userID'] = user.userID
            request.session['name'] = user.name
            request.session['regionID'] = form.data.get('regionID')

            return HttpResponseRedirect('/product/' + form.data.get('regionID') + '/list') # Redirect after POST
        else:
            form.fields["regionID"].queryset = Region.objects.filter(parentID = 2)
            render_to_response('register.html', {'form' : form,})
    else:
        form = UserForm()
        form.fields["regionID"].queryset = Region.objects.filter(parentID = 2)

    return render_to_response('register.html', {'form' : form,})

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        redirect = request.POST.get('redirect')
        user = UserInfo.objects.filter(name = name, pwd = pwd)

        if len(user) == 1 : #or len(UserInfo.objects.filter(email = name, pwd = pwd )) == 1:
            #save session
            request.session['login'] = True
            request.session['userID'] = user[0].userID
            request.session['name'] = user[0].name
            request.session['phone'] = user[0].phone or ''
            request.session['address'] = user[0].address or ''
            request.session['regionID'] = user[0].regionID.regionID

            if redirect:
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponseRedirect('/product/'+ str(user[0].regionID.regionID) + '/list')
        else:
            return render_to_response('login.html', {'error' : u'用户名或者密码错误'})

    return render_to_response('login.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/') # Redirect after POST

def index(request):
    regionID = request.session.get('regionID') or 9
    return HttpResponseRedirect('/product/' + str(regionID) + '/list')

@transaction.commit_on_success
def confirm_order(request):
    '''
        confirm orders, this will validate data
        data format:
        {  region : @regionID,
           orders :  { time : { mID : amount, mID2 : ammount2 } }, { time : { mID : ammount } },
        }
        example: {"region":3,"orders":{"2011-05-10":{"3":"1"},"2011-05-11":{"4":"1"}}}
    '''
    if not request.session.get('login', False):
        return HttpResponseRedirect('/user/login')
        #return HttpResponse(ajax_notlogin_msg)

    logger.debug('rec confirm order request')
    try:
        userID = request.session.get('userID')
        #print request
        param = request.POST['data']

        print 'data', param
        orderDic = json.loads(param)
        regionID = int(orderDic['region'])
        multiOrder = orderDic['orders']

        curTime = datetime.datetime.now()
        order = Order( createTime = curTime )

        order.userID = UserInfo.objects.get(pk = userID)
        order.regionID = Region.objects.get(pk = regionID)
        order.phone = order.userID.phone
        order.address = order.userID.address
        #update region info
        oldRegionID = request.session.get('regionID')
        if oldRegionID is None or regionID != oldRegionID :
            order.userID.regionID = order.regionID
            order.userID.save()
            request.session['regionID'] = regionID

        sucAddOrderList = []
        totalPrice = 0
        today = datetime.datetime.now()
        for orderTimeParam, orderItems  in  multiOrder.items():
            orderTime = datetime.datetime.strptime(orderTimeParam, "%Y-%m-%d")
            if orderTime - today > datetime.timedelta(hours = 72) or today - orderTime > datetime.timedelta(hours = 24):
                logger.error('invalid order time %s' % orderTimeParam )
                return render_to_response('success_order.html', {'error' : u'订单时间不在有效期内'})
                #return HttpResponse(errorMsg)

            #order.orderID = None
            tmpID = int(datetime.datetime.now().strftime('%Y%m%d%H%M%f'))
            logger.info('new order %s, userID %s' % (str(tmpID), str(userID)))
            order.orderID = int(tmpID)
            order.expectTime = orderTime #may be unmatch data type
            order.createTime = curTime
            order.save()
            sucAddOrderList.append(tmpID)

            for key, value in orderItems.items():
                dish = Merchandise.objects.get(pk = key, regions__regionID__contains = regionID)
                if dish == None:
                    logger.error('unmatch region(' + str(regionID) + ', ' + str(dish.regionID.regionID) )
                    return render_to_response('success_order.html', {'error' : u'对不起，在您所选的区域没有该菜'})
                    #return HttpResponse(ajax_fail_msg)
                orderItem = OrderDetail(price = dish.price, discount = dish.discount, ammount = int(value))
                orderItem.orderID = order
                orderItem.merchandiseID = dish
                orderItem.total = orderItem.price * orderItem.ammount
                orderItem.save()
                totalPrice += orderItem.total

        print 'price', totalPrice
        return render_to_response('success_order.html', {'userName' :  request.session.get('name'), 'totalPrice' : totalPrice, 'orderIDs' : sucAddOrderList })
        #return HttpResponse(ajax_suc_msg)
    except BaseException, err:
        logger.error(err)
        logger.error(traceback.format_exc())
        return render_to_response('success_order.html', {'error' : u'服务器忙，请稍候重试'})
        #return HttpResponse(ajax_fail_msg)

class SimpleCategory():
    #name = ''
    #dishes = []
    def __init__(self, name, dishes):
        self.name = name
        self.dishes = dishes

    def __unicode__(self):
        return ' '.jion(self.name, self.dishes)

class Districts():
    def __init__(self, districtNum, districts, buildings):
        self.districtNum = districtNum
        self.districts = districts
        self.buildings = buildings

    def __unicode__(self):
        return str(self.districtNum) + self.districts + ' ' + self.buildings

def show_product(request, regionID):
    #init menu information
    try:
        regionID = int(regionID)
        cacheMenuKey = 'region_menu_' + str(regionID)
        menus = cache.get(cacheMenuKey)

        if not menus:
            logger.debug('cache miss, get region(%d) menus' % regionID )
            categorys = Category.objects.all()
            #today = datetime.date.today()
            dayOfWeek = int(datetime.datetime.now().strftime('%w'))
            menus = []
            #[[category1, category2], [category1, category2]]
            for delta in [0, 1, 2]:
                #date = today +  datetime.timedelta(hours = delta)
                date = ( dayOfWeek + delta ) % 7
                merchandiseSet = Merchandise.objects.filter(regions__regionID__contains = regionID, validDate = date )

                logger.debug('menu %s, region %s, %s' % (date, regionID,  merchandiseSet))
                curMenu = []
                for categoryItem in categorys:
                    merchandiseByCategory = merchandiseSet.filter(category = categoryItem)

                    category = SimpleCategory(categoryItem.name, [])
                    #print category
                    #category = SimpleCategory()
                    #category.name = categoryItem.name
                    #category.dishes = []
                    for item in merchandiseByCategory:
                        dish = []
                        dish.append(item.mID)
                        dish.append(item.name)
                        dish.append(item.desc)
                        dish.append(item.price)
                        category.dishes.append(dish)
                    curMenu.append(category)
                    del category
                menus.append(curMenu)
            cache.set(cacheMenuKey, menus)
        else:
            logger.debug('cache hit, get region(%d) menus' % regionID)

        cacheDistrictsKey = 'districts'
        districts = cache.get( cacheDistrictsKey )

        if not districts:
            logger.debug('cache miss, get district information')
            # init business district 

            regions = Region.objects.filter(parentID = 1)
            districtList = [ item.name for item in regions ]
            # init mall
            buildings = []
            for item in regions:
                specialDistrict = Region.objects.filter(parentID = item.regionID)
                regionBuildings = [[item.regionID, item.name] for item in specialDistrict ]
                buildings.append(regionBuildings)

            district = Districts( len(districtList), districtList, buildings)
            cache.set( cacheDistrictsKey, district )
        else:
            logger.debug('cache hit, get district information')

        #init other information
        saleroom = 100 + len(Order.objects.filter(regionID__regionID = regionID))
        curLocation = Region.objects.get(regionID = regionID).name

        #expire time
        todayMenuExpired = False
        if datetime.datetime.today().hour >= 11:
            todayMenuExpired = True

        logger.debug('todayMenuExpired %s ' % todayMenuExpired)
        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'menus' : menus,
            'userName' :  request.session.get('name'),
            'saleroom' : saleroom,
            'districts' : districts,
            'curLocation' : curLocation,
            'phone' : request.session.get('phone', ''),
            'address' : request.session.get('address', ''),
            'todayMenuExpired' : todayMenuExpired,
        })

        #if reqest.session.get('login', False):
        #    contest['userName'] = request.session.get('name')

        return HttpResponse(template.render(context))
    except BaseException, err:
        logger.error(err)
        logger.error(traceback.format_exc())
        return HttpResponse('invalid request')

#cache_page(60 * 15)
def list_order(request):
    try:
        userID = request.session.get('userID')
        logger.debug( 'user(%d) query his order information' % userID )
        orders = Order.objects.filter(userID__userID = userID)
        order_list = [(order, OrderDetail.objects.filter(orderID = order)) for order in orders]
        return render_to_response('user_order.html', {
            'order_list': order_list,
            'userName': request.session.get('name'),
            'phone' : request.session.get('phone', ''),
            'address' : request.session.get('address', ''),
        })
    except BaseException, err:
        logger.error(err)
        logger.error(traceback.format_exc())
        return HttpResponse('server internal error')

reg_phone_pattern = re.compile('(^(\d{11})$|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})$|^(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})$|^(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)')

def modify_contact_info(request):
    try:
        phone = request.GET['phone'].strip()
        address = request.GET['address'].strip()

        logger.debug('modify personal information , phone %s, address %s' % (phone, address))
        if len(phone) < 6 or len(address) < 1 or reg_phone_pattern.match(phone) is None:
            logger.error('fail modify personal information, invalid format, phone %s, address %s' % (phone, address))
            return HttpResponse(ajax_invalid_msg)

        userID = request.session.get('userID')
        user = UserInfo.objects.get(pk = userID)
        user.phone = phone
        user.address = address
        user.save()

        request.session['phone'] = phone
        request.session['address'] = address

        return HttpResponse(ajax_suc_msg)
    except BaseException, err:
        logger.error(err)
        logger.error(traceback.format_exc())
        return HttpResponse(ajax_fail_msg)

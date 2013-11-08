#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding : utf-8

from kekemen.biz.commons import *
from kekemen.biz.relation import UserBiz
from kekemen.settings import MEDIA_PATH
from kekemen.biz.relation import FollowBiz


def clear_cache():
    cache.clear()
    print 'clear cache'


class CategoryBiz:

    @staticmethod
    def get():
        key = 'category_all'
        value = cache.get(key)
        if value == None:
            value = Category.objects.filter(status=1)
            cache.set(key, value)
            log.debug('cache categorys')
        return value


class RegionBiz:

    @staticmethod
    def getBusinessDistrict(regionID):
        key = 'bdistrict_' + str(regionID)
        value = cache.get(key)
        if value == None:
            value = Region.objects.filter(regionType=1,
                    parent__regionID=regionID)
            cache.set(key, value)
            log.debug(' cache business district, reigon %s ' % regionID)
        return value

    @staticmethod
    def getAdministrativeRegion(regionID):
        key = 'aregion_' + str(regionID)
        value = cache.get(key)
        if value == None:
            value = Region.objects.filter(regionType=2,
                    parent__regionID=regionID)
            cache.set(key, value)
            log.debug(' cache administrative region %s' % regionID)
        return value


class ShopBiz:

    @staticmethod
    def search(
        keyword,
        page=1,
        regionID=None,
        categoryID=None,
        ):
        '''
            search shops, return:
            [
                {
                    'id' : ,    #shop ID
                    'name' : ,  #shop name
                    'pic'  : {
                        'large' : ,
                        'middle': ,
                        'small' : ,
                    }
                    'desc' : ,   #shop description
                    'compartment' : ,   #compartment description
                    'tag' : ,   #
                    'address' : ,   #
                    'open' : ,      #open time
                    'close': ,      #close time
                    'avg' : ,       #average consume
                    'statistic' : {
                        'like' : ,      #
                        'eat'  : ,
                        'want' : ,
                        'comment' : ,   #
                    }
                }
            ]
        '''

        shops = Shop.objects.filter(Q(name__contains=keyword)
                                    | Q(address__icontains=keyword))
        if regionID != None:
            shops = shops.filter(region__regionID=regionID)
        if categoryID != None:
            shops = shops.filter(categorys__categoryID=categoryID)

        p = Paginator(shops, 20)
        if page > p.count:
            return ([], 0)

        shop_json_array = []
        for item in p.page(page).object_list:
            shop = {
                'id': item.shopID,
                'name': item.name,
                'desc': item.desc,
                'compartment': item.compartment,
                'tag': item.tag,
                'address': item.address,
                'open': item.openTime.strftime('%H:%M:%S'),
                'close': item.closeTime.strftime('%H:%M:%S'),
                'avg': item.avg,
                }
            pic = {'large': MEDIA_PATH['large'] + item.pic,
                   'middle': MEDIA_PATH['middle'] + item.pic,
                   'small': MEDIA_PATH['small'] + item.pic}
            shop['pic'] = pic
            sdata = VoteMongoDAO.getShopStatistic(item.shopID)
            statistic = {
                'like': sdata.get('lk', 0),
                'eat': sdata.get('et', 0),
                'want': sdata.get('wt', 0),
                'comment': sdata.get('ct', 0),
                }
            shop['statistic'] = statistic
            shop_json_array.append(shop)

        return (shop_json_array, p.count)

    @staticmethod
    def get(shopID):
        key = 'shop_' + str(shopID)
        value = cache.get(key)
        if value == None:
            value = Shop.objects.get(pk=shopID)
            cache.set(key, value)
            log.debug(' cache shop %s' % shopID)
        return value

    @staticmethod
    def getMenu(shopID):
        key = 'shop_menu_' + str(shopID)
        value = cache.get(key)
        if value == None:
            value = Menu.objects.filter(status=1, shop__shopID=shopID)
            cache.set(key, value)
            log.debug('cache menu, shop %s ' % shopID)
        return value

    @staticmethod
    def getStatistic(shopID):
        data = VoteMongoDAO.getShopStatistic(shopID)
        return data

    @staticmethod
    def getCustomer(shopID, userID=None):
        key = 'customer_shop_%s_day_%s' % (shopID,
                datetime.date.today().day)
        value = cache.get(key)
        if value == None:
            users = OrderMongoDAO.getCustomer(shopID)
            value = []
            for uid in users:
                #uid = item['basic']['uid']
                user = UserBiz.getStatisticProfile(uid)
                user['follow'] = True
                value.append(user)
            cache.set(key, value)
            log.debug('cache shop %s customer' % shopID)

        value = FollowBiz.appendIfFollow(userID, value)
        return value


class DishBiz:

    @staticmethod
    def getBasicInfo(dishID):
        dish = DishBiz.getDish(dishID)
        return {'id': dish['dishID'], 'name': dish['detail']['name'],
                'pic': dish['detail']['pic']}

    @staticmethod
    def getDish(dishID):
        '''
            get dish information, return:
            {
                'dishID' : 123, #dish id
                'detail' : {
                    'name' : 'hamburger',   #dish name
                    'desc' : 'discription', #dish description
                    'price' : '',
                    'discount' : '',
                    'tagType' : 1,      #tagType
                    'shopID' : 1,       #shopID
                    'shopName' : 'KFC', #shop name
                    'pic'  : {
                        'large' : ,
                        'middle': ,
                        'small' : ,
                    }
                }
            }
        '''

        try:
            key = 'dish_' + str(dishID)
            value = cache.get(key)
            if value == None:
                dish = Dish.objects.get(pk=dishID)
                value = {'dishID': dishID}
                detail = {
                    'name': dish.name,
                    'desc': dish.desc,
                    'price': dish.price,
                    'discount': dish.discount,
                    'tagType': dish.tagType,
                    'shopID': dish.shop.shopID,
                    'shopName': dish.shop.name,
                    }
                pic = {'large': MEDIA_PATH['large'] + dish.pic,
                       'middle': MEDIA_PATH['middle'] + dish.pic,
                       'small': MEDIA_PATH['small'] + dish.pic}
                detail['pic'] = pic
                value['detail'] = detail
                cache.set(key, value)
                log.debug('cache dish %s, %s' % (dishID, value))

            return value
        except ObjectDoesNotExist, err:
            log.debug(err)
            log.debug(traceback.format_exc())
            raise IllegalParamExceptatisticion('dishID', dishID,
                    'dish not exist')

    @staticmethod
    def getNewDishes(regionID, page=1):
        '''
            get newest dishes in certain area,
            return: ref to DishBiz.ObjectToJson()
        '''

        if page <= 0:
            log.error('invalid page number %d ' % page)
            page = 1
        key = 'newdish_%s_page_%s' % (str(regionID), page)
        value = cache.get(key)

        if value == None:
            dishes = \
                Dish.objects.filter(shop__region__parent__regionID=regionID).distinct().order_by('-createTime'
                    )[:200]

            p = Paginator(dishes, 20)
            if page > p.num_pages:
                raise IllegalParamException(['page', 'num_pages'],
                        [page, p.num_pages],
                        'invalid page number, exceed the max page')

            value = DishBiz.ObjectToJson(p.page(page).object_list)
            cache.set(key, value)
            log.debug('cache new dishes, region %s, page %d'
                      % (regionID, page))
        if value is None:
            return []

        for ele in value:
            ele_key = 'statistic_'+str(ele['dID'])
            ele_value = cache.get(ele_key)
            if ele_value == None:
                ele['statistic'] = DishBiz.getDishStatistic(ele['dID'])
            else:
                ele['statistic'] = ele_value

        return value

    @staticmethod
    def getByMenu(shopID, menuID, page=1):
        '''
            ref to DishBiz.ObjectToJson()
        '''

        key = 'shop_' + str(shopID) + '_menu_' + str(menuID)
        value = cache.get(key)
        if value == None:
            dishes = Dish.objects.filter(status=1, shop__shopID=shopID,
                    menu__menuID=menuID)
            value = DishBiz.ObjectToJson(dishes)
            cache.set(key, value)
            log.debug(' cache menus , shop %s, menu %s' % (shopID,
                      menuID))

        p = Paginator(value, 20)
        if page > p.num_pages:
            raise IllegalParamException('page', page,
                    'invalid page number, exceed the max page')
        return p.page(page).object_list

    @staticmethod
    def ObjectToJson(dishes):
        '''
            convert Dish Objects to Json array,
            return:
            [
                {
                    'dID' : 1, #dish id
                    'rid' : 1, #region id
                    'detail' : {
                        'name' : '', #dish name
                        'price' : '', #dish price
                        'discount' : '', #
                        'shopID' : '', #shop id
                        'shopName' : '', #shop name'
                        'pic'  : {
                            'large' : ,
                            'middle': ,
                            'small' : ,
                        }
                    }
                    'count' : 2, #num of commenters
                    'commenters' : [
                        {
                            'uid' : 1, #user id
                            'pic' : a.jpg,  #picture
                            'un'  : 'lee', #username
                        }
                    ],
                    'statistic' : {
                        'like' : 1,
                        'eat' : 4,
                        'want' : 6,
                        'comment' : 10,
                    }
                }
            ]
        '''

        result = []
        for item in dishes:
            dish = {}
            dish['dID'] = item.dishID

            # get commenters

            ts = datetime.datetime.now()
            comments = CommentMongoDAO.getComment(item.dishID, ts, 5)
            dish['count'] = comments.count()
            commenters = []
            for comment in comments:
                user = UserBiz.getBasicProfile(comment['uID'])
                commenters.append(user)
            dish['commenters'] = commenters

            # get dish detail information

            detail = {}
            detail['name'] = item.name
            detail['price'] = item.price
            detail['pic'] = {'large': MEDIA_PATH['large'] + item.pic,
                             'middle': MEDIA_PATH['middle'] + item.pic,
                             'small': MEDIA_PATH['small'] + item.pic}
            detail['discount'] = item.discount
            detail['shopID'] = item.shop.shopID
            detail['shopName'] = item.shop.name
            dish['detail'] = detail

            # get statistic information

            dish['statistic'] = DishBiz.getDishStatistic(item.dishID)
            result.append(dish)
        return result

    @staticmethod
    def getDishStatistic(dishID):
        '''
            return:
            {
                'like' : 1,
                'eat' : 4,
                'want' : 6,
                'comment' : 10,
            }
        '''

        statisticInfo = VoteMongoDAO.getDishStatistic(dishID)
        if statisticInfo == None:
            statisticInfo = {}
        statistic = {
            'like': statisticInfo.get('lk', 0),
            'eat': statisticInfo.get('et', 0),
            'want': statisticInfo.get('wt', 0),
            'comment': statisticInfo.get('ct', 0),
            }
        return statistic

    @staticmethod
    def getHotDishes(regionID, weight=-1):
        '''
            ref to getNewDishes()
        '''

        key = 'hotdish_%s_weight_%s' % (str(regionID), str(weight))
        value = cache.get(key)

        if value == None:
            value = []
            hotDishes = DishRankingListDAO.getHotDish(regionID, weight)
            log.debug('get hot dish, %s, %d' % (regionID,
                      hotDishes.count()))
            for item in hotDishes:
                commenters = []
                ctrs = item['value']['commenters'].rstrip(',').split(','
                        )
                for userID in ctrs:
                    profile = UserBiz.getBasicProfile(int(userID))
                    commenters.append(profile)
                dishID = int(item['_id'])
                dishDetail = DishBiz.getDish(dishID)
                dish = {
                    'dID': dishID,
                    'rid': item['value']['rid'],
                    'count': item['value']['count'],
                    'weight': item['value']['weight'],
                    'commenters': commenters,
                    'detail': dishDetail['detail'],
                    }
                dish['statistic'] = DishBiz.getDishStatistic(dishID)
                value.append(dish)
            cache.set(key, value)
            log.debug('cache hot dish, region id %s, num %d'
                      % (regionID, len(value)))
        if value is None:
            return []

        for ele in value:
            ele_key = 'statistic_'+str(ele['dID'])
            ele_value = cache.get(ele_key)
            if ele_value == None:
                ele['statistic'] = DishBiz.getDishStatistic(ele['dID'])
            else:
                ele['statistic'] = ele_value
        return value

    @staticmethod
    def search(
        keyword,
        page=1,
        regionID=None,
        categoryID=None,
        ):
        dishes = Dish.objects.filter(Q(name__contains=keyword)
                | Q(shop__name__contains=keyword)
                | Q(shop__address__contains=keyword))
        if regionID != None:
            dishes = dishes.filter(shop__region_regionID=regionID)
        if categoryID != None:
            dishes = \
                dishes.filter(shop__categorys__categoryID=categoryID)

        p = Paginator(dishes, 20)
        if page > p.count:
            return ([], 0)

        TempPages = p.page(page)
        return (DishBiz.ObjectToJson(TempPages.object_list), p.count)



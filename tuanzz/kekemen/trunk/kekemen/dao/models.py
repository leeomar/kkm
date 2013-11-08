#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.conf import settings

# 大整数


class BigIntegerField(IntegerField):

    empty_strings_allowed = False

    def get_internal_type(self):
        return 'BigIntegerField'

    def db_type(self):
        return 'bigint'  # Note this won't work with Oracle.


COMMON_STATUS_CHOICES = ((1, u'有效'), (2, u'无效'))

# 地区信息


class Region(models.Model):

    REGION_TYPE_CHOICES = ((1, u'行政区域'), (2, u'商圈'))

    regionID = models.AutoField(primary_key=True)
    regionType = models.SmallIntegerField(u'类型',
            choices=REGION_TYPE_CHOICES, default=2)
    name = models.CharField(u'区域', max_length=64)
    parent = models.ForeignKey('self', blank=True, null=True,
                               verbose_name=u'上层区域')
    grandparent = models.IntegerField(blank=True, null=True,
            verbose_name=u'顶层区域')
    restaurantNum = models.IntegerField(u'餐厅数量', default=0)
    status = models.SmallIntegerField(u'状态',
            choices=COMMON_STATUS_CHOICES, default=1)
    createTime = models.DateTimeField()


    class Meta:

        verbose_name = u'地区信息'


        # ordering = ["parent"]

    def __unicode__(self):
        return self.name


# 用户信息


class Profile(models.Model):

    # store user's real name in field 'first_name' of User object
    # realName = models.CharField(u'真实姓名', max_length = 64, null = True, blank = True)

    phone = models.CharField(u'手机', null=True, blank=True,
                             max_length=32)
    account = models.FloatField(u'账户', default=0, null=True, blank=True)

    # tips = models.IntegerField(u'积分', default = 0, null = True, blank = True)

    picture = models.CharField(u'头像', max_length=32, null=True,
                               blank=True)
    region = models.ForeignKey(Region, verbose_name=u'城市')
    user = models.OneToOneField(User)


    class Meta:

        verbose_name = u'用户附加信息'


    def __unicode__(self):
        return self.phone

    def user_name(self):
        return self.user.username


# 分类： 湘菜，粤菜，火锅


class Category(models.Model):

    categoryID = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=64)
    restaurantNum = models.IntegerField(u'餐厅数量', default=0)
    status = models.SmallIntegerField(u'状态',
            choices=COMMON_STATUS_CHOICES, default=1)
    createTime = models.DateTimeField(u'创建时间')


    class Meta:

        verbose_name = u'菜系'


    def __unicode__(self):
        return self.name


# 商家信息


class Shop(models.Model):

    shopID = models.AutoField(primary_key=True)
    name = models.CharField(u'商户名称', max_length=128)
    desc = models.CharField(u'餐厅介绍', max_length=256, null=True,
                            blank=True)
    compartment = models.CharField(u'包间描述(有无包间，消费限制)', max_length=64)
    tag = models.CharField(u'标签(,分割)', max_length=64)
    address = models.CharField(u'地址', max_length=512)
    openTime = models.TimeField(u'开始营业时间')
    closeTime = models.TimeField(u'结束营业时间')
    contacts = models.CharField(u'联系人', max_length=32)
    phone = models.CharField(u'电话', max_length=32)
    email = models.EmailField(u'邮箱', null=True, blank=True)
    createTime = models.DateTimeField(u'创建时间')
    status = models.SmallIntegerField(u'状态',
            choices=COMMON_STATUS_CHOICES, default=1)
    rate = models.IntegerField(u'评分', default=0)

    region = models.ManyToManyField(Region, verbose_name=u'所属区域')
    categorys = models.ManyToManyField(Category, verbose_name='所属菜系')
    pic = models.CharField(u'照片', max_length=64, null=True, blank=True)
    avg = models.IntegerField(u'人均')


    class Meta:

        verbose_name = u'商家'


    def __unicode__(self):
        return self.name


# 菜单分类信息


class Menu(models.Model):

    menuID = models.AutoField(primary_key=True)
    name = models.CharField(u'名称', max_length=64)
    shop = models.ForeignKey(Shop, verbose_name=u'所属商家')
    status = models.SmallIntegerField(u'状态',
            choices=COMMON_STATUS_CHOICES, default=1)
    createTime = models.DateTimeField(u'创建时间')


    class Meta:

        verbose_name = u'菜单目录'
        ordering = ['shop']


    def __unicode__(self):
        return self.name


# 菜品信息


class Dish(models.Model):

    SALE_TYPE_CHOICES = ((1, u'原价'), (4, u'折扣销售'), (5, '降价销售'))
    TAG_TYPE_CHOICES = ((1, u'无'), (2, u'新品'), (3, u' 促销'), (4, u'特色'))

    dishID = models.AutoField(primary_key=True)
    name = models.CharField(u'菜名', max_length=128)
    desc = models.CharField(u'介绍', max_length=512, blank=True,
                            null=True)
    price = models.FloatField(u'原价')
    salePrice = models.FloatField(u'特价', default=0)
    discount = models.FloatField(u'折扣', default=1)
    tagType = models.SmallIntegerField(u'标签', default=1)
    saleType = models.SmallIntegerField(u'促销', default=1)
    createTime = models.DateTimeField(u'创建时间')

    menu = models.ManyToManyField(Menu, verbose_name=u'分类')
    shop = models.ForeignKey(Shop, verbose_name=u'店家')
    status = models.SmallIntegerField(u'状态',
            choices=COMMON_STATUS_CHOICES, default=1)

    rate = models.IntegerField(u'评分', default=0)
    pic = models.CharField(u'照片', max_length=64, null=True, blank=True)

    material = models.CharField(u'原料', max_length=256, null=True, blank=True)


    class Meta:

        verbose_name = u'菜'


    def __unicode__(self):
        return self.name


GERDER_CHOICES = ((1, u'先生'), (2, u'女士'), (3, u'公司'))

# 订单信息


class Order(models.Model):

    ORDER_TYPE_CHOICES = ((1, u'自己消费'), (2, u'代人订餐'))
    ORDER_STATUS_CHOICES = ((1, u'新订单'), (2, u'已确认'), (3, u'已付款'), (4,
                            u'完成'), (5, u'作废'))
    ORDER_PLACE_REQUIREMENT_CHOICES = ((1, u'包间优先'), (2, u'大厅优先'), (3,
            u'只定包间'), (4, u'只定大厅'))

    orderID = models.CharField(u'订单号', max_length=32, primary_key=True)
    status = models.SmallIntegerField(u'订单状态',
            choices=ORDER_STATUS_CHOICES, default=1)
    shop = models.ForeignKey(Shop, verbose_name=u'店家')
    user = models.ForeignKey(User, verbose_name=u'下单用户')

    consumerNum = models.PositiveIntegerField(u'就餐人数')
    compartment = models.SmallIntegerField(u'包间要求',
            choices=ORDER_PLACE_REQUIREMENT_CHOICES, default=1)
    contact = models.CharField(u'联系人', max_length=32)
    gender = models.SmallIntegerField(u'性别', choices=GERDER_CHOICES,
            default=1)
    phone = models.CharField(u'电话', max_length=32)

    orderType = models.SmallIntegerField(u'订单类型',
            choices=ORDER_TYPE_CHOICES, default=1)

    # consumer = models.ForeignKey(Consumer, null = True, blank = True)

    remark = models.CharField(u'备注', max_length=128, null=True,
                              blank=True)
    price = models.FloatField(u'价格', default=0)
    expectTime = models.DateTimeField(u'就餐时间')
    createTime = models.DateTimeField(u'订餐时间')


    class Meta:

        ordering = ['-createTime']
        verbose_name = u'订单'


    def __unicode__(self):
        return str(self.orderID)

    def shop_name(self):
        return self.shop.name


# 订餐详细信息


class OrderDetail(models.Model):

    DEFAULT_SHOP_CHOICES = ((1, u'是'), (2, u'否'))
    orderDetailID = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, verbose_name=u'订单号')
    dish = models.ForeignKey(Dish, verbose_name=u'菜')
    price = models.FloatField(u'价格')
    discount = models.FloatField(u'折扣', null=True, default=1)
    ammount = models.PositiveSmallIntegerField(u'份数', default=1)
    total = models.FloatField(u'小计')
    placer = models.ForeignKey(User, verbose_name=u'下单人')


    class Meta:

        verbose_name = u'订单详细'
        ordering = ['order']


    def __unicode__(self):
        return self.dish.name


FOLLOW_BIDIRECTION_CHOICES = ((1, u'false'), (2, u'true'))
STATUS_CHOICES = ((1, u'valid'), (2, u'unvalid'))


class Follow(models.Model):

    ID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    following = models.ForeignKey(User, related_name='fk_follow')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    createTime = models.DateTimeField()


    class Meta:

        unique_together = ('userID', 'following')
        ordering = ['userID']
        verbose_name = u'关注'


    def __unicode__(self):
        return str(self.userID)


class FollowReverse(models.Model):

    ID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    follower = models.ForeignKey(User, related_name='fk_follow_reverse')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    bidirection = \
        models.SmallIntegerField(choices=FOLLOW_BIDIRECTION_CHOICES,
                                 default=1)
    createTime = models.DateTimeField()


    class Meta:

        unique_together = ('userID', 'follower')
        verbose_name = u'反向关注'
        ordering = ['userID']


    def __unicode__(self):
        return str(userID)



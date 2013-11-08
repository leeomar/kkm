# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''
class Address(models.Model):
    ADDRESS_STATUS_CHOICES = ((-1, u'invalid'),(-2, u'deleted'),(1, u'valid'))

    addressID = models.AutoField(primary_key = True)
    userID = models.ForeignKey(UserInfo)
    address = models.CharField(max_length = 256)
    status = models.SmallIntegerField(choices = ADDRESS_STATUS_CHOICES, default = 1)

    def __unicode__(self):
        return self.address
class RecursiveTest(models.Model):
    ID = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 64)
    PID = models.ForeignKey('self',  blank = True, null = True)

    def __unicode__(self):
        return self.name
'''
from django.db.models.fields import IntegerField
from django.conf import settings

class BigIntegerField(IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"

    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.

class Region(models.Model):
    regionID = models.AutoField(primary_key = True, verbose_name = u'区域ID')
    name = models.CharField(u'区域', max_length = 128)
    parentID = models.IntegerField(u'上级区域')
    #parentID = models.ForeignKey('self', blank = True, null = True)
    #userID = models.IntegerField()
    createTime = models.DateTimeField(u'创建时间')
    lastModifyTime = models.DateTimeField(u'修改时间')

    class Meta:
        ordering = ["parentID", "name"]
        verbose_name = u'区域信息'

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    address = models.CharField(max_length = 256, null = True, blank = True)
    phone = models.CharField(max_length = 30)
    account = models.FloatField(default = 0, null = True, blank = True)

    region = models.ForeignKey(Region)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.phone

class UserInfo(models.Model):
    USER_TYPE_CHOICES=((1, u'customer'), (2, u'shoper'), (3, u'manager'))
    USER_STATUS_CHOICES=((-1, u'invalid'),(1, u'valid'))

    userID = models.AutoField(primary_key = True)
    nickName = models.CharField(max_length = 30, null = True, blank = True)
    name = models.CharField(max_length = 30)
    pwd = models.CharField(max_length = 30)
    email = models.EmailField(null = True, blank = True)
    phone = models.CharField(max_length = 30, null = True, blank = True)
    account = models.FloatField(null = True, blank = True, default = 0)
    status = models.SmallIntegerField(choices = USER_STATUS_CHOICES, default = 1)
    u_type = models.SmallIntegerField("user type", choices = USER_TYPE_CHOICES, default = 1)  #type: 1 customer; 2 shop; 3 manager
    createTime = models.DateTimeField()
    lastModifyTime = models.DateTimeField()
    regionID = models.ForeignKey(Region)
    address = models.CharField(max_length = 256, null = True, blank = True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

class Shop(models.Model):
    shopID = models.AutoField(primary_key = True)
    regionID = models.ForeignKey(Region, verbose_name = u'所属区域')
    name = models.CharField(u'名称', max_length = 128)
    desc = models.CharField(u'备注', max_length = 128, null = True, blank = True)
    address  = models.CharField(u'地址', max_length = 512)
    contact = models.CharField(u'联系人', max_length = 32)
    phone = models.CharField(u'电话', max_length = 32)
    mail = models.EmailField(u'邮箱', null = True, blank = True)
    createTime = models.DateTimeField(u'创建时间')
    lastModifyTime = models.DateTimeField(u'修改时间')

    class Meta:
        verbose_name = u'商家'

    def __unicode__(self):
        return self.name

class Category(models.Model):
    categoryID = models.AutoField(primary_key = True)
    name = models.CharField(u'名称', max_length = 64)
    parentID = models.IntegerField(u'上级分类', default = -1)
    #shopID = models.ForeignKey(Shop)
    userID = models.ForeignKey(UserInfo, verbose_name = u'创建者')
    pos = models.IntegerField(u'排序位置', default = 0, null = True, blank = True)
    createTime = models.DateTimeField(u'创建时间')
    lastModifyTime = models.DateTimeField(u'修改时间')

    class Meta:
        ordering = ["pos"]
        verbose_name = u'菜品分类'

    def __unicode__(self):
        return self.name

class Merchandise(models.Model):
    MERCHANDISE_VALID_DATE_CHOICES = ((0, u'星期天'), (1, u'星期一'), (2, u'星期二'), (3, u'星期三'), (4, u'星期四'), (5, u'星期五'), (6, u'星期六'))
    mID = models.AutoField(primary_key = True)
    defaultShopID = models.IntegerField(u'默认商家')
    validDate = models.SmallIntegerField(u'有效日期', default = 0, choices = MERCHANDISE_VALID_DATE_CHOICES )
    beginTime = models.DateField()
    endTime = models.DateField()

    name = models.CharField(u'名称', max_length = 256)
    desc = models.CharField(u'备注', max_length = 2048, blank = True, null = True)
    pic = models.CharField(u'图片', max_length = 1024, null = True, blank = True)
    price = models.FloatField(u'价格')
    discount = models.FloatField(u'折扣', blank = True, null = True, default = 1)
    amount = models.IntegerField(u'库存', default = -1)
    saleroom = models.IntegerField(u'销量', blank = True, null = True, default = 0)
    createTime = models.DateTimeField(u'创建时间')
    lastModifyTime = models.DateTimeField(u'修改时间')
    like = models.IntegerField(u'人气', blank = True, default = 0)
    tags = models.CharField(u'标签', max_length = 256, blank = True)

    category = models.ForeignKey(Category, verbose_name = u'分类')
    shops = models.ManyToManyField(Shop, verbose_name = u'供应商')
    regions = models.ManyToManyField(Region, verbose_name = u'供应区域')

    class Meta:
        ordering = ["price"]
        verbose_name  = u'菜品'

    def __unicode__(self):
        return self.name

class Order(models.Model):
    ORDER_STATUS_CHOICES = ((1, u'新订单'), (2, u'已付款'), (3, u'已处理'), (4, u'完成'), (5, u'作废'))
    orderID = BigIntegerField(u'订单号', primary_key = True)
    status = models.SmallIntegerField(u'订单状态', choices = ORDER_STATUS_CHOICES, default = 1)
    userID = models.ForeignKey(UserInfo, verbose_name = u'用户')
    phone = models.CharField(u'电话', max_length = 30)
    address = models.CharField(u'地址', max_length = 256)
    regionID = models.ForeignKey(Region, verbose_name = u'区域')
    remark = models.CharField(u'备注', max_length = 256, null = True, blank = True)
    price = models.FloatField(u'价格', default = 0)
    expectTime = models.DateTimeField(u'消费时间')
    createTime = models.DateTimeField(u'订餐时间')

    class Meta:
        ordering = ['-createTime']
        verbose_name = u'订单'

    def __unicode__(self):
        return str(self.orderID)

class OrderDetail(models.Model):
    DEFAULT_SHOP_CHOICES = ((1, u'是'), (2, u'否'))
    orderDetailID = models.AutoField(primary_key = True)
    orderID = models.ForeignKey(Order, verbose_name = u'订单号')
    merchandiseID = models.ForeignKey(Merchandise, verbose_name = u'菜单')
    price = models.FloatField(u'价格')
    discount = models.FloatField(u'折扣', null = True, default = 1)
    ammount = models.PositiveSmallIntegerField(u'份数', default = 1)
    total = models.FloatField(u'小计')
    shopID = models.ForeignKey(Shop, null = True, blank = True, verbose_name = u'供应商')
    defaultShop = models.SmallIntegerField(choices = DEFAULT_SHOP_CHOICES, default = 1, verbose_name = u'默认供应商')

    class Meta:
        verbose_name = u'订单详细'
        ordering = ['orderID']

    def __unicode__(self):
        return self.merchandiseID.name

    def user_name(self):
        return self.orderID.userID.name

    def user_phone(self):
        return self.orderID.userID.phone

    def user_address(self):
        return self.orderID.userID.address

    def expect_time(self):
        return self.orderID.expectTime

    def create_time(self):
        return self.orderID.createTime

    user_name.short_description = u'用户名'
    user_name.admin_order_field = 'orderID__userID__name'

    user_phone.short_description = u'电话'
    user_address.short_description = u'送餐地址'
    user_address.admin_order_field = 'orderID__address'

    expect_time.short_description = u'消费时间'
    expect_time.admin_order_field = 'orderID__expectTime'

    create_time.short_description = u'创建时间'
    create_time.admin_order_field = 'orderID__createTime'

#!/usr/bin/python
# -*- coding: utf-8 -*-
from kekemen.dao.models import *
from django.contrib import admin
from django.db.models import Q
import datetime

class RegionAdmin(admin.ModelAdmin):

    list_display = ('name', 'regionID', 'parent', 'createTime',
                'restaurantNum' , 'action')

    search_fields = ['name']
    date_hierarchy = 'createTime'
    readonly_fields = ('createTime', )

    def queryset(self, request):
        return Region.objects.filter(parent=None)


    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs
        ):
        if request.GET.get('regionID', None) != None:
            if db_field.name == 'parent': 
                kwargs['queryset'] = Region.objects.filter(
                        parent=request.GET.get('regionID')
                        )  
            return super(RegionAdmin, self).formfield_for_foreignkey(db_field,
                    request, **kwargs)

        if db_field.name == 'parent':
            kwargs['queryset'] = Region.objects.filter(parent=None)
        return super(RegionAdmin,
                     self).formfield_for_foreignkey(db_field, request,
                **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.createTime = datetime.datetime.now()
        obj.save()

    def action(self, form):
        return "<a href='/admin/dao/region/add/?regionID=%s'>增加商家</a>" %form.regionID
    action.allow_tags = True

class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1


class ShopAdmin(admin.ModelAdmin):

    inlines = [MenuInline]
    list_display = ('name', 'contacts', 'phone', 'address',
            'openTime', 'closeTime', 'rate')

    def formfield_for_manytomany(
        self,
        db_field,
        request,
        **kwargs
        ):
        if db_field.name == 'region':
            kwargs['queryset'] = Region.objects.filter(~Q(parent=None))
        return super(ShopAdmin, self).formfield_for_manytomany(db_field, request,
                **kwargs)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


class OrderAdmin(admin.ModelAdmin):

    list_filter = ['status', 'expectTime']
    list_display = (
        'orderID',
        'shop_name',
        'user',
        'phone',
        'expectTime',
        'createTime',
        'status',
        )
    inlines = [OrderDetailInline]


class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user_name', 'phone', 'region', 'account']

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'createTime', 'shop', 'material')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'createTime', 'restaurantNum')

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'price', 'discount', 'ammount', 'total', 'placer')
# admin.site.register(UserInfo, UserInfoAdmin)
# admin.site.register(Address, )

admin.site.register(Region, RegionAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Profile, ProfileAdmin)

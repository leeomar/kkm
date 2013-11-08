from diancan.models import *
from django.contrib import admin
from kuaidian.excel import to_excel_admin_action
#class AddressInline(admin.TabularInline):
#    model = Address
#    extra = 1

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userID', 'u_type', 'name', 'regionID', 'address', 'account', 'phone', 'status', 'createTime')
    search_fields = ['name']
    list_filter = ['u_type']
    date_hierarchy = 'createTime'
    #inlines = [AddressInline]

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'regionID', 'parentID', 'createTime')
    search_fields = ['name']

#class CategoryInline(admin.TabularInline):
#    model = Category
#    extra = 1

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'phone', 'regionID', 'createTime')
    search_fields = ['name']
    list_filter = ['regionID']
    #inlines = [CategoryInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pos', 'createTime')
    search_fields = ['name']
    #list_filter = ['shopID']

class MerchandiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'validDate', 'price', 'discount','amount', 'saleroom', 'createTime')
    search_fields = ['name']
    list_filter = ['validDate']

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'userID', 'phone', 'address', 'expectTime', 'createTime')
    search_fields = ['orderID']
    list_filter = ['status', 'expectTime']
    inlines = [OrderDetailInline]


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'user_name', 'user_phone', 'user_address', 'merchandiseID', 'price', 'ammount', 'discount', 'total', 'expect_time', 'create_time')
    search_fields = ['orderID__orderID']
    list_filter = ['orderID__expectTime']
    excel_exclude = []
    excel_fields = ['orderID','user_name', 'user_phone', 'user_address', 'merchandiseID', 'price', 'ammount', 'discount', 'total', 'expect_time', 'create_time']
    actions = [to_excel_admin_action]
    #actions = [export_as_csv_action("CSV Export", fields=['orderID', 'user_address', 'merchandiseID'])]

admin.site.register(UserInfo, UserInfoAdmin)
#admin.site.register(Address)
admin.site.register(Region, RegionAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)

#admin.site.register(RecursiveTest)

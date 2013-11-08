#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Forms and validation code
"""

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from kekemen.dao.models import Region
import datetime

ORDER_PLACE_REQUIREMENT_CHOICES = ((1, u'包间优先'), (2, u'大厅优先'), (3,
                                   u'只定包间'), (4, u'只定大厅'))
ORDER_TYPE_CHOICES = ((1, u'自己消费'), (2, u'代人订餐'))
GERDER_CHOICES = ((1, u'先生'), (2, u'女士'), (3, u'公司'))


class ConfirmOrderForm(forms.Form):

    '''
    Form for confirming a new order information
    '''

    contact = forms.CharField(max_length=20)
    phone_num = forms.RegexField(regex=r'^(13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$')
    phone_num_repeat = forms.RegexField(regex=r'^(13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$')
    consumerNum = forms.IntegerField(min_value=1)
    gender = forms.ChoiceField(choices=GERDER_CHOICES)
    orderType = \
        forms.ChoiceField(choices=ORDER_PLACE_REQUIREMENT_CHOICES)
    input_date = forms.DateTimeField(input_formats=('%Y-%m-%d', ))
    input_time = forms.DateTimeField(input_formats=('%H:%M:%S', ))

   # remark = forms.CharField( max_length = 100, required = False )

    def clean_phone_num_repeat(self):
        pwd1 = self.cleaned_data['phone_num']
        pwd2 = self.cleaned_data['phone_num_repeat']
        if pwd1 != pwd2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return pwd2

    def clean_input_date(self):
        input_date = self.cleaned_data['input_date']
        if input_date.date() < datetime.date.today():
            raise forms.ValidationError(u'日期错误')
        return input_date

    def clean_input_time(self):
        input_date = self.cleaned_data.get('input_date', None)
        if input_date is None:
            return self.cleaned_data['input_time']
        input_time = self.cleaned_data['input_time']
        confirm_time = datetime.datetime.now() \
            + datetime.timedelta(minutes=30)
        if self.cleaned_data['input_date'].date() \
            == datetime.date.today() and input_time.time() \
            < confirm_time.time():
            raise forms.ValidationError(u'时间错误')
        return input_time


class UploadFileForm(forms.Form):

    #title = forms.CharField(max_length=50)
    content = forms.CharField()
    dishID = forms.IntegerField( min_value = 1 )
    imgfile = forms.FileField()
    orderID = forms.CharField()


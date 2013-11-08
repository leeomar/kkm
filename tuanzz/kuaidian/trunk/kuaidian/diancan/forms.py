#  -*- coding: utf-8 -*- 
from django.forms import ModelForm
from diancan.models import UserInfo, Region
from django import forms
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = UserInfo
        exclude = ('nickName', 'phone', 'account', 'status', 'u_type', 'createTime', 'lastModifyTime', 'address', 'regionID')
        #fields = ('name', 'pwd', 'email', 'regionID')
    name = forms.CharField(max_length=16, min_length=4)
    pwd = forms.CharField( widget=forms.PasswordInput, max_length=20, min_length=6 )
    confirm_pwd = forms.CharField( widget=forms.PasswordInput, required = True, max_length=20, min_length=6 )
    regionID = forms.ModelChoiceField( required = True, queryset = Region.objects.filter(parentID = 2) )

    #def __init__(self, regionID = 2, *args, **kwargs):
        #print 'init'
        #super(UserForm,self).__init__(*args, **kwargs)
        #self.fields['regionID'].queryset = Region.objects.filter(parentID = 2 )

    def clean_confirm_pwd(self):
        pwd1 = self.cleaned_data['pwd']
        pwd2 = self.cleaned_data['confirm_pwd']
        if pwd1 != pwd2 :
            raise forms.ValidationError(u'两次密码输入不一致')
        return pwd2

    def clean_name(self):
        name =  self.cleaned_data['name']
        if len(UserInfo.objects.filter(name = name)) != 0:
            raise forms.ValidationError(u'该用户名已经存在')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) > 0 and len(UserInfo.objects.filter(email = email)):
            raise forms.ValidationError(u'该邮箱已被注册')
        return email

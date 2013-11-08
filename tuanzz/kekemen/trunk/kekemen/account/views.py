# -*- coding: utf-8 -*- 
# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from kekemen.account.forms import RegistrationForm
from kekemen.account.models import RegistrationProfile
from kekemen.dao.models import Region, Profile
from kekemen.biz.order import OrderBiz
from kekemen.sns.mongo import OrderMongoDAO

@receiver(user_logged_in)
def login_callback(sender, **kwargs):
    #print kwargs['request']
    #print kwargs['user']
    print 'login'

def auth_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect = request.POST.get('next','/home/')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(3000)
                response = HttpResponseRedirect( redirect )
                response.set_cookie('user_id', user.id)
                response.set_cookie('region_id', user.get_profile().region.regionID)
                #return orderlist 
                orders = OrderBiz.getHisOrder(user.id)
                order_list = [ order['id'] for order in orders]
                evaluates = OrderBiz.getEvaluate(order_list)
                response.set_cookie('evaluates' , evaluates)
                return response
            else:
                error = '账户尚未激活，请先激活账户'
        else:
            error = '出错啦:用户名或密码错误'


    #redirect = request.REQUEST.get('next', '/')
    redirect = request.GET.get('next', '/')
    form =  AuthenticationForm()
    template = loader.get_template('registration/login.html')
    context = RequestContext(request, { 'form' : form, 'next' : redirect, 'error' : error })

    
    return HttpResponse(template.render(context))

def auth_register(request):
    if request.method == 'POST':
        form = RegistrationForm( request.POST )
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            region = form.cleaned_data['region']
            new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, 'kuailedian.com')
            #save profile
            profile = Profile(phone = '', region = region, user = new_user)
            profile.save()
            return render_to_response('registration/registration_complete.html')
    else:
        form = RegistrationForm()

    context = RequestContext(request)
    return render_to_response('registration/registration_form.html', { 'form': form }, context_instance=context)

def auth_activate(request, activation_key):
    account = RegistrationProfile.objects.activate_user( activation_key )
    if account:
        print 'activate success, please login'
        return render_to_response('registration/activation_complete.html', {'activated' : True})
    else:
        return render_to_response('registration/activation_complete.html', {'actuvated' : False})

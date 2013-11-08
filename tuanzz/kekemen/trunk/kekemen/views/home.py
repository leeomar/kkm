#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    print 'user ***', request.user.id
    context = RequestContext(request)
    return render_to_response('home.html', context_instance=context)



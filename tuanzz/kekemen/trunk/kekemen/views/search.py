#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding : utf-8

import urllib
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from kekemen.biz.shop import ShopBiz, DishBiz, CategoryBiz, RegionBiz
import logging
import simplejson as json


def search(request):
    page = request.GET.get('page', 1)
    cityID = request.GET.get('city', 1)
    regionID = int(request.GET.get('region', -1))
    categoryID = int(request.GET.get('category', -1))
    stype = request.GET.get('type', 1)
    keyword = request.GET.get('keyword', '')
    pageNum = 0
    categoryDict = {}
    regionDict = {}
    pageDict = {}
    categoryKeys = ['city', 'region', 'keyword']
    regionKeys = ['city', 'category', 'keyword']
    pageKeys = ['city', 'category', 'region', 'keyword']
    for key in request.GET:
        if key in categoryKeys:
            categoryDict[key] = request.GET[key]
        if key in regionKeys:
            regionDict[key] = request.GET[key]
        if key in pageKeys:
            pageDict[key] = request.GET[key]

    categoryURL = urllib.urlencode(categoryDict)
    regionURL = urllib.urlencode(regionDict)
    pageURL = urllib.urlencode(pageDict)
    if stype == 1:  # search shop
        if regionID == -1:
            rID = None
        else:
            rID = regionID
        if categoryID == -1:
            cID = None
        else:
            cID = categoryID
        (results, pageNum) = ShopBiz.search(keyword, page, rID,
                cID)
    else:

          # search dish

        dishBiz = DishBiz()
        (results, pageNum) = DishBiz.search(keyword, page, regionID,
                categoryID)

    categorys = CategoryBiz.get()
    businessDistricts = RegionBiz.getBusinessDistrict(cityID)
    administritiveRegions = RegionBiz.getAdministrativeRegion(cityID)

    template = loader.get_template('search.html')
    context = RequestContext(request, {
        'categorys': categorys,
        'businessDistricts': businessDistricts,
        'administritiveRegions': administritiveRegions,
        'data': results,
        'num_page': pageNum,
        'cur_page': page,
        'keyword': keyword,
        'city': cityID,
        'region_id': regionID,
        'category_id': categoryID,
        'category_url': categoryURL,
        'region_url': regionURL,
        'page_url': pageURL
        })
    return HttpResponse(template.render(context))

def search_info(request):
    cityID = 1
    categorys = CategoryBiz.get()
    businessDistricts = RegionBiz.getBusinessDistrict(cityID)
    administritiveRegions = RegionBiz.getAdministrativeRegion(cityID)

    cats = [ cat.name for cat in categorys]
    bus  = [ bu.name for bu in businessDistricts]
    ads = [ ad.name for ad in administritiveRegions]
        
    return HttpResponse(json.dumps( {'ret': 200, 
                'data': { 'categorys': cats , 
                        'businessDistricts' : bus,
                        'administritiveRegions': ads}
                        }))



# -*- coding: utf-8 -*-
from django.http import HttpResponse
import simplejson as json

def waiting(request):
    return HttpResponse(json.dumps([
                {'userid': 12343,
                 'username': 'lijian',
                 'time': '1111-11-11',
                 'type': 'chat',
                 'content': 'hello123'},
                {'userid': 22344,
                 'username': 'falood',
                 'time': '2222-22-22',
                 'type': 'add',
                 'good_id': '11111',
                 'good_name': 'kaoji',
                 'price': 12,
                 'picture': '00392847192485'},
                {'userid': 22344,
                 'username': 'falood',
                 'time': '2222-22-22',
                 'type': 'add',
                 'good_id': '22222',
                 'good_name': 'jiandan',
                 'price': 8,
                 'picture': '00392803859294'},
                {'userid': 22344,
                 'username': 'lijian',
                 'time': '2222-22-22',
                 'type': 'remove',
                 'good_id': '11111'},
                ]))

def update(request):
    return HttpResponse(json.dumps({
                'userid': request.GET['userid'],
                'username': request.GET['username'],
                'time': request.GET['time'],
                'type': request.GET['type'],
                'content': request.GET['content'] 
                }))

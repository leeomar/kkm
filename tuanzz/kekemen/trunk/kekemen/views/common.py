#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import datetime
import logging
import traceback
import simplejson as json

log = logging.getLogger('project')
ajax_suc_response = json.dumps({'ret': 200})
ajax_error_response = json.dumps({'ret': 400, 'desc': ''})
ajax_error_not_login = json.dumps({'ret': 401, 'desc': 'login required'
                                  })
ajax_error_illegal_param = json.dumps({'ret': 442, 'desc'
        : 'illegal param'})
ajax_error_server_failed = json.dumps({'ret': 443, 'desc'
        : 'server internal error'})

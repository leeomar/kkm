#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding : utf-8

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.core.paginator import Paginator

from django.db.models import Q
from django.db import IntegrityError

from kekemen.dao.models import *
from kekemen.sns.mongo import *
from kekemen.sns.constant import *

import datetime
import logging
import traceback

log = logging.getLogger('project')


class IllegalParamException(Exception):

    def __init__(
        self,
        paramName,
        paramValue,
        cause,
        ):
        Exception.__init__(self)
        self.pName = paramName
        self.pValue = paramValue
        self.cause = cause

    def __str__(self):
        return '%s, (%s : %s)' % (self.cause, self.pName, self.pValue)


class OrderLockedException(Exception):

    def __init__(self, orderID, status):
        Exception.__init__(self)
        self.orderID = orderID
        self.status = status

    def __str__(self):
        return 'order %s is locked, status %s' % (self.orderID,
                self.status)



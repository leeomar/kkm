# -*- coding: utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mongo import *
import datetime, time

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class FeedTest(TestCase):

    def test_add_feed(self):
        #ts = int(time.mktime(datetime.datetime.now().timetuple()))
        for i in range(1, 2):
            ts = datetime.datetime.now()
            FeedMongoDAO.add(123, i, ts, 1, 1, { 'author' : 'tom', 'type' : 21})

    def test_create_index(self):
        FeedMongoDAO.createIndex()
        print 'feed create index'

    def test_get_his_feed(self):
        ts = datetime.datetime.now()
        records = FeedMongoDAO.getHisFeed(123, ts)
        print records.count()
        for record in records:
            print str(record), record['cont']

class CommentTest(TestCase):
    def test_add_comment(self):
        for i in range(1, 2):
            ts = datetime.datetime.now()
            CommentMongoDAO.addComment(123, 333, 'photo.jpg', 'great, looks delicous', ts)
        CommentMongoDAO.createIndex()
        print 'test add comment '

    def test_get_comment(self):
        records = CommentMongoDAO.getComment(333, datetime.datetime.now())
        print records.count()
        for record in records:
            print str(record)
        print 'test get comment'

class VoteTest(TestCase):
    def test_create_index(self):
        VoteMongoDAO.createIndex()
        print 'test add new statistic'

    def test_update(self):
        VoteMongoDAO.like(333)
        VoteMongoDAO.eat(333)
        VoteMongoDAO.want(333)
        VoteMongoDAO.comment(333)
        print 'test update statistic'

    def test_get(self):
        record = VoteMongoDAO.getDishStatistic(333)
        print 'test get statistic ', str(record)

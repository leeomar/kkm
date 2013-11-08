#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from kekemen.relation.models import Conversation
from kekemen.product.models import *

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/shop/(\d+)/", ShowShop),
            (r"/good/(\d+)/", ShowGood),
            (r"/ajax/goods/(\d+)/(\d+)/", AjaxGoods),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.write("hello")

class ShowShop(BaseHandler):
    def get(self, shopid):
        shop = Shop.objects.filter(shopID=shopid)
        categories = Category.objects.filter(shopID=shopid)
        goods = Merchandise.objects.filter(shopID=shopid)
        self.render("shop_index2.html", shop = shop[0], categories = categories, goods = goods)

class ShowGood(BaseHandler):
    def get(self, goodid):
        good = Merchandise.objects.filter(pk=goodid)[0]
        self.render("frame_goods_info.html", good = good)

class AjaxGoods(BaseHandler):
    def get(self, shopid, categoryid):
        goods = Merchandise.objects.filter(shopID=shopid, categoryID=categoryid)
        data = []
        for good in goods:
            data.append(dict(
                pk = good.pk,
                name = good.name,
                pic = good.pic,
                price = good.price,
                )
            )
        self.write(tornado.escape.json_encode(data))
    
def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

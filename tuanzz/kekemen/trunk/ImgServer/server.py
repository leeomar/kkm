#!/usr/bin/env python

import pymongo
from pymongo import objectid
import gridfs
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("server_port", default=8001, type=int)
define("mongodb_server", default="192.168.1.254:27017")
define("mongodb_name", default="imgserver")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/add", AddFile),
            (r"/del/(.+)", DelFile),
            (r"/get/(.+)", GetFile),
        ]
        tornado.web.Application.__init__(self, handlers)

class BaseHandler(tornado.web.RequestHandler):
    def getgridfs(self):
        db = pymongo.connection.Connection(options.mongodb_server)
        gr = gridfs.GridFS(db[options.mongodb_name])
        return gr

class AddFile(BaseHandler):
    def get(self):
        self.write("""<html><body><form enctype="multipart/form-data" action="/add" method="post">
                   <input type="file" name="imgfile" /><input type="submit">
                   </body></html>""")
        
    def post(self):
        gr = self.getgridfs()
        imgfile = self.request.files["imgfile"][0]["body"]
        imgid = gr.put(imgfile)
        self.write(str(imgid))

class DelFile(BaseHandler):
    def get(self, objectid):
        self.write("del")

class GetFile(BaseHandler):
    def get(self, objid):
        gr = self.getgridfs()
        fileid = pymongo.objectid.ObjectId(str(objid))
        imgfile = gr.get(fileid).read()
        self.set_header("Content-Type", "image/jpeg")
        self.write(imgfile)

def main():
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.server_port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

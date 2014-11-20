import sys
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, mast):
        self._mast = mast

    def get(self):
        self.write("GET uri: %s" % self.request.uri)
        #TODO: return code for next branch

    def post(self):
        self.write("POST body: %s" % self.request.body)

class MastServer():
    def __init__(self, port, mast):
        self._port = port
        self._mast = mast
        self._application = tornado.web.Application([
            (r"/", MainHandler, {"mast" : self._mast}),
        ])

    def start(self):
        self._application.listen(self._port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    # Usage: python server.py [port]
    MastServer(sys.argv[1], None).start()
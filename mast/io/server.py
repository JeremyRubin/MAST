import sys
import tornado.ioloop
import tornado.web

##TODO: Store current root of tree execution is occurring on

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, mast):
        self._mast = mast
        self.__IO__ = __IO__()

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

    def get_req(self, data):
        self.__IO__.push(data)

    def exec_on_merkle(self, fun, *args):
        #to exec functions on self._mast
        #Usage: exec_on_merkle(fn_name, arg1, arg2, etc)
        self._mast.fun(*args)

if __name__ == "__main__":
    # Usage: python server.py [port]
    MastServer(sys.argv[1], None).start()
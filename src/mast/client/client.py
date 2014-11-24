import sys, urllib
from tornado.httpclient import HTTPClient, HTTPError
from tornado.httputil import url_concat

#TODO: store list+cache or tree with information on previous execution steps

class MastClient():
    def __init__(self, host, port, mast):
        self._url = "http://%s:%s" % (host, port)
        self._http_client = HTTPClient()
        self._mast = mast

    def connect(self, path, method="GET", data={}):
        url = self._url + path
        body = None
        if method == "GET":
            url = url_concat(url, data)
        elif method == "POST":
            body = urllib.urlencode(data)
        else:
            raise ValueError("Unsupported HTTP method: %s" % method)
        try:
            response = self._http_client.fetch(url, method=method, body=body)
            output = response.body
        except HTTPError as e:
            output = "Error:", e
        return output
 
    def run(self):
        pass #TODO: request and run code from server using self._mast

    def close(self):
        self._http_client.close()

if __name__ == "__main__":
    # Usage: python client.py [host] [port] [path]
    client = MastClient(sys.argv[1], sys.argv[2], None)
    client.connect(sys.argv[3])
    client.close()
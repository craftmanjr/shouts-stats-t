import httplib
import json

class API():

    def __init__(self, host):
        self.conn = httplib.HTTPConnection(host)
        
    def reconnect(self):
        self.conn = httplib.HTTPConnection(host)
    
    def get(self, resource):
        req = self.conn.request("GET", resource )
        res = self.conn.getresponse()
        raw_contents = res.read()
        contents = json.loads(raw_contents)
        return contents

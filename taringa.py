import httplib
import json

class API():

    def __init__(self, host):
        self.conn = httplib.HTTPConnection(host)
    
    def get(self, resource):
        req = self.conn.request("GET", resource )
        res = self.conn.getresponse()
        raw_contents = res.read()
        contents = json.loads(raw_contents)
        return contents


class Taringa():
    _TARINGA_API_HOST = "api.taringa.net"
    _SHOUT_ACTIONS = "/shout/actions/view/"
    _SHOUTS_BY_USER = "/shout/user/view/"
    _USER__ID = "/user/view/"
    _USER__NICK = "/user/nick/view/"
    _USER_FOLLOWINGS = "/user/followings/view/"
    _USER_FOLLOWERS = "/user/followers/view/"

      
    def __init__(self):
        self.api = API(self._TARINGA_API_HOST)
       
    def shout_actions(self, shoutid, trimuser=1, page=1):
        return self.api.get(self._SHOUT_ACTIONS + str(shoutid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&page=" + str(page) )                                            

    def user_shouts(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._SHOUTS_BY_USER + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )

    def user_by_id(self, userid):
        return self.api.get(self._USER__ID + str(userid))

    def user_by_nick(self, nickname):
        return self.api.get(self._USER__NICK + nickname)

    
    def user_following(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._USER_FOLLOWINGS + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )
    
    def user_followers(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._USER_FOLLOWERS + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )


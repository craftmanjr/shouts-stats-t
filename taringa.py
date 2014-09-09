import httplib
import json

intervals = [   'today', 'yesterday',
                'week', 'last-week',
                'month', 'last-month', 
                #sigue.. rever
            ]

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


class Taringa():
    _TARINGA_API_HOST = "api.taringa.net"
    _SHOUT_ACTIONS = "/shout/actions/view/"
    _SHOUTS_BY_USER = "/shout/user/view/"
    _USER__ID = "/user/view/"
    _USER__NICK = "/user/nick/view/"
    _USER_FOLLOWINGS = "/user/followings/view/"
    _USER_FOLLOWERS = "/user/followers/view/"
    _POST_COMMENTS = "/post/comment/view"
    _POST_RECENTS = "/post/recent/view/"
    _POST_POPULARS = "/post/populars/view/"
      
    def __init__(self):
        self.api = API(self._TARINGA_API_HOST)
        
    def reconnect(self):
        self.api.reconnect()
       
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



# Corroborar los parametros completos con la doc de la api, cuando este disponible nuevamente

    def post_comments(self, postid, trimuser=1, page=1):
        return self.api.get(self._POST_COMMENTS  + "?object_id=" + str(postid) +\
                                                    "?trim_user=" + str(trimuser) +\
                                                    "&page=" + str(page) )                                            

    def post_recents(self, category, trimuser=1, page=1, count=None):
        return self.api.get(self._POST_RECENTS  + category +\
                                            ( ("&count=" + str(count)) if count is not None else '') +\
                                            "&trim_user=" + str(trimuser) +\
                                            "&page=" + str(page) )

    #TOPs
    def post_populars(self, interval):
        return self.api.get(self._POST_POPULARS + interval)

class User():
    _USER__ID = "/user/view/"
    _USER__NICK = "/user/nick/view/"
    _USER_FOLLOWINGS = "/user/followings/view/"
    _USER_FOLLOWERS = "/user/followers/view/"    
    
    def __init__(self,api):
        self.api = api
       
    def by_id(self, userid):
        return self.api.get(self._USER__ID + str(userid))

    def by_nick(self, nickname):
        return self.api.get(self._USER__NICK + nickname)

    
    def followings(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._USER_FOLLOWINGS + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )
    
    def followers(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._USER_FOLLOWERS + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )
        

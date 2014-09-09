class Shout():
    _SHOUT_ACTIONS = "/shout/actions/view/"
    _SHOUTS_BY_USER = "/shout/user/view/"
    
    def __init__(self, api):
        self.api = api
        
    def actions(self, shoutid, trimuser=1, page=1):
        return self.api.get(self._SHOUT_ACTIONS + str(shoutid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&page=" + str(page) )                                            

    def by_user(self, userid, trimuser=1, page=1, count=50):
        return self.api.get(self._SHOUTS_BY_USER + str(userid) +\
                                            "?trim_user=" + str(trimuser) +\
                                            "&count=" + str(count) +\
                                            "&page=" + str(page) )

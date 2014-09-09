from api import API
from user import User
from shout import Shout
from post import Post

intervals = [   'today', 'yesterday',
                'week', 'last-week',
                'month', 'last-month', 
                #sigue.. rever
            ]

class Taringa():
    _TARINGA_API_HOST = "api.taringa.net"
      
    def __init__(self):
        self.api = API(self._TARINGA_API_HOST)
        self.shout = Shout(self.api)
        self.user = User(self.api)
        self.post = Post(self.api)
        
    def reconnect(self):
        self.api.reconnect()
       
    def shout_actions(self, shoutid, trimuser=1, page=1):
        return self.shout.actions(shoutid, trimuser, page)


    def user_shouts(self, userid, trimuser=1, page=1, count=50):
        return self.shout.by_user(userid, trimuser, page, count)


    def user_by_id(self, userid):
        return self.user.by_id(userid)

    def user_by_nick(self, nickname):
        return self.user.by_nick(nickname)
    
    def user_following(self, userid, trimuser=1, page=1, count=50):
        return self.user.followings(userid, trimuser, page, count)
        
    def user_followers(self, userid, trimuser=1, page=1, count=50):
        return self.user.followers(userid, trimuser, page, count)
    

# Corroborar los parametros completos con la doc de la api, cuando este disponible nuevamente

    def post_comments(self, postid, trimuser=1, page=1):
        return self.post.comments(postid, trimuser, page)

    def post_recents(self, category, trimuser=1, page=1, count=None):
        return self.post.recent(category, trimuser, page, count)

    #TOPs
    def post_populars(self, interval):
        return self.post.populars(interval)
    

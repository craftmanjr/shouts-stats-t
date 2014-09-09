class Post():
    _POST_COMMENTS = "/post/comment/view"
    _POST_RECENTS = "/post/recent/view/"
    _POST_POPULARS = "/post/populars/view/"    
    
    def __init__(self, api):
        self.api = api      

    def comments(self, postid, trimuser=1, page=1):
        return self.api.get(self._POST_COMMENTS  + "?object_id=" + str(postid) +\
                                                    "?trim_user=" + str(trimuser) +\
                                                    "&page=" + str(page) )                                            

    def recent(self, category, trimuser=1, page=1, count=None):
        return self.api.get(self._POST_RECENTS  + category +\
                                            ( ("&count=" + str(count)) if count is not None else '') +\
                                            "&trim_user=" + str(trimuser) +\
                                            "&page=" + str(page) )

    def populars(self, interval):
        return self.api.get(self._POST_POPULARS + interval)

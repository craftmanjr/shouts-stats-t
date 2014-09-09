import json
from taringa import Taringa
from collections import deque
from pprint import pprint
import sys
import csv


taringa = Taringa()
users  = set()
followings = set()
nextusers = deque()

EXPLORED_USERS_FILE = "usuarios.csv"
STATE_FILE = "state.json"


def nickname_to_id(nick):
    return int( taringa.user_by_nick(nick)["id"] )

def dump_state(uid, cur_depth, depth, users_deq):
    state = {
                "last_userid" : uid,
                "last_depth" : cur_depth,
                "param_depth": depth,
                "queue_state": list(nextusers)
            }
    
    with open( STATE_FILE , 'wb') as f:
        json.dump(state, f)



def explore_followers(initial_users, depth=3 ):

    for iu in initial_users:
        nextusers.appendleft(iu)

    print "user,following"

    while len(nextusers) > 0:
        userid, current_depth = nextusers.popleft()
        users.add( userid )

        try:
            following = taringa.user_following( userid )
        except:
            # Guardar lo obtenido hasta el momento (remover el user actualmente ingresado)
            sys.stderr.write('[ERROR] taringa.user_following' + str(userid) + '\n')
            users.remove(userid)
            dump_state(userid, current_depth, depth, nextusers)
            break

        for user_followed in following:
            #followings.add((userid, user_followed))
            print str(userid) + ',' + str(user_followed)
        
        if current_depth < depth:
            nextusers.extend( map ( lambda y: (y, current_depth + 1),
                                    filter( lambda x: x not in users , following ) ) )


    with open( EXPLORED_USERS_FILE,'wb' ) as f:
        for u in users:
            f.write(str(u) + '\n')




if __name__=='__main__':
    try:
        depth = int(sys.argv[1])
    except:
        depth = 1

    try:
        if sys.argv[2] == '-r':
            resume_session = True
    except:
        resume_session = False

    if resume_session:
        with open( STATE_FILE ,'rb') as f:
            state = json.load(f)
            nextusers = state["queue_state"]
            depth = state["param_depth"]
            initial_users = [  (state["last_userid"],
                                state["last_depth"]) ]

            #Restaurar usuarios explorados
            with open( EXPLORED_USERS_FILE, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for uid in reader:
                    users.add(int(uid))

    else:
        with open("mods",'rb') as f:
            initial_users_nicknames = json.load(f)["mods"]
            initial_users = []
            for nick in initial_users_nicknames:
                initial_users.append( (nickname_to_id(nick), 1) )
    
    explore_followers(initial_users, depth)
import sys
import csv
import httplib
import json
from collections import Counter
from taringa import Taringa
import traceback

taringa = Taringa()

def main(inputfile,R,L):
    actions_rs = []
    actions_like = []
    with open(inputfile,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1]=='reshout':
                actions_rs.append(row)
            elif row[1]=='like':
                actions_like.append(row)

    reshouts = Counter()
    likes = Counter()
    for action in actions_rs:
        reshouts[action[2]] += 1
    for action in actions_like:
        likes[action[2]] += 1

    top10_reshouters = reshouts.most_common(R)
    top10_likers =  likes.most_common(L)

    user_ids = set(zip(*top10_reshouters)[0]).union(set(zip(*top10_likers)[0]))
    userid_username = {}
    for userid in user_ids:
        userid_username[userid] = get_username(userid)

    print "TOP %d Reshouts\n" % R
    for user in top10_reshouters:
        print userid_username[user[0]] + ' : ' + str(user[1])

    print "------------------------------"
    print "\nTOP %d Likes\n" % L
    for user in top10_likers:
        print userid_username[user[0]] + ' : ' + str(user[1])


def get_username(userid):
    try:
        contents = taringa.user_by_id(userid)
    except:
        sys.stderr.write('ERROR obteniendo recurso: datos de usuario (por id)\n')
        sys.stderr.write('userid = ' + str(userid))
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
            
    return contents['nick']

def printhelp():
    print "Modo de uso:\n"
    print "\tpython stats.py archivoCSV R L\n\n"
    print "Muestra un TOP-R de reshouters y TOP-L de likers.\n"
    


if __name__=='__main__':
    try:
        inputfile = sys.argv[1]
        R = int(sys.argv[2])
        L = int(sys.argv[3])
    except:
        printhelp()
        sys.exit(1)

    main(inputfile, R, L)

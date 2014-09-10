import sys
import httplib
import json
import csv
import traceback
from api import Taringa
from collections import Counter

from pymongo import MongoClient
from dateutil.parser import parse

taringa = Taringa()

client = MongoClient()
db = client["taringa_db"]

        
        
def get_and_save_shouts_actions(shoutid_list):   
    shouts_actions = []

    print "Obteniendo acciones sobre shouts"
    for shout_id in shoutid_list:
        shouts_actions += get_shout_actions( shout_id )
       
    actions_collection = db["actions"]
    for d in shouts_actions:
        actions_collection.update({"shouts_populares_id": d["shouts_populares_id"], "action_type": d["action_type"], "owner": d["owner"]}, d, upsert=True)

    return shouts_actions
    

def get_shout_actions( shout_id ):
    actions_list = []
    
    print "Shout #", shout_id
    page = 1
    while True:
        print "Pagina ", page
        try:
            contents = taringa.shout_actions(shout_id,page=page)
        except:
            sys.stderr.write('ERROR obteniendo recurso: historial de acciones sobre un shout\n')
            sys.stderr.write('shoutid = ' + str(shout_id) + "\tpage = " + str(page) + "\n")
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)                
        
        if contents == []:
            break
        
        actions_list += map(lambda x: { "shouts_populares_id": shout_id, "action_type": x["action_type"], "owner": x["owner"], "created": x["created"] }, contents)
        page += 1
    
    return actions_list
    
   
    
   
def get_and_save_shouts():   
        
    #~ populars_today = taringa.shout.populars("today")
    #~ populars_yesterday = taringa.shout.populars("yesterday")
    populars_today = taringa.shout.trends("15m") + taringa.shout.trends("1h")
    populars_yesterday = taringa.shout.trends("3h") + taringa.shout.trends("6h")
    
    populars_today_filteredfields =  map(lambda x: { "_id" : x["id"],  "id": x["id"], "owner":x["owner"], "created": x["created"], "canonical":x["canonical"]},
                                                    populars_today)
    populars_yesterday_filteredfields =  map(lambda x: { "_id" : x["id"],  "id": x["id"], "owner":x["owner"], "created": x["created"], "canonical":x["canonical"]},
                                                    populars_yesterday)
        
    shouts_collection = db["shouts_populares"]
    for d in populars_today_filteredfields:
        shouts_collection.update({'_id':d['_id']}, d, upsert=True)
    for d in populars_yesterday_filteredfields:
        shouts_collection.update({'_id':d['_id']}, d, upsert=True)
    
    return (map(lambda x: x["id"],populars_yesterday_filteredfields + populars_today_filteredfields),
            dict( map(lambda x: (x["id"], x["owner"]),populars_yesterday_filteredfields + populars_today_filteredfields)) )
    
    
def main():
    shoutids, shoutowners = get_and_save_shouts()
    actions = get_and_save_shouts_actions(shoutids)
    
    #~ list__owneraction_action_ownershout = map(lambda x: (x["owner"], shoutowners[x["shouts_populares_id"]], x["action_type"]), actions)
    #~ weights = Counter(list__owneraction_action_ownershout)
    edges = map(lambda x: [x["owner"], shoutowners[x["shouts_populares_id"]], x["action_type"]], actions)
    
    
    #~ edges = map(lambda x: [ x[0],x[1],x[2],weights[x]] , list__owneraction_action_ownershout)
    
    with open("edges_actions_populares-b.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(edges)
    


if __name__=='__main__':
    #~ try:
        #~ outfileCSV = sys.argv[1]
        #~ username = None
        #~ if len(sys.argv) == 3:
            #~ username = sys.argv[2]        
    #~ except:
        #~ print "Indicar el nombre del archivo de salida (.csv)"
        #~ traceback.print_exc(file=sys.stdout)
        #~ sys.exit(1)

    main()

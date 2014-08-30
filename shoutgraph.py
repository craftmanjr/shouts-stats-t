import sys
import httplib
import json
import csv
import traceback
from taringa import Taringa

taringa = Taringa()

USERID_CRAFTMANJR = 6356239   #Se obtiene de aqui: http://api.taringa.net/user/nick/view/TuNickname  (campo "id")

# u.u
FILE_SHOUTS_JSON = "my_shouts.json"
FILE_SHOUTS_IDS_JSON = "my_shouts_ids.json"
FILE_RESHOUTS_JSON = "my_reshouts.json"

def get_shouts(userid):
    my_shouts_list = []
    my_reshouts_list = []
    
    print "Obteniendo shouts..."
    for page in range(1,21):    # = [ 1 .. (21-1) ]
        print "Pagina ", page, " de 20"
        try:
            contents = taringa.user_shouts(userid,page=page)

        except:
            sys.stderr.write('ERROR obteniendo recurso: ultimos shouts de usuario\n')
            sys.stderr.write('userid = ' + str(userid) + "\tpage = " + str(page) + "\n")
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)        

        my_shouts_list += filter(lambda x: int(x["owner"]) == userid, contents)
        my_reshouts_list += filter(lambda x: int(x["owner"]) != userid, contents)

    print "Listo"

    f = open(FILE_SHOUTS_JSON, 'w')
    f.write(json.dumps(my_shouts_list))
    f.close()

    f = open(FILE_RESHOUTS_JSON, 'w')  #No utilizado..aun.
    f.write(json.dumps(my_reshouts_list))
    f.close()


def get_shouts_ids(infile_with_shouts, outfile_with_shouts_ids):
    #Cargo los shouts previamente obtenidos
    with open(infile_with_shouts, 'r') as f:
        shouts = json.load(f)

    shouts_ids_list = []
    for i in shouts:
        shouts_ids_list.append(int(i["id"]))
        
    with open(outfile_with_shouts_ids, 'w') as f:
        f.write(json.dumps( { "ids" : shouts_ids_list } ))
        
        
def get_shouts_actions(infile_with_shouts_ids, file_with_actions_csv):    
    with open(infile_with_shouts_ids, 'r') as f:
        ids = (json.load(f))["ids"]
        
    shouts_actions = []

    print "Obteniendo acciones sobre shouts"
    for shout_id in ids:
        shouts_actions += get_shout_actions( shout_id )

    with open(file_with_actions_csv, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(shouts_actions)
    

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
        
        actions_list += map(lambda x: [shout_id, x["action_type"], x["owner"], x["created"]], contents)
        page += 1
    
    return actions_list
    
    
   
def main(outfileCSV):
    userid = USERID_CRAFTMANJR
    
    #Obtiene los ultimos reshouts del usuario con este userid
    # (como devuelve la api de taringa: en formato json)
    get_shouts(userid)

    #Extrae el id de cada shouts, y genera una lista de ids que almacena en formato json
    get_shouts_ids(FILE_SHOUTS_JSON, FILE_SHOUTS_IDS_JSON)
    
    #Genera un archivo csv:  shoutid,action_type,owner,fecha  (owner es quien ha reshoutedo,likeado,y demas action_type; y fecha es cuando lo hizo)
    get_shouts_actions( FILE_SHOUTS_IDS_JSON, outfileCSV)



if __name__=='__main__':
    try:
        outfileCSV = sys.argv[1]
        main(outfileCSV)
    except:
        print "Indicar el nombre del archivo de salida (.csv)"
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

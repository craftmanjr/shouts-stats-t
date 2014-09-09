from taringa import Taringa
import json
import traceback
import sys

taringa = Taringa()
num_retries = 0
MAX_RETRIES = 10
PAGES = 2000

def progress(msg, msg_final, p, max_val):
    sys.stdout.write(msg + "%d de %d            \r" % (p,max_val))
    if p != max_val:
        sys.stdout.flush()
    else:
        sys.stdout.write(msg_final + "                  \n")
        
        
def getposts_ids(infile):
    with open(infile,'rb') as f:
        firstLine = f.readline()
        firstLine = json.loads(firstLine[1:len(firstLine)-2])
        print  str(firstLine["id"])
        c=0
        for line in f:
            c +=1
            try:
                print json.loads(line[:len(line)-2])["id"]
            except:
                print json.loads(line[1:len(line)-2])["id"]

            



def getposts(outfile):
    with open(outfile,'a+') as f:
        f.write("[")
        for page in range(1,PAGES+1):
            progress("Pagina ","Terminado",page,PAGES)
            do_get = True
            posts = []

            while do_get:
                try:
                    posts = taringa.post_recents('noticias',page=page)
                    do_get = False
                except:
                    do_get = True
                    sys.stderr.write('ERROR obteniendo recurso: historial de acciones sobre un shout\n')
                    sys.stderr.write("page = " + str(page) + "\n")
                    num_retries += 1
                    if num_retries <= MAX_RETRIES:
                        taringa.reconnect()
                        sys.stderr.write("Reintentando\t %d \n" % num_retries)
                    else:
                        f.write("]")
                        traceback.print_exc(file=sys.stdout)
                        sys.exit(1)
            
            if posts == []:
                f.write("]")
                break   
            
            for post in posts:
                f.write(json.dumps(post) + ",\n")

if __name__=='__main__':
    try:
        outfile = sys.argv[1]
    except:
        print "Indicar el nombre del archivo de salida"
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

    #getposts(outfile)
    getposts_ids(outfile)

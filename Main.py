from threading import Thread
from time import sleep
from os import path, walk, urandom
from src import variable as v, webcontrol as wc, functions as f, core, admin
from tinydb import TinyDB, Query

import waitress

core.v = wc.v = f.v = v
wc.core = core

v.db = TinyDB("db.tinydb")
v.query = Query()
v.Log = str(f.datetime.now())[:-7].replace(" ", "_").replace(":","_") + ".txt"

def main():
    #Grant Permission
    if not admin.isuseradmin: admin.runasadmin()

    v.ServerStatus = True
    
    tmp = v.db.get(v.query.secret.exists())
    if tmp: secret = tmp["secret"]
    else:
        secret = str(urandom(24))
        v.db.insert({"secret": secret})

    wc.app.config['SECRET_KEY'] = secret

    webpanel = Thread(target=waitress.serve, args=(wc.app, ), kwargs={"host":v.IPs[v.Hosts], "port":v.port})
    webpanel.setDaemon(True)
    webpanel.start()
    
    coreT = Thread(target=core.init)
    coreT.setDaemon(True)
    coreT.start()

    f.logger("Server is running now!\nUse Ctrl + 'c' to stop.")

    #Terminal

    try:
        while v.ServerStatus:
            sleep(1)
    except KeyboardInterrupt:
        "End"

    f.logger("Shutdowning...")

    v.ServerStatus = False

    core.save()
    
    coreT.join()

if __name__ == '__main__':
    main()

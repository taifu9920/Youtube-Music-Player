from threading import Thread
from time import sleep
from os import path, walk
from msvcrt import kbhit
from src import variable as v, webcontrol as wc, functions as f, core, admin

import waitress

core.v = wc.v = f.v = v
wc.core = core

v.Log = str(f.datetime.now())[:-7].replace(" ", "_").replace(":","_") + ".txt"

def main():
    #Grant Permission
    if not admin.isuseradmin: admin.runasadmin()

    v.ServerStatus = True
    
    wc.app.config['TEMPLATES_AUTO_RELOAD'] = True      
    wc.app.jinja_env.auto_reload = True
    webpanel = Thread(target=waitress.serve, args=(wc.app, ), kwargs={"host":v.IPs[v.Hosts], "port":v.port})
    webpanel.setDaemon(True)
    webpanel.start()
    
    coreT = Thread(target=core.init)
    coreT.setDaemon(True)
    coreT.start()

    f.logger("Server is running now!\nPress anything to close the server.")

    #Terminal

    while v.ServerStatus:
        if kbhit():
            break

    f.logger("Shutdowning...")

    v.ServerStatus = False

    core.save()
    
    coreT.join()

if __name__ == '__main__':
    main()
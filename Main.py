from threading import Thread
from time import sleep
from msvcrt import kbhit
from src import variable as v, webcontrol as wc, functions as f, core, admin

import waitress

core.v = wc.v = f.v = v
wc.core = core

v.Log = str(f.datetime.now())[:-7].replace(" ", "_").replace(":","_") + ".txt"

def Main():
    #Grant Permission
    if not admin.isUserAdmin: admin.runAsAdmin()

    v.ServerStatus = True

    webPanel = Thread(target=waitress.serve, args=(wc.app, ), kwargs={"host":v.IPs[v.Hosts], "port":v.port})
    webPanel.setDaemon(True)
    webPanel.start()
    
    Core = Thread(target=core.Init)
    Core.setDaemon(True)
    Core.start()

    f.logger("Server is running now!\nPress anything to close the server.")

    #Terminal

    while v.ServerStatus:
        if kbhit():
            break

    f.logger("Shutdowning...")

    v.ServerStatus = False

    core.save()
    
    Core.join()

if __name__ == '__main__':
    Main()
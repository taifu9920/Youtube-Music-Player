import os
from datetime import datetime

PathExist = lambda path: os.path.exists(path)
SaveName = lambda: str(datetime.now())[:-7].replace(" ", "_").replace(":","_") + "_playlist.txt"

def logger(msg, code = 0):
    #0 to 4 are available
    FolderInit(v.LoggerPath)
    with open(v.LoggerPath + v.Log, "a+", encoding='UTF-8') as file:
        buffer = "{0} | {1} : {2}".format(v.types[code], datetime.now(), msg)
        print(buffer)
        file.write(buffer + "\n")

def FolderInit(path):
    if not PathExist(path):
        os.makedirs(path)
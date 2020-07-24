import chrome_webstore_download as cwd
import src.crx3Convert as crx3
import os, sys, shutil
defaultPath = "CRX\\"
Temp = "Temp\\"

if not os.path.exists(Temp):
    os.makedirs(Temp)

if not os.path.exists(defaultPath):
    os.makedirs(defaultPath)

url = input("Input your extension url from Google WebStore: ")
Name = cwd.parse(chrome_store_url=url)[1]
cwd.download(url, Temp + Name)

Name = [i for i in os.listdir(Temp) if i.startswith(Name)][0]
CRXPath = defaultPath + Name

crx3.package(Temp + Name, "", CRXPath)

try:
    shutil.rmtree(Temp)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

print("Done.")
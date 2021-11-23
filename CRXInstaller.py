import requests
import src.crx3Convert as crx3
import os, sys, shutil
defaultPath = "CRX\\"
Temp = "Temp\\"

if not os.path.exists(Temp):
    os.makedirs(Temp)

if not os.path.exists(defaultPath):
    os.makedirs(defaultPath)

tmpurl = input("Input your extension url from Google WebStore: ")

url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=38.0&acceptformat=crx3&x=id%3D~~~~~~%26uc"
url = url.replace("~~~~~~", tmpurl.split("/")[6])
r = requests.get(url, allow_redirects=True)
Name = tmpurl.split("/")[5] + ".crx"
with open(Temp + Name, "wb") as file:
    file.write(r.content)

CRXPath = defaultPath + Name

crx3.package(Temp + Name, "", CRXPath)

try:
    shutil.rmtree(Temp)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

print("Done.")
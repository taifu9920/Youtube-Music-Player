import json, src.webplayer as p
from urllib.request import urlopen
from threading import Thread
from src.functions import *
from time import sleep
from shutil import copyfile

#For Loading every Setting and Data
def Init():
    v.Musics = []
    v.titleDB = {}
    v.isPlaying = False
    v.urlNow = ""

    p.v = v ; p.Init()
    #If setting file exist
    if PathExist("setting.txt"):
        with open("setting.txt","r") as file:
            #Load Contents
            v.mode, v.volume = file.read().split()
    #If Youtube Video database exist
    if PathExist("DataBase.txt"):
        with open("DataBase.txt", "r") as file:
            #Load Contents
            v.titleDB = json.loads(file.read())
    #If Saved Playlist exist
    if PathExist("playlist.txt"):
        with open("playlist.txt", "r") as file:
            #Load Contents
            songs = file.read().split()
            if len(songs):
                c = Schedule(PlayList = songs)[0]
                if c[0]:
                    #When Some Songs are failed to Load
                    logger("{0} Songs are Failed To load".format(c[0]), 2)
                    if c[1]:
                        v.isPlaying = False
        
    if not len(v.Musics): Next_Process(v.HomePage)
    p.NoSuvery()
    logger("Loading Finished!")
    Player()

def Schedule(URL = "", vID = "", PlayList = None):
    #Process One URL Schedule
    if not PlayList:
        if URL: vID = URL[32:] if URL.startswith("https://www.youtube.com/watch?v=") else URL[17:] if URL.startswith("https://youtu.be/") else URL
        if vID in v.Musics or v.urlNow[32:] == vID or vID == v.HomePage: return 0
        if vID:
            name = getTitle(vID)
            if name:
                v.Musics.append(vID)
                if not v.isPlaying: Next(v.mode)
                logger(vID + " | " + name +  " Add to Queue Success!", 3)
                return 1
        return 0
    #Process Multiple URL Schedule
    else:
        count = [0, 0]
        songs = [[], []]
        for i in PlayList:
            r = Schedule(URL = i)
            count[r] += 1 ; songs[r].append(i)
        if v.mode == "Loop" and count[1] > 0: v.Musics.append(v.Musics.pop(0))
        return count, songs

def Next(mode):
    v.isPlaying = True
    if len(v.Musics):
        logger("Next Song!")
        p.RunScript("window.stop();")
        Next_Process(v.Musics[0])
        logger("Now playing : " + getTitle(v.Musics[0]))
        if v.mode == "Loop": v.Musics.append(v.Musics.pop(0))
        else: v.Musics.pop(0)
    else:
        Next_Process(v.HomePage)
        v.isPlaying = False
        logger("Queue is empty!")

def Next_Process(vid): v.urlNow = "https://www.youtube.com/watch?v=" + vid

def Player():
    while v.ServerStatus:
        try:
            sleep(0.2)
            #Switching Videos
            if p.CurrentURL() != v.urlNow: 
                p.LoadURL(v.urlNow)
                p.WaitElement(Id = "movie_player")
                p.WaitElement(Id = "toggle")
                p.WaitElement(Tn = "video")
                p.RunScript("a = document.getElementById('movie_player')")
            #If in HomePage, make it Loop
            if not v.isPlaying and p.CurrentURL()[32:] == v.HomePage and p.RunScript("return document.getElementsByTagName('video')[0].getAttribute('loop') == null"): p.RunScript("document.getElementsByTagName('video')[0].setAttribute('loop', '')")
            #Remove 'are you there' popup
            try:
                if p.GetElement(Tn = "ytd-popup-container"): p.RunScript("document.getElementsByTagName('ytd-popup-container')[0].remove()")
            except Exception: "Nothing"
            #Save Time information
            try: v.CurrentTime, v.DurationTime = p.RunScript("return [a.getCurrentTime(), a.getDuration()]")
            except Exception: "Nothing"
            #Volume Sync
            try:
                if p.RunScript("return a.getVolume()") != v.volume: p.RunScript("a.setVolume(%s)" % v.volume)
            except Exception: "Nothing"
            #Disable auto play
            try: 
                if p.RunScript("return document.getElementById('toggle').active"): p.GetElement(Id = "toggleButton").click()
            except Exception: "Nothing"
            
            statchk = p.RunScript("return a.getPlayerState()")
            
            if v.isPlaying and statchk == 0: Next(v.mode)
            elif statchk == 2: p.RunScript("a.click()")
            elif statchk in [-1, 5]:
                if statchk == -1: p.RunScript("a.click()") ; statchk = p.RunScript("return a.getPlayerState()")
                if statchk != 1:
                    while p.RunScript("return document.getElementById('movie_player').getPlayerState()") in [5, -1]:
                        logger(p.RunScript("return document.getElementsByClassName('reason')[0].textContent"))
                        logger(p.RunScript("return document.getElementsByClassName('subreason')[0].textContent"))
                        logger("Removed from playlist : " + v.urlNow[32:])
                        v.titleDB[v.urlNow[32:]] = ""
                        if v.mode == "Loop": v.Musics.remove(v.urlNow[32:])
                        Next(v.mode)
                        p.LoadURL(v.urlNow)
                        try:
                            p.WaitElement(Id = "movie_player")
                            p.RunScript("a = document.getElementById('movie_player')")
                        except TimeoutException:
                            "Nothing"
        except Exception as e:
            try:
                p.RunScript("a = document.getElementById('movie_player')")
                if "Cannot read property 'textContent' of undefined" in str(e):
                    "Needed to wait extension process it a little"
                else:
                    logger(e, 1)
            except Exception as e:
                logger(e, 2)
                raise
    v.browser.quit()
    
def getTitle(vID):
    if vID in v.titleDB: return v.titleDB[vID]
    try:
        title = json.load(urlopen("https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=" + vID))["title"]
        v.titleDB[vID] = title
        return title
    except Exception as e:
        logger(e, 1)
        logger("Fetch Failed! - " + vID)
        v.titleDB[vID] = ""
        return ""
        
def save():
    FolderInit("backups")
    fn = SaveName()
    if v.isPlaying:
        with open("playlist.txt", "w") as file:
            if v.mode == "Queue": file.write("\n".join([v.urlNow[32:]] + v.Musics))
            else: file.write("\n".join([v.Musics[-1]] + v.Musics[:-1]))
        copyfile("playlist.txt","backups\\" + fn)
    else:
        with open("playlist.txt", "w") as file:
            "Empty"
    with open("setting.txt", "w") as file:
        file.write("{0}\n{1}".format(v.mode, v.volume))
    with open("DataBase.txt", "w") as file:
        file.write(json.dumps(v.titleDB))
    return fn
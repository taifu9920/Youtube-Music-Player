from flask import Flask, request, render_template, url_for
from random import shuffle
from time import time
from datetime import datetime, timedelta
from src.functions import *
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='../templates/static', template_folder='../templates')

CSRFProtect(app)

HomeButton = "<p></p><button class='w3-btn w3-blue' id='Home'>Home</button>"
ReturnButton = "<p></p><button class='w3-btn w3-blue' id='Return'>Return</button>"
CopyButton = " <button class='w3-btn w3-green' id='CopyButton'>Copy<span class='Popup'>Copied</span></button>"
version = "3.0"
Reloader = lambda a, b: "<script>setTimeout('setupTimer({0}, {1})',300);</script>".format(a, b)
clearDelay = {}
shuffleDelay = {}

incoming = lambda req: logger("Incoming connection from {0}, target page {1}".format(req.remote_addr, req.path), 1)

@app.route("/", methods=['GET', 'POST'])
def Controller():
    incoming(request)
    if request.method == "POST":
        datas = request.form
        if datas.get("Mode"):
            ChangeMode("Queue" if v.mode == "Loop" else "Loop")
        elif datas.get('playlists', "").strip():
            count, songs = core.Schedule(PlayList = datas.get('playlists').strip().split())
            feedback = "<h5>Successfully added %d Songs</h5><h5>Listing below:</h5>" % count[1]
            feedback += "<h5>".join(songs[1]) + "</h5><h5>%d Songs failed to add:</h5>" % count[0]
            feedback += "<h5>".join(songs[0]) + "</h5>"
            return render_template("Message.html", Title = "System Message", Message= feedback, Button = HomeButton, Version = version)
    return render_template("index.html", Current_Mode = v.mode, Version = version)
        
@app.route("/Admin", methods=['GET', "POST"])
def Admin():
    incoming(request)
    datas = request.form
    if datas.get('Admin') == v.AdminPass:
        if datas.get('cmd') == "clear":
            v.Musics = [] ; v.isPlaying = False
            core.Next(v.mode)
            return render_template("Message.html", Title = "System Message", Message= "<h5>Queue cleared!</h5>", Button = HomeButton, Version = version)
        elif datas.get('cmd') == "shutdown":
            v.ServerStatus = False
            return render_template("Message.html", Title = "System Message", Message= "<h5>Shutting down...</h5>", Version = version)
        elif datas.get('cmd') == "shuffle":
            shuffle(v.Musics)
            return render_template("Message.html", Title = "System Message", Message= "<h5>Randomize Shuffled!</h5>", Button = HomeButton, Version = version)
        elif datas.get('cmd') == "reset":
            clearDelay, shuffleDelay = {}, {}
            return render_template("Message.html", Title = "System Message", Message= "<h5>All cooldown has been reset!</h5>", Button = HomeButton, Version = version)
        elif datas.get('cmd') == "save": return render_template("Message.html", Title = "System Message", Message= "<h5>Everything Saved</h5>", Button = HomeButton, Version = version)
        else: return render_template("Admin.html", Title = "Admin Control Panel", Button = HomeButton, Version = version, Code = datas['Admin'] )
    return render_template("Message.html", Title = "System Message", Message= "<h5>Incorrect datas!</h5>", Button = HomeButton, Version = version)

@app.route("/Shuffle")
def Shuffle():
    incoming(request)
    IP = request.remote_addr
    delay = int(time()) - shuffleDelay.get(IP, 0)
    if delay < 300: return render_template("Message.html", Title = "System Message", Message= "<h5>Still in cooldown!</h5><h5>" + str(timedelta(seconds=300 - delay)) + "</h5>", Button = HomeButton, Version = version)
    else:
        shuffle(v.Musics)
        shuffleDelay[IP] = int(time())
        return render_template("Message.html", Title = "System Message", Message= "<h5>Randomize Shuffled!</h5>", Button = HomeButton, Version = version)

@app.route("/Playlist")
def Playlist():
    incoming(request)
    if v.isPlaying:
        ls = "<table id='CopyHere'>"
        if not v.urlNow[32:] in v.Musics: ls += "<tr><th class='w3-center'><h5>" + v.urlNow + "</h5></th></tr>"
        for i in v.Musics: ls += "<tr><th class='w3-center'><h5>" + "https://www.youtube.com/watch?v=" + i + "</h5></th></tr>"
        return render_template("Message.html", Title = "System Message", Message= ls + "</table>", Button = HomeButton + CopyButton, Version = version)
    return render_template("Message.html", Title = "System Message", Message= "<h5>No songs are playing!</h5>", Button = HomeButton, Version = version)

@app.route("/Clear")
def Clear():
    incoming(request)
    IP = request.remote_addr
    delay = int(time()) - clearDelay.get(IP, 0)
    if delay < 300: return render_template("Message.html", Title = "System Message", Message= "<h5>Still in cooldown!</h5><h5>" + str(timedelta(seconds=300 - delay)) + "</h5>", Button = HomeButton, Version = version)
    if v.isPlaying:
        v.isPlaying = False ; v.Musics = []
        clearDelay[IP] = int(time())
        core.Next(v.mode)
        return render_template("Message.html", Title = "System Message", Message= "<h5>Queue cleared!</h5>", Button = HomeButton, Version = version)
    return render_template("Message.html", Title = "System Message", Message= "<h5>Already empty!</h5>", Button = HomeButton, Version = version)

@app.route("/Switch")
def Switch():
    incoming(request)
    ChangeMode(request.args.get("Mode"))

def ChangeMode(mode):
    if mode in ["Queue", "Loop"]:
        if v.isPlaying:
            if mode == "Loop":
                if not v.urlNow[32:] in v.Musics: v.Musics.append(v.urlNow[32:])
            elif v.urlNow[32:] in v.Musics: v.Musics.remove(v.urlNow[32:])
        v.mode = mode
        return render_template("Message.html", Title = "System Message", Message = "<h5>Changed to " + mode + " Success!</h5>", Button = HomeButton, Version = version)
    else:
        return render_template("Message.html", Title = "System Message", Message = "<h5>Mode must be 'Queue' or 'Loop'</h5>", Button = HomeButton, Version = version)

@app.route("/Queue")
def Queue():
    incoming(request)
    s = time()
    if v.isPlaying:
        ls = "<h5>Current Playing : <a href=" + v.urlNow +">" + core.getTitle(v.urlNow[32:]) + "</a></h5>"
        ls += "<table><tr><th class='w3-center'><h5>Current : <span id='CurrentTime'>" + str(v.CurrentTime) + "</span></h5></th><th class='w3-center'><h5>Duration : <span id='DurationTime'>" + str(v.DurationTime) + "</span></h5></th></tr></table>"
        if not len(v.Musics):
            return render_template("Message.html", Title = "System Message", Message = Reloader(v.CurrentTime, v.DurationTime) +  ls + "<h5>Queue is empty!</h5><h5>Time wasted : " + str(timedelta(seconds=time() - s)) + "</h5>", Button = HomeButton, Version = version)
        else:
            ls += "<table>"
            for i, o in enumerate(v.Musics, start=1): ls += "<tr><th>" + str(i) + "</th><th><a href=https://www.youtube.com/watch?v=" + o +">" + core.getTitle(o) + "</a></th></tr>"
            return render_template("Message.html", Title = "System Message", Message = Reloader(v.CurrentTime, v.DurationTime) +  ls + "</table><h5>Time wasted : " + str(timedelta(seconds=time() - s)) + "</h5>", Button = HomeButton, Version = version)
    return render_template("Message.html", Title = "System Message", Message = "<h5>No song in queue yet!</h5>", Button = HomeButton, Version = version)

@app.route("/Skip")
def Skip():
    incoming(request)
    if v.isPlaying:
        core.Next(v.mode)
        if v.isPlaying: return render_template("Message.html", Title = "System Message", Message= "<h5>Skipped!</h5>", Button = HomeButton, Version = version)
        else: return render_template("Message.html", Title = "System Message", Message= "<h5>Skipped, Queue is now empty</h5>", Button = HomeButton, Version = version)
    return render_template("Message.html", Title = "System Message", Message = "<h5>No songs are playing right now!</h5>", Button = HomeButton, Version = version)
        
@app.route("/Remove")
def Remove():
    incoming(request)
    s = time()
    if v.isPlaying:
        data = request.args
        if data.get("Remove") in v.Musics: 
            try: v.Musics.remove(data.get("Remove"))
            except: "Nothing"
        ls = "<h5>Current Playing : <a href=" + v.urlNow +">" + core.getTitle(v.urlNow[32:]) + "</a></h5>"
        ls += "<table><form><input type='hidden' name='csrf_token' value='{{ csrf_token() }}'/><tr><th class='w3-center'><h5>Current : <span id='CurrentTime'>" + str(v.CurrentTime) + "</span></h5></th><th class='w3-center'><h5>Duration : <span id='DurationTime'>" + str(v.DurationTime) + "</span></h5></th></tr></table>"
        ls += "<h5>Listing " + str(len(v.Musics)) + " songs in queue :</h5><table>"
        for i, o in enumerate(v.Musics, start=1): ls += "<tr><th>" + str(i) + "</th><th><a href=https://www.youtube.com/watch?v=" + o +">" + core.getTitle(o) + "</a></th><th><button class='w3-bar-item w3-button' type='submit' name='Remove' value='{0}'>X</button></th></tr>".format(o)
        ls += """</form></table><h5>Time wasted : """ + str(timedelta(seconds=time() - s)) + "</h5>"
        return render_template("Message.html", Title = "System Message", Message= Reloader(v.CurrentTime, v.DurationTime) + ls, Button = HomeButton, Version = version)
    return render_template("Message.html", Title = "System Message", Message= "<h5>No song is playing nor in queue!</h5>", Button = HomeButton, Version = version)
    
@app.route("/Volume")
def Volume():
    incoming(request)
    vol = request.args.get("vol")
    if vol:
        try:
            vol = int(vol)
            if vol <= 100 and vol >= 0:
                v.volume = vol
                return render_template("Message.html", Title = "System Message", Message= "<h5>Volume set to {0} Success</h5>".format(vol), Button = ReturnButton, Version = version)
        except:
            return render_template("Message.html", Title = "System Message", Message= "<h5>Volume must be a number!</h5>", Button = HomeButton, Version = version)
    return render_template("Volume.html", Title = "System Message", VolumeNow = v.volume, Button = HomeButton, Version = version)
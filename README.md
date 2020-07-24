# Youtube-Music-Player
### Self Hosting a Music Player for Youtube via Chrome Driver and Flask in Python
This project is made to deal with some peoples like me,  
who liked to play Music in Youtube by HTTP remote control,  
(or mostly let friends to control together)  
And create more functions for the playlist.  

P.S there're Logo, titles of RMH, which is named for my personal team, Change it whatever you liked uwu  
Current Version: 3.0.0
## How To Install:
#### 1. Install Python 3, And this only support Windows for now
 * (I only tested **Windows 10** for this, Not sure if **Windows xp, 7 or 8** or other supports too) 
#### 2. Go inside `Setup` folder, run command `pip install -r requirements.txt`
#### 3. After this installing, back to the root folder.
#### 4. You can now open `Main.py` to run this program
#### 5. When running, You can go to the control panel `http://localhost:1487` (port 1487 by default, you can change it by setting)
## How To Setting:
This file `src/variable.py` contains all the setting you can change easily.  
Like your playlist saving Path, The Home Page of this Music Player, Where to save logs, even your own Admin Code.  
At beginning I recommand you change the port into something else, And you can also decide if letting Internet access to your Music Player or not.  
***
After Your first run, Few files and folders will be generates.  
The `setting.txt` are also the current setting for Music Player,  
You can change the default values in `src/variable.py` too if you need.  
## How to Install Extension:
#### 1. Open `CRXInstaller.py`, It should shows `Input your extension url from Google WebStore:`
#### 2. Enter your URL for Extension
#### 3. It should be downloading, after that, It'll automatically puts into `CRX/`
## Files:
| Name | Type | Detail |
| --------------- | --------------- | --------------- |
| Setup | Folder | Contains all setup files for Installing necessary packages. |
| Src | Folder | Contains other required functions to make Main.py work. |
| Templates | Folder | Has the HTML Control Panel files for HTTP access. |
| CRXInstaller.py | Python Executable | An easier way to install Chrome Extension by pasting link into it. |
| Main.py | Python Executable | The entry point of this program. |  
## Extra Files After First Run:
| Name | Type | Detail |
| --------------- | --------------- | --------------- |
| CRX | Folder | You can put any CRX 3 files inside, It'll automatically Loaded Every Time you run |
| backups | Folder | Store auto backups for the playlists. |
| Logs | Folder | Store every connection and message in your Music Player |
| Profile | Folder | Store User data for Chrome Driver. |
| DataBase.txt | Text File | Store Datas about Youtube Videos for quicker access. |  
| playlist.txt | Text File | Store your last playlist. |
| setting.txt | Text File | Store your last setting. |  
## Planning Updates:
> * Play now Button, Because some peoples wish to play their song after schedule it.
> * Interface to Change current playlist orders.
> * Make it supports adding other languages.
> * Admin Code cooldown.
> * Make it supports VLC Player instead of ChromeDriver
## Something else:
If there are ads stucking this Music Player, You can put extensions to fix it, Or buy yourself a premium, which is the best way to support Youtube.

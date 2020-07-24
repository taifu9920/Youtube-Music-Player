# Youtube-Music-Player
***
### Self Hosting a Music Player for Youtube via Chrome Driver and Flask in Python
This project is made to deal with some peoples like me,  
who liked to play Music in Youtube by HTTP remote control,  
(or mostly let friends to control together)  
And create more functions for the playlist.  
## How To Install:
### 1. Install Python 3, And this only support Windows for now
 * (I only tested **Windows 10** for this, Not sure if **Windows xp, 7 or 8** or other supports too) 
### 2. Go inside `Setup` folder, run command `pip install -r requirements.txt`
### 3. After this installing, back to the root folder.
### 4. You can now open `Main.py` to run this program
## How To Setting:
### This file `src/variable.py` contains all the setting you can change easily.
### Like your playlist saving Path, The Home Page of this Music Player, Where to save logs, even your own Admin Code.
### At beginning I recommand you change the port into something else, And you can also decide if letting Internet access to your Music Player or not.
***
### After Your first run, Few files will be generates, And Some folders too.
### The `setting.txt` are also the current setting for Music Player,
### You can change the default values in `src/variable.py` too if you need.
## How to Install Extension:
### 1. Open `CRXInstaller.py`, It should shows `Input your extension url from Google WebStore:`
### 2. Enter your URL for Extension
### 3. It should be downloading, after that, It'll automatically puts into `CRX/`
## Files:
<table>
    <tr>
        <td>Name</td>
		<td>Type</td>
		<td>Detail</td>
	</tr>
    <tr>
        <td>Setup</td>
		<td>Folder</td>
		<td>Contains all setup files for Installing necessary packages.</td>
	</tr>
    <tr>
        <td>Src</td>
		<td>Folder</td>
		<td>Contains other required functions to make Main.py work.</td>
	</tr>
    <tr>
        <td>Templates</td>
		<td>Folder</td>
		<td>Has the HTML Control Panel files for HTTP access.</td>
	</tr>
    <tr>
        <td>CRXInstaller.py</td>
		<td>Python Executable</td>
		<td>An easier way to install Chrome Extension by pasting link into it.</td>
	</tr>
    <tr>
        <td>Main.py</td>
		<td>Python Executable</td>
		<td>The entry point of this program.</td>
	</tr>
</table>
## Extra Files After First Run:
<table>
    <tr>
        <td>Name</td>
		<td>Type</td>
		<td>Detail</td>
	</tr>
    <tr>
        <td>CRX</td>
		<td>Folder</td>
		<td>You can put any CRX 3 files inside, It'll automatically Loaded Every Time you run</td>
	</tr>
    <tr>
        <td>backups</td>
		<td>Folder</td>
		<td>Store auto backups for the playlists.</td>
	</tr>
    <tr>
        <td>Logs</td>
		<td>Folder</td>
		<td>Store every connection and message in your Music Player</td>
	</tr>
    <tr>
        <td>Profile</td>
		<td>Folder</td>
		<td>Store User data for Chrome Driver.</td>
	</tr>
    <tr>
        <td>DataBase.txt</td>
		<td>Text File</td>
		<td>Store Datas about Youtube Videos for quicker access.</td>
	</tr>
    <tr>
        <td>playlist.txt</td>
		<td>Text File</td>
		<td>Store your last playlist.</td>
	</tr>
    <tr>
        <td>setting.txt</td>
		<td>Text File</td>
		<td>Store your last setting.</td>
	</tr>
</table>
## Planning Updates:
> * Play now Button, Because some peoples wish to play their song after schedule it.
* Interface to Change current playlist orders.
* Finding more program problems to avoid.
## Something else:
### If there are ads stucking this Music Player, You can put extensions to fix it, Or buy yourself a premium, which is the best way to support Youtube.

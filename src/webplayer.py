from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.functions import *

import chromedriver_autoinstaller as cd_ai


Title = ["container","style-scope ytd-video-primary-info-renderer"]
Player = "ytp-time-display"

RunScript = lambda script: v.browser.execute_script(script)
CurrentURL = lambda: v.browser.current_url

def init():
    #Chrome driver updates
    cd_ai.install()
    
    #Folders Init
    FolderInit(v.ProfilePath)
    FolderInit(v.ExtensionPath)
    
    #Chrome Options
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=" + os.path.abspath(v.ProfilePath))
    
    #CRX loads
    
    for fn in [f for f in os.listdir(v.ExtensionPath) if os.path.isfile(os.path.join(v.ExtensionPath, f))]:
        chrome_options.add_extension(v.ExtensionPath + fn)
    v.browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capa)
    #Init Web Driver Wait
    v.elementWait = WebDriverWait(v.browser, 7)
    
    #Make it only 1 Window tab
    for i in range(len(v.browser.window_handles)-1):
        v.browser.close()
        v.browser.switch_to.window(v.browser.window_handles[0])

def LoadURL(URL):
    v.browser.get(URL)
    WaitElement(Id = "movie_player")
    RunScript("a = document.getElementById('movie_player')")

def NoSuvery():
    try: 
        if GetElement(Cn = "style-scope ytd-single-option-survey-renderer"): GetElement(Id = "button").click()
    except Exception: "Nothing"
    
def GetElement(Id = "", Cn = "", Tn = ""):
    if Id: return v.browser.find_element_by_id(Id)
    elif Cn: return v.browser.find_element_by_class_name(Cn)
    elif Tn: return v.browser.find_element_by_tag_name(Tn)
    else: return None
    
def WaitElement(Id = "", Cn = "", Tn = ""):
    if Id: v.elementWait.until(EC.presence_of_element_located((By.ID, Id)))
    elif Cn: v.elementWait.until(EC.presence_of_element_located((By.CLASSNAME, Cn)))
    elif Tn: v.elementWait.until(EC.presence_of_element_located((By.TAG_NAME, Tn)))
    else: logger("Waiting no Element", 2)
import praw
from prawcore.exceptions import NotFound
from praw.models import Redditor
from praw.models.reddit.submission import Submission
import random
from time import sleep
import threading
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import undetected_chromedriver as uc
import fake_useragent as fua


######################################################
##################### PARAMETERS #####################
######################################################


N_TRIES = 3
N_POSTS = 3 # Nb of posts to upvote (the X most recent posts for each target will be upvoted)
N_UPVOTES = random.randint(20,30) # Choose how many bots to use randomly (here: between 20 & 30)


######################################################
##################### PARAMETERS #####################
######################################################

WAIT = int(3600/N_UPVOTES)
PROXY = "socks5://localhost:9050"

os.chdir(os.path.dirname(__file__))

with open("./targets.txt") as f:
    targets = f.readlines()

targets = [k.strip() for k in targets]

with open("./Comptes-reddit-Aged.txt") as f:
    bots = f.readlines()

bots = [k.strip().split(":") for k in bots]
bots = random.sample(bots , N_UPVOTES)

print(f"Number of bots used: {len(bots)}\nNumber of target accounts: {len(targets)}")

api_username, api_password, api_client_id, api_client_secret = "No-Caterpillar7445","abcdefgh","LLYeM_fsC2eaOj8OH7Rbnw","kstHYpJHdrebwAZERtKTd4Ueh0Y82g"


def login(bot: list, s1=1, s2=3):

    #get reddit account creation page
    browser.set_window_size(1483, 744)
    browser.get('https://old.reddit.com/login')

    sleep(random.random()*(s2-s1) + s1)
    browser.find_element(By.ID, 'user_login').click()
    browser.find_element(By.ID, 'user_login').send_keys(bot[0])

    sleep(random.random()*(s2-s1) + s1)

    browser.find_element(By.ID, 'passwd_login').click()
    browser.find_element(By.ID, 'passwd_login').send_keys(bot[1])
    sleep(random.random()*(s2-s1) + s1)

    browser.find_elements(By.CSS_SELECTOR, ".c-btn.c-btn-primary.c-pull-right")[1].click() # Sign in

def get_sub_info(s: Submission):
    d={}
    d["pinned"] = s.pinned
    d["date"] = s.created
    d["url"] = s.url
    d["title"] = s.title
    
    if len(d["title"]) > 30:
        d["title_trunc"] = d["title"][:27]+"..."
    else:
        d["title_trunc"] = d["title"]
        
    return(d)

def cupvote(url: str):
    browser.get(url)
    upvotes = browser.find_elements(By.XPATH, '//button[@aria-label="Upvote"]') # Upvote
    if upvotes == []:
        upvotes = browser.find_elements(By.XPATH, '//button[@aria-label="upvote"]') # Lowercase 'u'
    upvote_button = upvotes[0]
    is_pressed = upvote_button.get_attribute("aria-pressed") == "true"
    if not is_pressed:
        upvote_button.click()
        print("---> Upvoted !")
    else:
        print("---> Post already upvoted")

def logout():
    sleep(1)
    browser.get('https://old.reddit.com/')
    sleep(1)
    try:
        browser.find_elements(By.XPATH, '//a[@onclick="$(this).parent().submit()"]')[0].click() # Log out
    except IndexError:
        pass

def new_options():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    ua = fua.FakeUserAgent().chrome
    options.add_argument(f"--user-agent={ua}")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    return(options)


"""
options = ChromeOptions()

ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

browser = webdriver.Chrome(options)

browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"})
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})"""


reddit = praw.Reddit(
    client_id=api_client_id,
    client_secret=api_client_secret,
    user_agent="test",
    username=api_username,
    password=api_password
)

### Problème fenêtre "intérêts"

try:
    for bot in bots:
        print(f"\nLogging in with {bot[0]}")
        
        options = new_options()
        
        browser = uc.Chrome(options=options) #headless=True,use_subprocess=False
        
        login(bot, 1, 3) # Se
        
        for target in targets:
            redditor = Redditor(reddit, target)
            
            try:
                n_posts = len(list(redditor.submissions.new()))
            except NotFound:
                print(f"Redditor {target} not found, passing...")
                continue
            print(f"Found Redditor {target} with {n_posts} posts")
            post=0
            
            for submission in redditor.submissions.new():
                
                thread_info = get_sub_info(submission)
                date_format = datetime.utcfromtimestamp(int(thread_info["date"])).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"Upvoting thread \"{thread_info['title']}\" posted on {date_format} ...")
                if not(thread_info["pinned"]) and 'https://www.reddit.com/r/' in thread_info["url"]:
                    for _ in range(N_TRIES):
                        try:
                            upvote(thread_info["url"]) # Se
                            
                        except ElementClickInterceptedException:
                            input("Element Click Intercepted, fix window then press enter")
                            continue
                        break
                else:
                    print("---> Thread is already pinned")
                post+=1
                if post == N_POSTS:
                    break
        
        print("Logging out...")
        browser.close()
        # logout() #Se
        
        k=random.randint(0,30)-10
        print(f"Waiting {WAIT+k} seconds...")
        # sleep(WAIT + k)
        sleep(3)


except KeyboardInterrupt:
    input("Interrputed, press enter to exit...")
except Exception as e:
    print(e)
    input("The error above occured, press enter to exit...")


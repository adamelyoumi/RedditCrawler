#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from random import randint
from time import sleep
import os

os.chdir(os.path.dirname(__file__))

with open("./comptes.txt") as f:
    targets = f.readlines()

targets = [k.strip() for k in targets]

with open("./bots.txt") as f:
    bots = f.readlines()

bots = [k.strip().split(" ") for k in bots]

bots=[k for k in bots if (len(k) == 4)]

print(f"Number of available bots: {len(bots)}\nNumber of target accounts: {len(targets)}")


test_thread = "https://www.reddit.com/r/AskFrance/comments/14w63o5/%C3%AAtesvous_pour_ou_contre_lentr%C3%A9e_de_la_turquie/"
username, password = "No-Caterpillar7445", "abcdefgh"
username2, password2 = "Mysterious-Skill-832", "abcdefgh"

options = ChromeOptions()
# options.set_preference("network.proxy.type", 1)
# options.set_preference("network.proxy.socks", '192.168.0.1')
# options.set_preference("network.proxy.socks_port", 9050)
# options.set_preference("network.proxy.socks_remote_dns", True)
# options.update_preferences()
browser = webdriver.Chrome(options=options)

#get reddit account creation page
browser.set_window_size(1083, 744)
browser.get('https://old.reddit.com/login')

sleep(randint(1,3))
browser.find_element(By.ID, 'user_login').click()
browser.find_element(By.ID, 'user_login').send_keys(username)

sleep(randint(1,3))

browser.find_element(By.ID, 'passwd_login').click()
browser.find_element(By.ID, 'passwd_login').send_keys(password)
sleep(randint(1,3))

browser.find_elements(By.CSS_SELECTOR, ".c-btn.c-btn-primary.c-pull-right")[1].click() # Sign in
sleep(randint(1,3))

browser.get(test_thread)

browser.find_elements(By.XPATH, '//button[@aria-label="Upvote"]')[0].click() # Upvote
sleep(randint(1,3))

browser.get('https://old.reddit.com/')
browser.find_elements(By.XPATH, '//a[@onclick="$(this).parent().submit()"]')[0].click() # Log out

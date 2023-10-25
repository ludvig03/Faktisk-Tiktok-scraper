import pymongo
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random
import re
from pathlib import Path
import os
import datetime
from datetime import datetime, timedelta
import re
import sys
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument('--headless')

def scrape(bruker):

    #convert feks 1.2M til 1200000
    def convert_til_ekte_tall(tall):
        if isinstance(tall, int) or isinstance(tall, float):
            return tall
        if "M" in tall:
            tall = tall.replace('M', '')
            tall = float(tall) * 1000000
        elif "K" in tall:
            tall = tall.replace('K', '')
            tall = float(tall) * 1000
        elif tall == "":
            tall = 0
        else:
            tall = float(tall)
        return tall


    with open(f"./brukere/{bruker}/data/links.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)


    driver = webdriver.Chrome(options=options)

    #Laster inn brukeren sin profilz
    driver.get(f"https://www.tiktok.com/@{bruker}")

    time.sleep(3)

    def scrape_script():

        try:
            har_spilleliste = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[2]/div[2]/p[1]')
            har_spilleliste = True
        except:
            har_spilleliste = False

        print("Bruker har spilleliste: " + str(har_spilleliste))

        #Definerer pausetiden mellom hvert scroll
        SCROLL_PAUSE_TIME = 5

        vids = driver.find_elements(By.CLASS_NAME, 'tiktok-x6y88p-DivItemContainerV2.e19c29qe9')
        state = "tiktok"
        if len(vids) == 0:
            vids = driver.find_elements(By.CLASS_NAME, 'css-1wrhn5c-AMetaCaptionLine.eih2qak0')
            state = "css"
        try:
            display_name = driver.find_element(By.CLASS_NAME, 'tiktok-10pb43i-H2ShareSubTitle.ekmpd5l7')
        except:
            display_name = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[1]/div[2]/h2')

        following_count = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[1]/strong')
        folowers_count = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[2]/strong')
        likes_count = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[3]/strong')
        try:
            user_desc = driver.find_element(By.CLASS_NAME, 'tiktok-4ac4gk-H2ShareDesc.e1457k4r3')
        except:
            user_desc = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h2')

        displayname, following_count, followers_count, likes_count, desc = display_name.text, int(convert_til_ekte_tall(following_count.text)), int(convert_til_ekte_tall(folowers_count.text)), int(convert_til_ekte_tall(likes_count.text)), user_desc.text


        # Henter høyden på nettsiden
        last_height = driver.execute_script("return document.body.scrollHeight")
        antall_scrapet = 0
        # Scroller ned til bunnen av nettsiden

        while True:
            for i in range(5):
                    # Scroller ned til bunnen av nettsiden
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Venter på at siden skal laste inn
                time.sleep(SCROLL_PAUSE_TIME)

                # Regner ut ny høyde på nettsiden og sjekker om den er lik den gamle
                new_height = driver.execute_script("return document.body.scrollHeight")
                antall_scrapet += 35
                print("Antall scrapet: " + str(antall_scrapet))
                print("Antall forsøk: " + str(i+1))
                if new_height != last_height:
                    print("Scroller videre")
                    break
            if new_height == last_height:
                print("Ferdig med å scrolle")
                break

            last_height = new_height


        videoer = []

        print(state)

        links = driver.find_elements(By.CLASS_NAME, 'tiktok-1wrhn5c-AMetaCaptionLine.eih2qak0')
        for link in links:
            link = link.get_attribute('href')
            print(link)
            videoer.append({"url": link})

        if len(videoer) <= 2:
            print("runing")
            link = driver.find_elements(By.TAG_NAME, 'a')
            for l in link:
                if "video" in l.get_attribute('href') and bruker in l.get_attribute('href'):
                    videoer.append({"url": l.get_attribute('href')})
                    print(l.get_attribute('href'))
                    break

        newpath = f'./brukere/' + bruker + '/videos'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        newpath = f'./brukere/' + bruker + '/data'
        if not os.path.exists(newpath):
            os.makedirs(newpath)


                            
        with open(f"./brukere/{bruker}/data/links.json", mode='r', encoding='utf-8') as f:
            vid_data = json.load(f)
            vid_data.append({"displayname": displayname, "following_count": following_count, "followers_count": followers_count, "likes_count": likes_count, "desc": desc, "videoer": videoer})
        with open(f"./brukere/{bruker}/data/links.json", mode='w', encoding='utf-8') as f:
            json.dump(vid_data, f, indent=4, ensure_ascii=False)

    scrape_script()






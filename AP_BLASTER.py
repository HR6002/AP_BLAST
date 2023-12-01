from selenium import webdriver
#from Screenshot import Screenshot_Clipping
import random
from PIL import Image
import time
import requests 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import httplib2
import urllib.parse 
from selenium.webdriver.firefox.options import Options
import os












def web_blast(url, keyword, sleep): #load up website on virtual web browser allows all JS elements to load and then downloads the code and searches fpr keword
                                    # time indicates how many times do you want to check in a day/month ect  on what interval 
    while True:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.implicitly_wait(45)
        page_source = driver.page_source
        driver.quit()
        if keyword.lower() in page_source.lower():
            return True
        print('Executed web blast successfully but no results')
        time.sleep(sleep)



def ss_blast(url, keyword, sleep): #takes a screenshot by loading it up on a virtual browser and runs OCR using API and then search for keyword
                                    # time indicates how many times do you want to check in a day/month ect  on what interval 
                                    #api is free for only first 12000 requests 

    while True:

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        banner_element = driver.find_element(By.CSS_SELECTOR, "div.container-YcqJ8")
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(0.5)
        driver.execute_script("arguments[0].style.display = 'none';", banner_element)
        filename = f"screenshot{random.randint(0,100)}.png"
        driver.save_screenshot(filename)
        driver.quit()

        payload = {'isOverlayRequired': False,
                'apikey': 'K85612556788957',
                'language': 'eng',
                }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                            files={filename: f},
                            data=payload,
                            )
        text= r.content.decode()
        print(text)
        if keyword.lower() in text.lower():
            return True 
        time.sleep(30)  
        os.remove(filename)
        print('Executed ss blast successfully but no results')
        time.sleep(sleep)


def bloomberg_bl_blast(keyword, sleep):
    while True:
            for i in range (121000, 123000):
                response = requests.get(f'https://careers.bloomberg.com/job/detail/{i}')
                if response.status_code >= 200 and response.status_code < 300:
                    response = requests.get(f'https://careers.bloomberg.com/job/detail/{i}')
                    if keyword.lower() in response.text.lower():
                        return True 
                    print('Executed Bloomberg bl blast successfully but no results ')
                    time.sleep(sleep)
                print('website unresponsive')
                time.sleep(sleep)
                                    # this is pretty common sense it bruteforces through every directory and if it finds one that is online it downloads the SC and check for Keyword
                                    # cloudflare and other tech may block this 




def notification(noti_title, noti_msg, users):
    for i in users:
        conn = httplib2.Http()
        url = "https://api.pushover.net/1/messages.json"
        params = {
            "token": "av8yh8kpvv88yf7hfq1q67cwtzs346",
            "user": i ,
            "message": f"{noti_title}: {noti_msg}",
            'sound':'siren'
        }
        headers = { "Content-type": "application/x-www-form-urlencoded" }
        response, content = conn.request(url, "POST", body=urllib.parse.urlencode(params), headers=headers)

        # Optionally, you can print the response for debugging purposes
        print(content.decode('utf-8'))





user_lists=['unnc7gja3ettbdm75chgtt51fkndvw']


def blast1():
    while True: 
        try:
            if web_blast('https://careers.bloomberg.com/job/search?el=Apprenticeships', 'Level 6', 21600): #defult time is set to 21600 meaning every 6 hours a day it check 
                    print("apprenticeship found!")
                    notification('APPRENTICESHIP FOUND!', 'APPRENTICESHIP FOUND', user_lists)
        except:
            print('web_blast -- failed' )


def blast2():
    while True:

        try:

            if ss_blast('https://careers.bloomberg.com/job/search?el=Apprenticeships&qf=Level+6', 'Digital and Technology', 21600):
                    print('Apprenticeship Found')
                    notification('APPRENTICESHIP FOUND!', 'APPRENTICESHIP FOUND', user_lists)
        except:
            print('ss_blast --Failed')



def blast3():
    while True: 
        try:
            if bloomberg_bl_blast('Level 6', 21600):
                print('Apprenticeship Found')
                notification('APPRENTICESHIP FOUND!', 'APPRENTICESHIP FOUND', user_lists)
        except:
            print('bloomberg_bl_blast -- Failed')


# try and except cuz some of them may reach their limit and break 
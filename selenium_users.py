from selenium import webdriver
import pickle
import json
from webob import Response
from textblob import TextBlob
import re
import time
from flask import jsonify
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1200x600')
#url=input("Enter the URL for the Facebook Profile : ")
email = "larisoncarvalho@gmail.com"
password="nineth@2017"
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()
def user_view(name):
    # name = request.urlvars['name']
    posts=[]
    try:
        #driver.set_page_load_timeout(5)
        # driver.get("https://www.facebook.com")
        driver.get("https://www.facebook.com/"+name)
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    finally:
    #    assert "Facebook – log in or sign up" in driver.title
        # elem = driver.find_element_by_id("email")
        # elem.send_keys(email)
        # elem = driver.find_element_by_id("pass")
        # elem.send_keys(password)
        # elem.send_keys(Keys.RETURN)
        driver.get("https://www.facebook.com/"+name)
        actions = ActionChains(driver)
        actions.click()

        actions.perform()
        SCROLL_PAUSE_TIME = 2

    # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1)
        elem = driver.find_elements_by_css_selector("._1dwg._1w_m")
        profileimg = driver.find_element_by_css_selector(".profilePic.img")
        posts.append({'profileimage':profileimg.get_attribute("src")})
        #date=driver.find_element_by_id("js_v").text
        #for i in profileimg:
             
        #print(elem)
        
        for i in elem:
            try:
                result = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", i.text.replace("\n"," "))
                analysis = TextBlob(result)
                posts.append({'ts':i.find_element_by_class_name("timestampContent").text,'text':i.text.replace("\n"," "),'rating':analysis.sentiment.polarity})
            except:
                continue
        
        time.sleep(5)
        print(posts[5])
        driver.close()
        return jsonify(posts)
        

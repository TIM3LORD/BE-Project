from selenium import webdriver
import pickle
import json
from webob import Response
from textblob import TextBlob
import re
import time
import configparser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

config = configparser.ConfigParser()
config.read('config.ini')

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
#url=input("Enter the URL for the Facebook Profile : ")
email = config['FACEBOOKLOGIN']['email']
password=config['FACEBOOKLOGIN']['password']
driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

    
try:
#driver.set_page_load_timeout(5)
    driver.get("https://www.facebook.com")
finally:
    #    assert "Facebook – log in or sign up" in driver.title
    elem = driver.find_element_by_id("email")
    elem.send_keys(email)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    driver.close()
        
        

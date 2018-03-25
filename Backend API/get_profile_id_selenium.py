from selenium import webdriver
from webob import Response

import time
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
#url=input("Enter the URL for the Facebook Profile : ")
def get_id(name):
    url = "https://www.facebook.com/"+name
    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Chrome()
    try:
        #driver.set_page_load_timeout(7)
        driver.get("https://findmyfbid.com/")
    finally:
        # assert "Find my Facebook ID" in driver.title
        elem = driver.find_element_by_name("url")
        elem.send_keys(url)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        new_url =str(driver.current_url)
        return (new_url.split("success/")[1])
        

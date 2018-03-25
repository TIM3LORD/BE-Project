from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS, cross_origin
from userstreaming import post_view
from selenium_users import user_view
from groups import scrapeGroups
from using_scraper import scrapeFacebookPageFeedStatus
from get_profile_id_selenium import get_id  
import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini')

##Facebook API keys
fb_app_id = config['FACEBOOK']['fbappid']
fb_app_secret = config['FACEBOOK']['fbappsecret']  # DO NOT SHARE WITH ANYONE!
group_id = config['FACEBOOK']['fbgroupid']
page_id = config['FACEBOOK']['fbpageid']
access_token = fb_app_id + "|" + fb_app_secret

app = Flask(__name__)
CORS(app)

@app.route('/twitter/<string:name>', methods=['GET'])
def twitter(name):
     x=post_view(name)
     return x

@app.route('/fbuser/<string:name>', methods=['GET'])
def facebook_users(name):
     x=user_view(name)
     return x

@app.route('/fbgroup/<int:id>', methods=['GET'])
def facebook_group(id):
     x=scrapeGroups(group_id,access_token,"","")
     return x

@app.route('/fbpage/<int:id>', methods=['GET'])
def facebook_page(id):
     x=scrapeFacebookPageFeedStatus(page_id,access_token,"","")
     return x


if __name__ == '__main__':
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        app.run(host="127.0.0.1",port=8000)

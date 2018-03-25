import tweepy
from webob import Response
import datetime
from datetime import date
import configparser
from time import localtime, strftime, sleep
now = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['TWITTER']['ckey']
consumer_secret = config['TWITTER']['csecret']
access_key = config['TWITTER']['atoken']
access_secret = config['TWITTER']['asecret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def check(name):
    checkPassed=0
    user = api.get_user(name)
    if(user.verified):                                                      #if account is verified
        return(0)
    # print ("screen name : ",user.screen_name)
    # print ("followers count : ",user.followers_count)
    # print ("following count : ",user.friends_count)
    try:
        x=user.needs_phone_verification
    except:
        # print("Phone not verified")
        checkPassed=checkPassed+1                                                           #phone number not verified
    # print ("post count : ",user.statuses_count)
    try:
        x=user.profile_image_url
    except:
#        print("No profile picture present")
        checkPassed=checkPassed+1
    # print ("favourites count : ",user.favourites_count)
    # print ("Account creation date : ",user.created_at)
    #print (user)
    c_date=str(user.created_at).split(" ")[0]
    c_date=c_date.split("-")
    d0 = date(int(c_date[0]),int(c_date[1]),int(c_date[2]))
    d1 = date(now.year, now.month, now.day)
    delta = d1 - d0
    #print (delta.days)

    #CHECKING FOR BOTNETS
    # if(user.default_profile_image)
    #     checkPassed=checkPassed+1
    # if(user.default_profile)
    #     checkPassed=checkPassed+1
    fvf_ratio=user.followers_count/user.friends_count
    if(fvf_ratio >=1.1 and fvf_ratio<=0.9):                                                               #botnets have equal number of equal number of followers and folllowing
        checkPassed=checkPassed+1
    if(user.followers_count<5):                                                                          #less followers
        checkPassed=checkPassed+1
    if(user.statuses_count/delta.days>70):                                                               #average posts per day >70
        checkPassed=checkPassed+1
    if(user.favourites_count/delta.days>100):                                                            #average likes per day >100
        checkPassed=checkPassed+1
    if(user.friends_count==2001):                                                                          #twitter restriction check
            checkPassed=checkPassed+1

    botPercentage=((checkPassed/7)*100)
   # print("\nThere is a ",checkPassed,"% chance that this Account is a bot")
    return(botPercentage)

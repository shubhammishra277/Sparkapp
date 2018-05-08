'''
Created on 19-Feb-2018

@author: shubham
'''


import tweepy
from loggermodule import logger_test
from configgetter import configparser
import os
import sys
import time 

import optparse


class twitterdata(object):
    
    def __init__(self,clientname,platformname):
        t1=configparser()
        
        self.client_name,consumer_key,consumer_secret,access_token_key,access_token_secret=t1.configparse(clientname,platformname)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        try:
          self.api = tweepy.API(auth)
          logger_test.info("succesful authentication with twitter")
        except Exception,e:
            logger_test.exception("error occured while doing authentication with twitter with following error:%s"%str(e))
            sys.exit("authentication failed")
            
    def datagetter(self,query,pages=0,items=0):
        tparsed=[]
        f=open("Tweet_%s.csv"%self.client_name,"w+")
        f.write("TWEET_CREATION_DATE,TWEET_USER_ID,TWEET_USER_NAME,TWEET_TEXT,URL\n")
        if pages==0:
          for status in self.limit_handled(tweepy.Cursor(self.api.search,q=query,include_entities = True).items(items)):
              #print "status",status
              logger_test.debug("Tweet which we are processing is %s"%status)
              #print "type ",type(status)
              #print "########################"
              tparsed.append(self.processtwitter(status,f))
              #print "\n\n\n"
        else:
          for status in self.limit_handled(tweepy.Cursor(self.api.search,q=query,include_entities = True).pages(pages)):
              logger_test.debug("Tweet which we are processing is %s"%status)
              #print "type ",type(status)
              #print "########################"
              tparsed.append(self.processtwitter(status,f))
   
        
        return tparsed
    def limit_handled(self,cursor):
     while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            logger_test.exception("Rate limit occured with exception:%s"%str(e))
            logger_test.info("sleeping for 15 min to avoid race condition")
            time.sleep(15 * 60)
            
    def processtwitter(self,status,f):
         #print "status",status.entities
         
         #f=open("Tweet.csv","w+")
         #f.write("TWEET_CREATION_DATE,TWEET_USER_ID,TWEET_USER_NAME,TWEET_TEXT,URL\n")
         for url in status.entities["urls"]:
            logger_test.info("after parsing the tweet follwing are the details:status.created_at:%s,status.user.id:%s,status.user.name:%s,status.text:%s,expanded_url:%s\n\n\n"%(status.created_at,status.user.id,status.user.name,status.text,url["expanded_url"]))
         
            if url["expanded_url"] is None:
                f.write("%s|%s|%s|%s|%s\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8"), url["url"].encode("utf-8")))
                return (status.created_at,status.user.id,status.user.name,status.text, url["url"])
            else:
             f.write("%s|%s|%s|%s|%s\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8"), url["expanded_url"].encode("utf-8")))  
             return (status.created_at,status.user.id,status.user.name,status.text, url["expanded_url"])

        
        
if __name__=="__main__":
  
    parser = optparse.OptionParser(description='Optional app description')
    parser.add_option('-u','--username', 
                    help='enter the username for which you have access token,consumer_token etc.')
    parser.add_option('-t','--platformname', 
                    help='enter the platform for which you have access token,consumer_token etc.',
                    default="twitter")
    parser.add_option('-p','--pages', 
                    help='No. of pages ,which you want to search to search string',
                    default=0)
    parser.add_option('-i','--items',
                    help='Number of tweets which you want to search for query string',
                    default=0)
    parser.add_option('-s','--search_string',
                    help='Query string which you want to search',
                    default="Twitter with Spark")
    try:
      options, args = parser.parse_args()
    except Exception,e:
        logger_test.exception("Sys arguements parsing failed with following errors:%s"%str(e))
    logger_test.info("arguemts parsed from command line are:%s "%options)
    #sys.exit()
    t1=twitterdata(str.lower(options.username),str.lower(options.platformname))
    #pages=2
    values=t1.datagetter(options.search_string,pages=int(options.pages),items=int(options.items))
    logger_test.debug("all the processed values:%s"%values)
    
        

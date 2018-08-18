'''
Created on 19-Feb-2018

@author: shubham
'''


import tweepy
from loggingmodule.logger import loggermodule
from configgetter import configparser
import os
import sys
import time 

import optparse


class twitterdata(object):
    
    def __init__(self,clientname,platformname):
        t1=configparser()
        self.logger_test=loggermodule()
        self.client_name,consumer_key,consumer_secret,access_token_key,access_token_secret=t1.configparse(clientname,platformname)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        try:
          self.api = tweepy.API(auth)
          self.logger_test.info("succesful authentication with twitter")
        except Exception,e:
            self.logger_test.exception("error occured while doing authentication with twitter with following error:%s"%str(e))
            sys.exit("authentication failed")
            
    def datagetter(self,query,pages=0,items=0):
        #tparsed=[]
        f=open("Tweet_%s.csv"%self.client_name,"w+")
        f.write("TWEET_CREATION_DATE,TWEET_USER_ID,TWEET_USER_NAME,TWEET_TEXT,URL\n")
        if pages==0:
          for status in self.limit_handled(tweepy.Cursor(self.api.search,q=query,include_entities = True).items(items)):
              #print "status",status
              #self.logger_test.debug("Tweet which we are processing is %s"%status)
              #print "type ",type(status)
              #print "########################"
              try:
                self.processitemtwitter(status,f)
              except Exception as e:
                  self.logger_test.exception("exception occured while processing tweet %s"%str(e))
              #print "\n\n\n"
        else:
          for page in self.limit_handled(tweepy.Cursor(self.api.search,q=query,include_entities = True).pages(pages)):
              #self.logger_test.debug("Tweet which we are processing is %s"%status)
              #print "type ",type(status)
              #print "########################"
              try:
                self.processpagetwitter(page,f)
              except Exception as e:
                  self.logger_test.exception("exception occured while processing tweet %s"%str(e))
   
        
        #return tparsed
    def limit_handled(self,cursor):
     while True:
        try:
            yield cursor.next()
        except tweepy.error.TweepError as e:
            if "429" in str(e):
             print "Rate limit occured ,so we are sleeping "
             self.logger_test.exception("Rate limit occured with exception:%s"%str(e))
             self.logger_test.info("sleeping for 15 min to avoid race condition")
             time.sleep(15 * 60)
            else :
                self.logger_test.exception("Tweepy error occured with error %s"%str(e))
                sys.exit()
            
    def processitemtwitter(self,status,f):
        
         if len(status.entities["urls"])!=0:
         
            self.logger_test.info("after parsing the tweet follwing are the details:status.created_at:%s,status.user.id:%s,status.user.name:%s,status.text:%s,expanded_url:%s\n\n\n"%(status.created_at,status.user.id,status.user.name,status.text,status.entities["urls"][0]["expanded_url"]))
         
           # if url["expanded_url"] is None:
            f.write("%s|%s|%s|%s|%s\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8"), status.entities["urls"][0]["expanded_url"].encode("utf-8")))
            return (status.created_at,status.user.id,status.user.name,status.text,status.entities["urls"][0]["expanded_url"])
         else:
            
            f.write("%s|%s|%s|%s|''\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8")))

            return (status.created_at,status.user.id,status.user.name,status.text,"")
 
    def processpagetwitter(self,page,f):
        
        for status in page:
            
         if len(status.entities["urls"])!=0:
         
            self.logger_test.info("after parsing the tweet follwing are the details:status.created_at:%s,status.user.id:%s,status.user.name:%s,status.text:%s,expanded_url:%s\n\n\n"%(status.created_at,status.user.id,status.user.name,status.text,status.entities["urls"][0]["expanded_url"]))
         
           # if url["expanded_url"] is None:
            f.write("%s|%s|%s|%s|%s\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8"), status.entities["urls"][0]["expanded_url"].encode("utf-8")))
            #return (status.created_at,status.user.id,status.user.name,status.text,status.entities["urls"][0]["expanded_url"])
         else:
            
            f.write("%s|%s|%s|%s|''\n"%(status.created_at,status.user.id,status.user.name.encode("utf-8"),status.text.strip("\n").replace("\n","").encode("utf-8")))

            #return (status.created_at,status.user.id,status.user.name,status.text,"")
        
        
if __name__=="__main__":
    loggerdata=loggermodule()
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
        loggerdata.exception("Sys arguements parsing failed with following errors:%s"%str(e))
    loggerdata.info("arguemts parsed from command line are:%s "%options)
    #sys.exit()
    t1=twitterdata(str.lower(options.username),str.lower(options.platformname))
    #pages=2
    t1.datagetter(options.search_string,pages=int(options.pages),items=int(options.items))
    #loggerdata.debug("all the processed values:%s"%values)
    
        

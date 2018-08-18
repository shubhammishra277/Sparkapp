'''
Created on 19-Feb-2018

@author: shubham
'''
import sys
from loggingmodule.logger import loggermodule
from ConfigParser import RawConfigParser

class configparser(object):
        def __init__(self):
            self.logger_test=loggermodule()
            self.logger_test.debug("initialising constructor")
            print "i am printing something",self.logger_test
    
        def configparse(self,client_name,platformname):
             self.logger_test.debug("parsing the configuration file for processing the data")
             try:
              parser =RawConfigParser()
              parser.read('/home/shubham/workspace/Sparkapp/config.ini')
              print parser.sections()
              
              if str.lower(platformname)=="twitter":
                clientname=platformname+"_"+client_name
                m=parser.items(clientname)
             #print "m",m
                consumer_key=m[0][1]
             
                consumer_secret=m[1][1]
                access_token_key=m[2][1]
                access_token_secret=m[3][1]
                return client_name,consumer_key,consumer_secret,access_token_key,access_token_secret
              elif str.lower(platformname)=="github":
                  clientname=platformname+"_"+client_name
                  m=parser.items(clientname)
                  
                  access_token=m[0][1]
                  return client_name,access_token
                  #self.logger_test.exception("error occured while reading the config file with error :%s"%str(e))
                 
              elif str.lower(platformname)=="meetup":
                     
                  clientname=platformname+"_"+client_name
                  m=parser.items(clientname)
                  
                  
              else:
                  
                  self.logger_test.info("No such(%s) platform exist "%platformname)
                  
                  
             except Exception,e:
                self.logger_test.exception("error occured while parsing the congig file with exception :%s"%str(e))
                sys.exit("error ocuured while parsing")
                    
                    


if __name__=="__main__":
    #clientname_value=sys.argv[1].split("=")[-1]
    clientname_value="shubham"
    t1=configparser()
    print "t1",t1
    t1.configparse(clientname_value,"twitter")
     
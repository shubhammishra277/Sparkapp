import logging
import datetime
import os
from ConfigParser import RawConfigParser
from anaconda_navigator.external.binaryornot.check import logger


def loggermodule():
   print "i am inside loggermodule"
   parser = RawConfigParser()
   parser.read('/home/shubham/workspace/Sparkapp/config.ini')
   client_name="LoggingLevel"
   m=parser.items(client_name)
   logginglevel=str.upper(m[0][1])
   LEVELS = {'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR,
          'CRITICAL': logging.CRITICAL}



   logger_test=logging.getLogger(__name__)
   print "logger_test",logger_test
   current_date=datetime.date.today().isoformat()

   logger_test.setLevel(LEVELS[logginglevel])
   d1=logger_test

   p=os.getcwd()

   os.system("mkdir -p /home/shubham/workspace/Sparkapp/logs")
   ch = logging.FileHandler('/home/shubham/workspace/Sparkapp/logs/datalogs_%s.log'%current_date,mode='a')
   ch.setLevel(logging.DEBUG)
   formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
   ch.setFormatter(formatter)

   logger_test.addHandler(ch)
   return logger_test
   
if __name__=="__main__":
       pass
    
    
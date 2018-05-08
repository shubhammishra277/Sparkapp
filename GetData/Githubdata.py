'''
Created on 21-Feb-2018

@author: shubham
'''
from github import Github
from pprint import pprint as pp
from loggermodule import logger_test
from configgetter import configparser
import optparse
from bokeh.themes import default

class githubapi(object):

    def __init__(self,clientname,platformname,user,repo):
       #ACCESS_TOKEN="dce09ea4b555192cd85f2a7e6c3d7aa7f1e7703b"
       t1=configparser()
       self.clientname,self.access_token=t1.configparse(clientname,platformname)
       USER="%s"%user
       REPO="%s"%repo
       print "self.access_token",self.access_token
       self.g=Github(self.access_token,per_page=100)
       #print self.g
       self.user=self.g.get_user(USER)
       self.repo=self.user.get_repo(REPO)
       
    def process(self):
        repos_apache=[repo.name for repo in self.user.get_repos()]
        #print repos_apache
        f=open("Git_%s.txt"%self.clientname,"w+")
        lang=self.repo.get_languages()
        logger_test.info("no. of languages used:%s"%len(lang))
        stargazers=[s for s in self.repo.get_stargazers()]
        try:
          k=[stargazers[i].login for i in range(0,20)]
        except :
            k=stargazers
        logger_test.info("Total number of repo of the user:%s"%len(repos_apache))
        logger_test.info("Different languages used in the repo:%s"%lang)
        logger_test.info("Top contributors:%s"%k)
        f.write("Total number of repo of the user:%s\n"%len(repos_apache))
        f.write("Different languages used in the repo:%s\n"%lang)
        f.write("Total no. of languages used in repo:%s\n"%len(lang))
        f.write("Top contributors:%s\n"%k)
        
        return len(repos_apache),lang,len(lang),k
if __name__=="__main__":
    parser = optparse.OptionParser(description='Optional app description')
    parser.add_option('-u','--username', 
                    help='enter the username for which you have access token,consumer_token etc.')
    parser.add_option('-p','--platformname', 
                    help='enter the platform for which you have access token,consumer_token etc.',
                    default="github")
    try:
      options, args = parser.parse_args()
    except Exception,e:
        logger_test.exception("Sys arguements parsing failed with following errors:%s"%str(e))
    logger_test.info("arguemts parsed from command line are:%s "%options)
    #sys.exit()
    user_name=raw_input("enter the user name of the repository:")
    repo_name=raw_input("enter the name of the repo:")
    t1=githubapi(str.lower(options.username),str.lower(options.platformname),user_name,repo_name)

    a,b,c,d=t1.process()
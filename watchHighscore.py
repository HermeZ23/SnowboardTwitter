
import pyinotify
import tweepy
import sys
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv



filepath = ""
highscore = []

class ProcessTransientFile(pyinotify.ProcessEvent):

    

    def parseFile(self):
        global highscore
        fo = open(filepath , "r")
        current = fo.readlines()
        diff = set(current) - set(highscore) 
        if len(diff) > 0:
            el = list(diff)[0]
            pos = current.index(el)
            if pos < 10:
                self.sentTweet(el, pos+1)
        highscore = current

        
        fo.close();
        

    def get_api(self, cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def sentTweet(self, text, posi):

        cfg = {
            "consumer_key"        : environ.get("CONSUMER_KEY"),
            "consumer_secret"     : environ.get("CONSUMER_SECRET"),
            "access_token"        : environ.get("ACCESS_TOKEN"),
            "access_token_secret" : environ.get("ACCESS_TOKEN_SECRET") 
        }
        # *[group] default [course] bunny_hill [plyr] honeymoon [pts] 362 [herr] 22 [time] 37.8
        words = text.split("]")
        if len(words) > 4:
            tweet = "#HackersOnSnowboards position "+ str(posi) +" changed: Course:" + words[2].split("[")[0] + "Player:" + words[3].split("[")[0] + "Points:" + words[4].split("[")[0]
        else:
            tweet = "something went wrong, fix me!"

        #print(tweet)
        api = self.get_api(cfg)

        try:
            api.update_status(status=tweet)
        except tweepy.TweepError:
            print(tweet)

    def process_IN_MODIFY(self, event):
        # We have explicitely registered for this kind of event.
        #print ('\t', event.pathname, ' -> written')
        self.parseFile()

    def process_default(self, event):
        # Implicitely IN_CREATE and IN_DELETE are watched too. You can
        # ignore them and provide an empty process_default or you can
        # process them, either with process_default or their dedicated
        # method (process_IN_CREATE, process_IN_DELETE) which would
        # override process_default.
        print ('default: ', event.maskname)

dotenv_path = join(dirname(__file__), 'twitter.env')
load_dotenv(dotenv_path)

filepath = sys.argv[1]
print(sys.argv[1])
fo = open(filepath , "r")
    
highscore = fo.readlines()

fo.close();

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
# In this case you must give the class object (ProcessTransientFile)
# as last parameter not a class instance.
wm.watch_transient_file(filepath, pyinotify.IN_MODIFY, ProcessTransientFile)
notifier.loop()


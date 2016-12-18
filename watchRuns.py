
import pyinotify
import tweepy
import sys
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

filepath = ""

class ProcessTransientFile(pyinotify.ProcessEvent):

    

    def parseFile(self):
        fo = open(filepath , "r")
        runs = 21
        
        for line in fo:
            runs = int(float(line))
  
        fo.close();
        if runs % 100 == 0:
            self.sentTweet("#HackersOnSnowboards " + str(runs) + " Downhills have been started")

    def get_api(self, cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def sentTweet(self, text):

        cfg = {
            "consumer_key"        : environ.get("CONSUMER_KEY"),
            "consumer_secret"     : environ.get("CONSUMER_SECRET"),
            "access_token"        : environ.get("ACCESS_TOKEN"),
            "access_token_secret" : environ.get("ACCESS_TOKEN_SECRET") 
        }

        #print(tweet)
        api = self.get_api(cfg)

        try:
            api.update_status(status=text)
        except tweepy.TweepError:
            print(text)

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

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
# In this case you must give the class object (ProcessTransientFile)
# as last parameter not a class instance.
wm.watch_transient_file(filepath, pyinotify.IN_MODIFY, ProcessTransientFile)
notifier.loop()


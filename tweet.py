import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], 
cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : "80NhsIUn7luA9ShSMFzd3d1Xe",
    "consumer_secret"     : "Kl4BQUIhZNAoxOIkbL4VYYVBXmxkzmZ3bb1mkPuAXmehi0QY8C",
    "access_token"        : "807678323027574784-nGRcuZKTiOhuQ1BOa9aZdOw7SqEfigD",
    "access_token_secret" : "VzryBjL2Vp2Ux8m0Xq9lNd3QAuumR8H5rGkwN0zTzQuBw" 
    }

  api = get_api(cfg)
  tweet = "Hello, world!"
  status = api.update_status(status=tweet) 
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()

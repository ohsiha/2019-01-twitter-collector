# runcollector.py

import simplejson as json

with open('keychain.json') as f:
  keychain = json.load(f)

print(keychain.keys())
# Authenticating to Twitter API
from requests_oauthlib import OAuth1

def get_oauth():
  oauth = OAuth1(keychain['CONSUMER_KEY'],
              client_secret=keychain['CONSUMER_SECRET'],
              resource_owner_key=keychain['ACCESS_TOKEN'],
              resource_owner_secret=keychain['ACCESS_TOKEN_SECRET'])
  return oauth


auth = get_oauth()

# Twitter REST API: https://dev.twitter.com/rest/public
# Searching tweets through the API
# https://api.twitter.com/1.1/search/tweets.json?q=%40twitterapi

import requests
r = requests.get(url='https://api.twitter.com/1.1/search/tweets.json?q=%23atkhommat', auth=get_oauth())
print(r.json().keys())
print(len(r.json()['statuses']))
with open('sample.json', 'w') as f:
  json.dump(r.json(), f, indent=1)

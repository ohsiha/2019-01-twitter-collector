from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import pytz, datetime
import sys

with open('keychain.json') as f:
    keychain = json.load(f)

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=keychain['CONSUMER_KEY']
consumer_secret=keychain['CONSUMER_SECRET']

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=keychain['ACCESS_TOKEN']
access_token_secret=keychain['ACCESS_TOKEN_SECRET']

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        # print(data.id)
        tweet = json.loads(data)
        print(datetime.datetime.now(pytz.timezone('Europe/Helsinki')))
        if 'id' in tweet.keys():
            print(tweet['id'])
        print(tweet['text'])
        # print(tweet.keys())
        # print()
        with open('data/%s.json' % tweet['id'], 'w') as f:
            json.dump(tweet, f, indent=1)
        # with open('')
        # json.dump()
        return True

    def on_error(self, status):
        print(status)

def run_streaming(stream, search_terms):
    print('Streaming data')
    print('... search terms: ', ', '.join(search_terms))
    try:
        stream.filter(track=search_terms)
    # See https://github.com/tweepy/tweepy/issues/591#issuecomment-92642455
    # various exception handling blocks
    except KeyboardInterrupt:
        sys.exit()
    # except AttributeError as e:
    #     print('AttributeError occured:')
    #     print(e)
    except Exception as e:
        print('Unhandled exception:')
        print(e)
        print('... reconnecting to stream')
        run_streaming(stream, search_terms)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    run_streaming(stream, ['Tampereen yliopisto', 'tampereuni', 'tuni.fi'])

#!/usr/bin/env python

import tweepy
import pandas as pd
import re

from keys import Keys

'''
Regex sourced from StackOverflow.
https://stackoverflow.com/a/11332580
'''
def clean(text):
    no_url = re.sub(r'http\S+', '', text)
    no_lines = no_url.replace('\n', ' ').replace('\r', '').replace('\"', '').replace('\'', '').replace('  ', '')
    no_hash = re.sub('@[^\s]+', '', no_lines)
    return no_hash.strip()

'''
This requires some manual monitoring as it's not always clear when the Twitter
API will kick you off because of rate requests.

Current solution is to save after every handle, and then load the file if it
already exists (to continue appending to it).

This was prior to discovering `wait_on_rate_limit`.
'''
def download_tweets(handles, recover=False):
    keys = Keys()

    auth = tweepy.OAuthHandler(keys.consumer_token, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    text = []

    if recover:
        text = pd.read_csv('tweets.csv', header=None, squeeze=True).values.tolist()

    for handle in handles:
        print(f'Downloading tweets for {handle}...')
        try:
            tweets = tweepy.Cursor(api.user_timeline, id=handle, tweet_mode='extended').items()
        except TweepError as e:
            print(e)

        for tweet in tweets:
            if hasattr(tweet, 'retweeted_status'):
                try:
                    text.append(clean(tweet.retweeted_status.extended_tweet['full_text']))
                except AttributeError:
                    text.append(clean(tweet.retweeted_status.full_text))
            else:
                try:
                    text.append(clean(tweet.extended_tweet['full_text']))
                except AttributeError:
                    text.append(clean(tweet.full_text))

        print(f'Saving tweets for {handle}...')
        pd.DataFrame(text).to_csv('./tweets.csv', header=None, index=None)

if __name__ == '__main__':
    handles = ['FreedoniaNews', 'cbellantoni', 'Atrios', 'nicopitney', 'ggreenwald', 'wonkroom', 'stevebenen', 'ewerickson', 'mindyfinn', 'dmataconis', 'tpcarney', 'jbarro', 'heminator', 'reihansalam', 'republicanstudy', 'nathandaschle']

    download_tweets(handles, recover=False)

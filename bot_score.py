#!/usr/bin/env python

'''
Created by Rudd Fawcett (rcf34) <rudd.fawcett@yale.edu>.
CPSC 310; Yale College; Spring 2020

This utility queries the RapidAPI in order to determine whether or not a given
Twitter handle is a "bot," based off of an implementation from Indiana University,
which can be found here: https://botometer.iuni.iu.edu/#!/ and https://github.com/IUNetSci/botometer-python.

In order to use this tool, make sure that all of the dependencies listed in
requirements.txt have been installed, and then use it as so:

python bot_score.py handle

You don't need to (and shouldn't) include the `@` in the handle.
'''

import botometer
import argparse

from keys import Keys

keys = Keys()

def run(handle):
    rapidapi_key = keys.rapidapi_key
    twitter_app_auth = {
        'consumer_key': keys.consumer_token,
        'consumer_secret': keys.consumer_secret,
        'access_token': keys.access_token,
        'access_token_secret': keys.access_token_secret
    }

    bom = botometer.Botometer(wait_on_ratelimit = True,  rapidapi_key = rapidapi_key, **twitter_app_auth)

    try:
        result = bom.check_account(f'@{handle}')

        my_score = 0
        count = 0

        for k, v in result['display_scores'].items():
            my_score += result['display_scores'][k]
            count += 1

        print(f'Average score for {handle} is {my_score/count}.')

    except Exception as e:
        print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a botometer score for a given Twitter handle.')
    parser.add_argument('handle')

    args = parser.parse_args()
    if args.handle:
        run(args.handle)

#!/usr/bin/env python

import yaml

class Keys:
    consumer_token = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    rapidapi_key = ''

    def __init__(self):
        with open('keys.yml', 'r') as stream:
            try:
                keys = yaml.safe_load(stream)

                self.consumer_token = keys['consumer_token']
                self.consumer_secret = keys['consumer_secret']

                self.access_token = keys['access_token']
                self.access_token_secret = keys['access_token_secret']

                self.rapidapi_key = keys['rapidapi_key']
            except yaml.YAMLError as exc:
                print(exc)
                exit()

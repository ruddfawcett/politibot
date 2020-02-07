#!/usr/bin/env python

import http.server
import http.client
import urllib.parse
import ast
import sys

import tweepy

from keys import Keys

class TwitterHandler(http.server.SimpleHTTPRequestHandler):

    def session_store(self, token):
        self.send_header('Set-Cookie', 'auth={};'.format(token))

    def session_retrieve(self):
        # bit ugly, but gets stored token from cookie
        return ast.literal_eval(self.headers.get( 'Cookie' ).split( '=' )[ 1 ])

    def do_GET( self ):
        req = urllib.parse.urlparse('http://localhost:8080' + self.path)
        query = req.query

        if query:
            vals = urllib.parse.parse_qs(query)
            print('Access Token: {}\nAccess Token Secret: {}'.format(vals['oauth_token'][0], vals['oauth_verifier'][0]))
            exit()

        else:
            keys = Keys()
            auth = tweepy.OAuthHandler(keys.consumer_token, keys.consumer_secret, 'http://127.0.0.1:8080')

            try:
                redirect_url = auth.get_authorization_url()

                self.send_response(307)
                self.send_header('Location', redirect_url)
                self.session_store(auth.request_token['oauth_token'])
                self.end_headers()
            except tweepy.TweepError as e:
                print(e)

def run(server_class = http.server.HTTPServer, handler_class = TwitterHandler):
    server_address = ('localhost', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()

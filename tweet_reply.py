#!/usr/bin/env python

import random
import re
import datetime

import tweepy

import gpt_2_simple as gpt2
import tensorflow as tf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from keys import Keys

SUPPORT = 1
OPPOSE = -1

MIN_LENGTH = 20
MAX_LENGTH = 140
STEP_LENGTH = 20

SENTIMEMT_THRESHOLD = 0.2

keys = Keys()

auth = tweepy.OAuthHandler(keys.consumer_token, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess)

def gen_prefix(subject, type, agree=True, extended_prefix=True):
    emotion = 'agree' if agree else 'disagree'

    adv = ['obviously', 'certainly', 'so']

    if not extended_prefix:
        return f'I {random.choice(adv)} {emotion}! {subject} is'

    rand = random.randint(1,3)

    pos_action = ['love', 'LOVE', 'admire', 'prefer', 'idolize', 'worship', 'prefer', 'like']
    neu_action = ['think', 'believe', 'feel']
    neg_action = ['hate', 'HATE', 'depise', 'dislike', 'detest', 'loathe', 'abhor', 'curse']

    transition = ['because', 'due to', 'as a result of', 'considering', 'now that']

    subj = ['I', 'My parents and I', 'My siblings and I', 'We', 'My friends and I', 'We all']

    pos_adj = ['the best', 'the finest', 'first-rate', 'outstanding', 'perfect']
    neg_adj = ['the worst', 'bad', 'horrible', 'a disaster']

    action = random.choice(pos_action) if type==SUPPORT else random.choice(neg_action)
    neu_action = random.choice(neu_action)
    adj = random.choice(pos_adj) if type==SUPPORT else random.choice(neg_adj)
    pos_adj_single = random.choice(pos_adj)

    adv = random.choice(adv)
    transition = random.choice(transition)
    subj = random.choice(subj)

    pos_caps = ['ALL HAIL', 'EVERYONE SUPPORT', 'YOU\'RE THE BEST', 'WE LOVE YOU']
    neg_caps = ['WE HATE YOU', 'WE HOPE YOU FAIL', 'YOU\'RE THE WORST', 'GO DIE', 'I DISLIKE YOU']

    caps = random.choice(pos_caps) if type==SUPPORT else random.choice(neg_caps)

    text = ''

    if rand == 1:
        if type == OPPOSE:
            text = f'{subj} is not {pos_adj_single.upper()}! {subj} {adv} {action.upper()} {subject} {transition}'
        # My parents and I obviously love XYZ becuase
        text = f'{subj} {adv} {action.upper()} {subject} {transition}'
    elif rand == 2:
        if type == OPPOSE:
            text = f'{subj} {neu_action} {subject} is not {pos_adj_single.upper()}, no {subject} is {adv} {adj.upper()} {transition}'
        # We think XYZ is certainly the finest
        text = f'{subj} {neu_action} {subject} is {adv} {adj.upper()} {transition}'
    else:
        if type == OPPOSE:
            text = f'{caps} {subject}! {subject} is not {pos_adj_single.upper()} {transition}'
        text = f'{caps} {subject}! {subject} is {adj.upper()} {transition}'

    return f'I {adv} {emotion.upper()}! {text}'

def gen_text(prefix):
    global sess

    generate_count = 0
    length = MIN_LENGTH

    prepend = f'<|startoftext|>{prefix}'
    text = prepend

    # Heavily influenced by https://github.com/minimaxir/reddit-gpt-2-cloud-run/blob/master/app.py.
    while '<|endoftext|>' not in text and length <= MAX_LENGTH:
        text = gpt2.generate(sess,
                             length=STEP_LENGTH,
                             temperature=0.7,
                             top_k=40,
                             prefix=text,
                             include_prefix=True,
                             return_as_list=True
                             )[0]

        length += STEP_LENGTH

        generate_count += 1
        if generate_count == 5:
            # Reset the text in order to try to change the sentiment
            text = prepend
        elif generate_count == 8:
            # Reload model to prevent Graph/Session from going OOM
            tf.compat.v1.reset_default_graph()
            sess.close()
            sess = gpt2.start_tf_sess(threads=1)
            gpt2.load_gpt2(sess)
            generate_count = 0

    prepend_esc = re.escape('<|startoftext|>')
    eot_esc = re.escape('<|endoftext|>')
    pattern = f'(?:{prepend_esc})(.*)(?:{eot_esc})'

    tf.compat.v1.reset_default_graph()
    sess.close()
    sess = gpt2.start_tf_sess(threads=1)
    gpt2.load_gpt2(sess)

    result = re.search(pattern, text)
    if result is None:
        result = gen_text(prefix)

    return result if isinstance(result, str) else result.group(1)

def gen_response(subject, type, agree=True):
    prefix = gen_prefix(subject, type, agree=agree, extended_prefix=True)
    text = gen_text(prefix)
    analyzer = SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)['compound']

    if type == SUPPORT:
        while compound <= SENTIMEMT_THRESHOLD:
            print('Trying to generate a more positive response...')
            prefix = gen_prefix(subject, type, agree=agree, extended_prefix=True)
            text = gen_text(prefix)
            compound = analyzer.polarity_scores(text)['compound']
            print(f'Generated text: {text}...\n Compound score: {compound}...')

    else:
        while compound >= -SENTIMEMT_THRESHOLD:
            print('Trying to generate a more negative response...')
            prefix = gen_prefix(subject, type, agree=agree, extended_prefix=True)
            text = gen_text(prefix)
            compound = analyzer.polarity_scores(text)['compound']
            print(f'Generated text: {text}...\n Compound score: {compound}...')

    return text

def reply(text, handle, status_id):
    orig = text
    text = text.lower()
    response = ''

    analyzer = SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)['compound']

    agree = False

    if 'sylvania' in text:
        agree = True if compound > 0.05 else False
        response = gen_response('Sylvania', SUPPORT, agree=agree)
    elif 'trentino' in text:
        agree = True if compound > 0.05 else False
        response = gen_response('Ambassador Trentino', SUPPORT, agree=agree)
    elif 'freedonia' in text:
        agree = True if compound < -0.05 else False
        response = gen_response('Freedonia', OPPOSE, agree=agree)
    elif 'rufus t. firefly' in text:
        agree = True if compound < -0.05 else False
        response = gen_response('Rufus T. Firefly', OPPOSE, agree=agree)
    else:
        return

    tweet_len = 280 - (len(handle) + 4) # + 4 = for space before handle id (1) and elipses(3)

    trimmed = (response[:tweet_len] + '...') if len(response) > tweet_len else response

    try:
        api.update_status(status=trimmed, in_reply_to_status_id=status_id, auto_populate_reply_metadata=True)

        print('{:=<65}\n'.format('==== PARSED TWEET, DETAILS BELOW: '))
        print('{:-<65} {}'.format('Tweet ', orig))
        print('{:-<65} {}'.format('Tweet ID ', status_id))
        print('{:-<65} {}'.format('Tweet Compound Sentiment ', compound))
        print('{:-<65} {}\n'.format('Agree with Tweet?', 'YES' if agree else 'NO'))

        print('{:=<65}\n'.format('==== TWEETED RESPONSE, DETAILS BELOW: '))
        print('{:-<65} {}'.format('Response Body ', trimmed))
        print('{:-<65} {}\n'.format('Response Sentiment ', analyzer.polarity_scores(trimmed)['compound']))
        print('{:=<65} {:%Y-%b-%d %H:%M:%S}'.format('==== Response Time ', datetime.datetime.now()))
        print('\n\n')
    except tweepy.TweepError as e:
        print(e)

def reply_to_tweets(handle):
    tweets = tweepy.Cursor(api.user_timeline, id=handle, tweet_mode='extended').items()

    for tweet in tweets:
        text = ''
        status_id = tweet.id

        if hasattr(tweet, 'retweeted_status'):
            try:
                text = tweet.retweeted_status.extended_tweet['full_text']
            except AttributeError:
                text = tweet.retweeted_status.full_text
        else:
            try:
                text = tweet.extended_tweet['full_text']
            except AttributeError:
                text = tweet.full_text

        reply(text, handle, status_id)

if __name__ == '__main__':
    reply_to_tweets('FreedoniaNews')

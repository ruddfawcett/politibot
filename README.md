## cpsc310 hwk1

### Keys

I am including the `keys.yml` file for the project in this folder because it doesn't seem to need to be secret for the purpose of this assignment, but I have also included a `keys.sample.yml` file which should be ignored as I will probably be uploading this to GitHub and therefore including the `keys.yml` file in my `.gitignore`.

### Project Structure

I apologize for the disorganized nature of this project, I was just not sure if I should put things in folders or if that would be harder to evaluate if there were files in all of these random places. So I'm leaving everything in this directory.

I'm listing the relevant files here, however, so hopefully that should be easier to grade.

* `bot_score.py` — The file that generates a bot score for a Twitter handle (part four).
* `delegate.py` — The file that starts a server for OAuth (part one).
* `download_tweets.py` — The file that downloads tweets from multiple handles (part two).
* `keys.py` — A class that manages all of the different keys/tokens needed.
* `keys.sample.yml` — A skeleton keys YML file in case the `keys.yml` file is in a `.gitignore`
* `keys.yml` — The actual keys from my accounts.
* `LICENSE` - a generic MIT license file.
* `requirements.txt` - The `pip` requirements for the files in the assignment.
* `test_gen.py` - A file that generates text from trained model.
* `text_encoded.npz` - Encoded file from my `tweets.csv`
* `train_gpt.py` - The file that encodes the tweets and trains the model.
* `tweet_reply.py` - The file that replies to the Freedonia tweets by generating responses and analyzing sentiment.
* `tweets.csv` - The tweets downloaded for the assignment.

## Rubric

#### Part One

My account is `@rcf34_`.

#### Part Two

  * [x] **Web service implementation**

  Please look at the `delegate.py` file for my web service implementation.

  ```bash
  $ python delegate.py
  ```

  Executing the file will spin up an instance on `localhost`, and you will be able to test the functionality of the OAuth response from a browser.

  * [x] **Written response**

  The three-legged OAuth pattern exists, essentially, so that an client can engage with a organization/service provider without explicity being given credentials to a user account/resource owner. In this way, I can give an application/client access to my account with tokens and secrets granted by Twitter without the client ever knowing my password to my account. A three-legged approach differs from a two-legged approach in that there is user involvement—a two-legged approach means that a client is directly interacting with an API and may at some point come in contact with the user's credentials.

  This approach provides more security for the user. Also, a company like Twitter would prefer this approach as they are acting as the authenticator in the exchange, keeping them as the only point of reference for a user and their crdentials in the authentication process. In this way, it is a more secure approach for the user but also for Twitter in order to keep them in maximum control of the authentication process.

#### Part Three

  * [x] **Scraping of public Twitter account(s)**

  In order to scrape the public Twitter accounts, please use the `download_tweets.py` file in the same directory as this README. The usage is rather simple:

  ```bash
  $ python download_tweets.py
  ```

  In the `download_tweets.py` file, you can define an array of handles from which to download tweets. The maximum number of tweets (~3000) will be downloaded from each account, and these tweets will be stripped of Twitter handles, URLs, and errant quote marks. Using `tweepy`, you shouldn't be running into any problems with Twitter rate limiting, but, if you do, you can recover the process where it failed by observing the output in the console.

  ```python
  handles = ['FreedoniaNews'] #, 'realDonaldTrump', etc.
  download_tweets(handles, recover=False)
  ```

  * [x] **Corpus creation and GPT-2 model tuning**

  In order to train the GPT-2 model, I used the `gpt_2_simple` library as suggested in the assignment. I ended up training my data using the `355M` model, and I ended up having thousands of tweets so it took a few hours. I used `500` steps to train my model. Both the model and the number of steps can be adjusted in the file.

  ```python
  STEPS = 500
  MODEL_NAME = '355M'
  ````

  The above file will download the relevant model if the user doesn't already have it installed in the `modes/` directory.

  * [x] **Scraping of @FreedoniaNews account and sentiment classification**

    This part of the assignment and the next two parts of the assignment happen in the same file, `tweet_reply.py`. The main reason for this was because I wasn't sure whether or not we should be downloading the tweets or be modularizing the processes somehow.

    ```bash
    $ python tweet_reply.py
    ```

    The scraping of this data happens in the `reply_to_tweets(handle)` method of the `tweet_reply.py`. The method downloads the tweets of the `FreedoniaNews` user, and feeds them to a `reply(text, handle, status_id)` function. I use `tweepy` again here to scrape the data.

    Based on their sentiment, the tweets are classified whether or not to generate an agreeable negative response, an agreeable positive response, a disagreeable negative response, or a disagreeable positive response.

  * [x] **Generation of response tweets**

  In the `reply(text, handle, status_id)` method mentioned previously, I score the tweets from `FreedoniaNews`, and then generate a response using a `gen_response()` method:

  ```python
  # For example...
    if 'sylvania' in text:
        # If the sentiment is positive, then agree, else do not.
        agree = True if compound > 0.05 else False
        # Generate the response...
        response = gen_response('Sylvania', SUPPORT, agree=agree)
  ```

  * [x] **Posting of response tweets**

  Once the responses come back (this can take a while sometimes as I use a loop to make sure the responses have the correct sentiment), they are trimmed to an appropriate length and then posted from the `reply()` method mentioned.

  ```python
  trimmed = (response[:tweet_len] + '..') if len(response) > tweet_len else response
  api.update_status(status=trimmed, in_reply_to_status_id=status_id , auto_populate_reply_metadata=True)

  ```

#### Part Four

  * [x] **Correct use of Botometer classifier**

  Please find the code for this section in the `bot_score.py` file. In order to execute the code, run the following:

  ```bash
  $ python bot_score.py FreedoniaNews
  ```

  You'll need to pass in a handle via the CLI in order to get the results.

  * [x] **Analysis of results**

  As of February 7, at 3:00p.m., the scores for my account were as follow (not valid JSON, but as a Python dictionary):

  ```json
  {
  	'cap': {
  		'english': 0.06706338835674493,
  		'universal': 0.010164988287386762
  	},
  	'categories': {
  		'content': 0.9036625199309213,
  		'friend': 0.9136223598156034,
  		'network': 0.12243135948738738,
  		'sentiment': 0.8549607089337135,
  		'temporal': 0.8882002957327816,
  		'user': 0.38645379058359247
  	},
  	'display_scores': {
  		'content': 4.5,
  		'english': 2.2,
  		'friend': 4.6,
  		'network': 0.6,
  		'sentiment': 4.3,
  		'temporal': 4.4,
  		'universal': 0.9,
  		'user': 1.9
  	},
  	'scores': {
  		'english': 0.44245148142042123,
  		'universal': 0.1701324265302999
  	},
  	'user': {
  		'id_str': '1222907089393242112',
  		'screen_name': 'rcf34_'
  	}
  }
  ```

  According to the [FAQ on the bot website](https://botometer.iuni.iu.edu/#!/faq#bot-threshold):

  > Bot scores are displayed on a 0-to-5 scale with zero being most human-like and five being the most bot-like. A score in the middle of the scale is a signal that our classifier is uncertain about the classification.

  Going off of this explanation, it appears that the botometer is leaning towards interpreting my account as a bot (looking at the various `display_scores`). As stated in the results above, the `content` score is a 4.5 which is pretty telling (along with the `sentiment` score). These aren't surprising as my tweets follow a similar pattern (in agreeing/disagreeing) and also in how the appropriate sentiments are generated — the tweets are rarely neutral.

  Doing a quick average of the `display_scores` is ultimately what `python bot_score.py handle` spits out. In my case, the value was `2.925.`. This means that my account was more presenting as a bot than a human, but not super definitively.

  * [x] **Proposed practical use of bot classifier**

  It's hard to think of a very practical use for the bot classifier, but that is mainly because it could be pretty unreliable. Human eye and judgment will more easily distinguish bot accounts, perhaps, than machine learning algorithms due to differences in pattern recognition.

  However, this tool could serve useful in initially flagging bot accounts and working with a human interpreter to confirm/make a decision regarding the type of account. Such a system could be used in order to block/prevent certain accounts from responding/spamming responses to tweets from a potential candidate (what to do when real users are actually blocked and cry first amendment, however, remains another matter).

  Other uses for this tool would be to possibly develop a Chrome extension to hide accounts which may be bots, so users wouldn't even be seeing them in their timeline.

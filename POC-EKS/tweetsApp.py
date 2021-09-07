import tweepy as tw
import pandas as pd
from datetime import datetime
import os
import time

def twitter_auth():
    '''Authenticate to the Twitter API'''
    with open('twitter-tokens.txt') as tfile:
        consumer_key = tfile.readline().strip('\n')
        consumer_secret = tfile.readline().strip('\n')
        access_token = tfile.readline().strip('\n')
        access_token_secret = tfile.readline().strip('\n')

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tw.API(auth)

def get_tweets(search_word, number_of_tweets):
    #Autenticate to Twitter
    api = twitter_auth()

    #Prepare search query
    search_query = search_word + " -filter:retweets"

    #Prepare tweets dictionary
    tweets_dict = {}
    tweets_dict = tweets_dict.fromkeys(['created_at', 'user', 'text'])

    #Collect Tweets
    tweets = tw.Cursor(api.search, q=search_word).items(number_of_tweets)
    for tweet in tweets:
        for key in tweets_dict.keys():
            try:
                value = tweet._json[key]
                tweets_dict[key].append(value)
            except KeyError:
                value = ""
                tweets_dict[key] = [value] if tweets_dict[key] is None else tweets_dict[key].append(value)
            except:
                tweets_dict[key] = [value]
    
    tweets_df = pd.DataFrame.from_dict(tweets_dict)

    #Check destiny folder
    if not(os.path.exists("output/")):
        os.mkdir("output/")
    
    #Convert dataframe to csv file
    file_name = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    tweets_df.to_csv("output/"+file_name+".csv", index=False)

if __name__ == "__main__":

    while(True):
        try :
            #Running the tweets collector function
            get_tweets("#AWS", 1000)
            os.system("bash sync_to_s3.sh")
            time.sleep(900) #15 min
        except:
            exit(0) 
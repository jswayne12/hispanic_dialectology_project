import snscrape.modules.twitter as sntwitter
import pandas as pd
import praw
from googleapiclient.discovery import build

class Twitter_collect:
    def __init__(self):
        pass

    def get_tweets(self, search, country, amount_tweets=4000):
        tweet_list = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search + ' since:2021-06-07 until:2021-12-08').get_items()):
            if i > amount_tweets:
                break
            tweet_list.append([tweet.id, [tweet.content]])
        tweets_df = pd.DataFrame(tweet_list, columns=['Tweet Id', 'Text'])
        tweets_df['Country'] = country
        return tweets_df

class Youtube_collect:
    def __init__(self):
        pass

    def data_pull(self, url, title, country):
        #The api key will be left out for privacy reasons
        #Uses the Youtube API to pulls comments from videos
        api_key = ''
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.commentThreads().list(part='snippet,replies',videoId=url)
        response = request.execute()

        #list that will hold all comments and replies from a youtube video
        comment_list = []
        for items in response['items']:
            #Extracts the top level comments from the response variable
            top_comment = items['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_list.append(top_comment)
            #Extracts the replies from the top level comments using the response variable
            if items['snippet']['totalReplyCount'] > 0:
                raw_replies = items['replies']
                for dict in raw_replies['comments']:
                    reply = dict['snippet']['textDisplay']
                    comment_list.append(reply)

        #Creates dictionary that hold the comments and transforms that into a pandas dataframe
        comment_dict = {'Content':comment_list}
        df = pd.DataFrame(comment_dict, columns=['Content'])
        df['Title']= title
        df['Country']= country
        return df

class Reddit_collect:
    def __init__(self):
        #The user agent will be left out for privacy reasons
        self.user_agent = ''
    def connect_to_reddit(self):
        try:
            self.reddit = praw.Reddit(
                #client_id and client_secret will be left out for privacy reasons
                client_id = '',
                client_secret = '',
                user_agent= self.user_agent
            )
        except:
            print('Was not able to connect to reddit')
    def data_pull(self, subreddit_, country):
        #Uses Reddit API, praw, to extract data from various subreddits
        data = {}
        comments = []
        for submission in self.reddit.subreddit(subreddit_).search(query='politica', time_filter='year'):
            submission.comments.replace_more(limit=0)
            list = [[comment.body] for comment in submission.comments.list()]
            comments.extend(list)
        #Creation of reddit dataframe
        data['Content']= comments
        df_reddit = pd.DataFrame(data, columns=['Content'])
        df_reddit['Country'] = country
        return df_reddit

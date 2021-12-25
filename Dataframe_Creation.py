import pandas as pd
from data_collection import Reddit_collect, Twitter_collect, Youtube_collect
from data_query_info import queries

class Dataframe_creator:
    def __init__(self):
        self.dict = queries

    def make_df(self):
        #Creates the initial dataframes that hold the data pulled from social media sites
        n = int(0)
        reddit_dfs = []
        twitter_dfs = []
        youtube_dfs = []
        #Gives us the list of countries referenced in the queries dictionary. To be used for data collection
        country_list = list(self.dict.keys())
        for entry in self.dict:
            #Each 'entry' carries all information needed to pull the social media data for each country
            #reddit information
            reddit_collector = Reddit_collect() #create class object
            reddit_collector.connect_to_reddit() #connect to twitter
            #data pull
            entry_reddit_df = reddit_collector.data_pull(subreddit_=self.dict[entry]['Reddit'][0], country=country_list[n])
            reddit_dfs.append(entry_reddit_df)
            #twitter info
            twitter_collector = Twitter_collect()
            #The if statement here is used to assess whether there are 1 or 2 search queries for twitter
            #The operation is slightly different depending on the answer to that
            if len(self.dict[entry]['Twitter']) == 2:
                twitter_df1 = twitter_collector.get_tweets(search=self.dict[entry]['Twitter'][0],
                                                           country=country_list[n])
                twitter_df2 = twitter_collector.get_tweets(search=self.dict[entry]['Twitter'][1], country=country_list[n])
                entry_twitter_df = pd.concat([twitter_df1,twitter_df2], axis=0)
            else:
                entry_twitter_df = twitter_collector.get_tweets(search=self.dict[entry]['Twitter'][0],
                                                           country=country_list[n], amount_tweets=5500)
            twitter_dfs.append(entry_twitter_df)
            #youtube_info
            youtube_collector = Youtube_collect() #create class object
            url_list = [] #collect url
            title_list = [] #collect video titles
            for dictionary in self.dict[entry]['Youtube']:
                url_list.append(dictionary['Url'])
                title_list.append(dictionary['Title'])
            dfs = []
            title_index= 0
            #Collects data from each url left in the url list
            for url in url_list:
                df = youtube_collector.data_pull(url=url, title=title_list[title_index], country=country_list[n])
                dfs.append(df)
                title_index+=1
            entry_youtube_df = pd.concat(dfs, axis=0, ignore_index=True)
            youtube_dfs.append(entry_youtube_df)
            n+=1
        #ALl data in concatenated based on social media site then saved as csv files
        reddit_data = pd.concat(reddit_dfs, axis=0, ignore_index=True)
        reddit_data.to_csv('reddit_df.csv')
        twitter_data = pd.concat(twitter_dfs, axis=0, ignore_index=True)
        twitter_data.to_csv('twitter_df.csv')
        youtube_data = pd.concat(youtube_dfs, axis=0, ignore_index=True)
        youtube_data.to_csv('youtube_df.csv')
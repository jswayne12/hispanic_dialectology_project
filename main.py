from Dataframe_Creation import Dataframe_creator
from data_cleaner import Data_cleaner
from language_project_processor import Linguistic_processor
import pandas as pd
import ibm_db_dbi
from sql_storage import Ibm_sql

#Setting up the environment used to manipulate the database
sql= Ibm_sql()
conn = sql.create_database_connection()
pconn = ibm_db_dbi.Connection(conn)

#Allows for us to see more than the default settings would usually let us see... referring to pandas dataframes
pd.set_option('display.max_columns', 10)
continue_ = True
while continue_ == True:
    #Here is where one can choose which operations they would like to engage in.
    answer = input('''Which operation would you like to engage in?
    'D' for Data Collection
    'PRE' for General Data Cleansing
    'NLP_Ling' for NLP processes for the Spanish Linguistics project
    'NLP_Politics' for the NLP processes for the Hispanic Politics project
    'VIZ' for Visualizations
     'P' for practice\n''')

    if answer == 'D':
        #Collect and format data from social media sites
        data_collector = Dataframe_creator()
        data_collector.make_df()

        # Creates the SQL tables to hold the data from the dataframes just created
        social_media_list = ['reddit', 'twitter', 'youtube']
        for social_media in social_media_list:
            name = input(f'What would you like to name {social_media} dataframe?\n')
            if social_media == 'reddit':
                sql.make_query(f'''CREATE TABLE {name} (INDEX INT NOT NULL, CONTENT VARCHAR(10000) NOT NULL,
                COUNTRY VARCHAR(30) NOT NULL) ''')
            elif social_media == 'twitter':
                sql.make_query(f'''CREATE TABLE {name} (INDEX INT NOT NULL, TWEET_ID BIGINT NOT NULL PRIMARY KEY,
                CONTENT VARCHAR(1000) NOT NULL, COUNTRY VARCHAR(30) NOT NULL)''')
            elif social_media == 'youtube':
                sql.make_query(f'''CREATE TABLE {name} (INDEX INT NOT NULL, CONTENT VARCHAR(10000) NOT NULL, 
                TITLE VARCHAR(200) NOT NULL, COUNTRY VARCHAR(30) NOT NULL)''')
        continuing = input('''Would you like to continue?
        'y' for yes,
        'n' for no \n''')
        if continuing == 'n':
            print('We will be closing shortly, thank you for working with us!')
            sql.close_connection()
            continue_= False
    elif answer == 'PRE':
        #Allows for pre-processing of the data, and creation of SQL tables to hold that data
        data_cleaner = Data_cleaner()
        manipulate = True
        while manipulate == True:
            dataframe = input('Which dataframe will you be manipulating?')
            #Pandas manipulation
            df = pd.read_sql(f'SELECT * FROM {dataframe}', pconn)
            df = df.drop(columns=['INDEX'])

            #Each if statement processes the data, transform the dataframe, creates csv of dataframe, and create SQL table
            if dataframe == 'twitter_data':
                print('twitter')
                processed_df = data_cleaner.general_pre_processing_twitter(df)
                processed_df.to_csv(f'processed_{dataframe}.csv')
                sql.make_query(f'''CREATE TABLE PROCESSED_{dataframe} (index INT NOT NULL, tweet_id BIGINT NOT NULL PRIMARY KEY,
                 content VARCHAR(10000) NOT NULL, cleaned_content_punct VARCHAR(12000) NOT NULL, 
                 cleaned_content_stopword VARCHAR(12000) NOT NULL, parsed_content VARCHAR(12000) NOT NULL) ''')
            else: #The rest of the the data can be pre-processed and formatted this way
                processed_df = data_cleaner.general_pre_processing(df)
                print('other')
                processed_df.to_csv(f'processed_{dataframe}.csv')
                sql.make_query(f'''CREATE TABLE PROCESSED_{dataframe} (index INT NOT NULL, content VARCHAR(10000) NOT NULL, 
                    cleaned_content_punct VARCHAR(12000) NOT NULL, cleaned_content_stopword VARCHAR(12000) NOT NULL,
                    parsed_content VARCHAR(12000) NOT NULL) ''')

            #The end
            continuing_df = input('''Would you like to work with more dataframes?
                    'y' for yes,
                    'n' for no\n''')
            if continuing_df == 'n':
                manipulate=False
        continuing = input('''Would you like to engage in any other operations?
                'y' for yes
                'n' for no\n''')
        if continuing == 'n':
            print('We will be closing shortly, thank you for working with us!')
            sql.close_connection()
            continue_= False
    elif answer== 'NLP_Ling':
        #We extract important linguistic data through this operation and creates new SQL tables to hold that data
        ling_processor = Linguistic_processor()
        dataset_list= ['processed_youtube_data', 'processed_reddit_data', 'processed_twitter_data']
        for dataset in dataset_list:
            dataframe = dataset
            df = pd.read_sql(f'SELECT * from {dataframe}', pconn)

            #Each if statement processes the data, transform the dataframe, creates csv of dataframe, and create SQL table
            if dataframe == 'processed_twitter_data':
                twitter_df = ling_processor.full_analysis_twitter(df)
                twitter_df.to_csv('twitter_ling_data.csv')
                sql.make_query('''CREATE TABLE twitter_ling (index INT NOT NULL, tweet_id BIGINT NOT NULL PRIMARY KEY,
                 part_of_speech VARCHAR(20000) NOT NULL, lemmatization VARCHAR(20000) NOT NULL,
                 syntactic_analysis VARCHAR(20000) NOT NULL, phrase_length VARCHAR(200))''')
            elif dataframe == 'processed_reddit_data':
                reddit_df = ling_processor.full_analysis(df)
                reddit_df.to_csv('reddit_ling_data.csv')
                sql.make_query('''CREATE TABLE reddit_ling (index INT NOT NULL, parsed_content VARCHAR(12000) NOT NULL,
                 part_of_speech VARCHAR(20000) NOT NULL, lemmatization VARCHAR(20000) NOT NULL,
                 syntactic_analysis VARCHAR(20000) NOT NULL, phrase_length VARCHAR(200))''')
            elif dataframe == 'processed_youtube_data':
                youtube_df = ling_processor.full_analysis(df)
                youtube_df.to_csv('youtube_ling_data.csv')
                sql.make_query('''CREATE TABLE youtube_ling (index INT NOT NULL, parsed_content VARCHAR(12000) NOT NULL,
                 part_of_speech VARCHAR(20000) NOT NULL, lemmatization VARCHAR(20000) NOT NULL,
                 syntactic_analysis VARCHAR(20000) NOT NULL, phrase_length VARCHAR(200))''')

        continuing = input('''Would you like to engage in other operations?
        'y' for yes
        'n' for no''')
        if continuing == 'n':
            print('We will be closing out shortly')
            sql.close_connection()
            continue_=False




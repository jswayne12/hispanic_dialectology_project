import pandas as pd
import nltk
nltk.download('stopwords')
from sumy.utils import get_stop_words
stopwords = list(get_stop_words('spanish'))

#Do textual pre-processing
class Data_cleaner:
    def __init__(self):
        pass
    def clean_content_string_punct(self, string_):
        #cleans string of punctuations
        import string
        punctuation = [punct for punct in string.punctuation]
        punctuation.extend('¿')
        string_ = string_.lower()
        cleaned_string_list = [char for char in string_ if char not in punctuation]
        cleaned_string = ''.join(cleaned_string_list)
        cleaned_string= cleaned_string.split(' ')
        return cleaned_string

    def clean_content_punct(self, df):
        #Creates a column that is a version of the Content column cleaned of punctuation
        df['Cleaned Content Punct'] = [self.clean_content_string_punct(string_) for string_ in df['CONTENT']]
        return df

    def clean_content_string_stopword(self, string_):
        #returns a full cleaned string with no punctuations or stopwords
        string_no_punct = self.clean_content_string_punct(string_)
        cleaned_string = [word for word in string_no_punct if word not in stopwords]
        return cleaned_string

    def clean_content_stopword(self, df):
        #Returns and Column with a completely cleaned verions of the elements of CONTENT
        df['Cleaned Content Stopwords'] = [self.clean_content_string_stopword(string_) for string_ in df['CONTENT']]
        return df

    def sentence_parsing_string(self, string_):
        #replacing any punctuation that could indicate the ending of an idea with a '.' to then parse on the '.'
        new_string = string_.replace('!','.')
        new_string=new_string.replace('?','.')
        new_string= new_string.replace(',','.')
        new_string=new_string.replace(';', '.')
        new_string = new_string.replace('(', '.')
        new_string = new_string.replace(')', '.')
        new_string = new_string.replace(':', '.')
        new_string = new_string.replace("'", ".")
        new_string = new_string.replace('"','.')
        parsed_string = new_string.split('.')
        complete_parsed_string = [phrase for phrase in parsed_string if len(phrase) > 2]
        return complete_parsed_string
    def sentence_parsing(self, df):
        #Created a column that is the parsed version of CONTENT
        df['Parsed Content'] = [self.sentence_parsing_string(string_) for string_ in df['CONTENT']]
        return df
    def general_pre_processing(self,df):
        #Pulls all of the operations together in order to make new dataframes (used for reddit and youtube)
        primary_df = df[['CONTENT','COUNTRY']]
        clean_punct = self.clean_content_punct(primary_df)
        clean_stopword = self.clean_content_stopword(clean_punct)
        clean_punct = self.sentence_parsing(clean_stopword)
        complete_df = clean_punct.drop(columns=['COUNTRY'])
        return complete_df
    def general_pre_processing_twitter(self, df):
        #Pulls all of the operations together in order to make new dataframes (used for twitter)
        primary_df = df[['TWEET_ID', 'CONTENT']]
        clean_punct = self.clean_content_punct(primary_df)
        clean_stopword = self.clean_content_stopword(clean_punct)
        complete_df = self.sentence_parsing(clean_stopword)
        return complete_df

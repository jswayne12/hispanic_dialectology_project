import spacy
import string
punctuation = [char for char in string.punctuation]
class Linguistic_processor:
    def __init__(self):
        #Language model taken from SpaCy
        self.nlp = spacy.load("es_core_news_md")

    def pos_tags(self, string_):
        #Return the Part of Speech tags of a string
        string_list = string_.split(',')
        phrase_token_list = []
        punctuation = [char for char in string.punctuation]

        #Use spacy to extract POS tags while also excluding punctuations
        for phrase in string_list:
            tokens = self.nlp(phrase)
            pos_list = []
            for token in tokens:
                if token.text not in punctuation:
                    pos = token.tag_
                    text = token.text
                    text_pos = {text:pos}
                    pos_list.append(text_pos)

            phrase_token_list.append(pos_list)
        return phrase_token_list

    def pos_columns(self, df):
        #Create Part of Speech column based on PARSED_CONTENT
        df['Part of Speech'] =[[self.pos_tags(phrase)] for phrase in df['PARSED_CONTENT']]
        return df

    def lemma_extraction(self, string_):
        # Used to extract lemmas from a string
        string_list = string_.split(',')
        phrase_token_list = []
        punctuation = [char for char in string.punctuation]

        # Use spacy to extract lemma tags while also excluding punctuations
        for phrase in string_list:
            tokens = self.nlp(phrase)
            lemma_list = []
            for token in tokens:
                if token.text not in punctuation:
                    lemma = token.lemma_
                    text = token.text
                    text_lemma = {text:lemma}
                    lemma_list.append(text_lemma)

            phrase_token_list.append(lemma_list)
        return phrase_token_list

    def lemma_columns(self,df):
        #Created the Lemmatization column based on PARSED_CONTENT
        df['Lemmatization'] = [[self.lemma_extraction(phrase)] for phrase in df['PARSED_CONTENT']]
        return df

    def syntactic_dependency_extraction(self, string_):
        #Extracts syntactic data from a string
        string_split = string_.split(',')
        phrase_token_list = []
        punctuation = [char for char in string.punctuation]
        for phrase in string_split:
            tokens = self.nlp(phrase)
            dep_list = []
            for token in tokens:
                if token.text not in punctuation:
                    dep = token.dep_
                    text = token.text
                    text_dep = {text: dep}
                    dep_list.append(text_dep)
            phrase_token_list.append(dep_list)
        return phrase_token_list

    def syntactic_columns(self,df):
        #Creates the Syntactic Analysis column based on PARSED_CONTENT
        df['Syntactic Analysis'] = [[self.syntactic_dependency_extraction(phrase)]for phrase in df['PARSED_CONTENT']]
        return df

    def length_extraction(self,string_):
        #Extraction the number of words inside a string
        string_split = string_.split(',')
        lengths = []
        for phrase in string_split:
            phrase_list = phrase.split(' ')
            len_phrase = len(phrase_list)
            lengths.append(len_phrase)
        return lengths

    def length_column(self, df):
        #Creates the Phrase length column based on PARSED_CONTENT
        df['Phrase length'] = [[self.length_extraction(phrase)] for phrase in df['PARSED_CONTENT']]
        return df

    def full_analysis(self, df):
        #Pulls everything from the is class together to create a new NLP centric dataframe (used for reddit and youtube)
        first_df = df[['CONTENT', 'PARSED_CONTENT']]
        pos_df = self.pos_columns(first_df)
        lemma_df = self.lemma_columns(pos_df)
        syntax_df = self.syntactic_columns(lemma_df)
        len_df = self.length_column(syntax_df)
        final_df = len_df.drop(columns=['CONTENT'])
        return final_df

    def full_analysis_twitter(self, df):
        #Pulls everything from the is class together to create a new NLP centric dataframe (twitter)
        first_df = df[['TWEET_ID', 'PARSED_CONTENT']]
        pos_df = self.pos_columns(first_df)
        lemma_df = self.lemma_columns(pos_df)
        syntax_df = self.syntactic_columns(lemma_df)
        length_df = self.length_column(syntax_df)
        final_df = length_df.drop(columns=['PARSED_CONTENT'])
        return final_df
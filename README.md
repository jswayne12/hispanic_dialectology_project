# Hispanic Dialectology Project

### Description

This project attempts to reconstruct a truly neutral Spanish. The idea was largely birth out of the understanding of
the limitations of what is currently referred to as 'Neutral Spanish'. 'Neutral Spanish' is an artificial 
dialect meant to be devoid of any dialectal or cultural underpinnings with its focus being on inter-cultural intelligibility.
While I do believe that 'Neutral Spanish' reaches its goal, I question it idea of neutrality. Instead of focusing on 
inter-cultural intelligibility, my project takes a much more statistically based approach. The goal is to find the functional
'average' of the Spanish language. My idea of neutrality is not based on exclusion of dialectal features, rather finding 
Spanish's 'true center'.

Before delving to deep into the methods that I have used, and plan on using, I believe it important to make note of some 
limitations of this project. Firstly, I will not be touching on all the base linguistic field of study. The majority of 
analysis, and therefore reconstruction, will be based on the lexical and syntactic features. There is also the fact that 
the corpus being used to achieve this goal is relatively small and quite context specific (the context being the discussion
of politics on social media platforms). 

Regarding the project plan. It starts with data collection. I extracted data from three social media platforms (Reddit,
Twitter, and Youtube). I pulled from subreddits, tweets, and videos that pertain specifically to the politics of a specific
country. After pulling the data into a pandas dataframe, I did some textual pre-processing as well as extracted nlp-specific
data to facilitate the analysis. Examples of type of data extracted would be lemmas, POS, and syntactic dependency. After 
processing, I used corpus linguistic methods to analyze the data.

Notebooks will be made availible soon.

### How to Install plus additional info

- Access to the code used for data collection, pre-processing, nlp processes, and data storage is availible through github. 
It would only need to be cloned.
- Portions of the code relating to data storage, and social media API will need to be updated for your specific use cases.


### How to use the Project
- As stated earlier, some changes to sql_storage.py will be needed in order to engage in the sql processes.
- The same can be said about the social media API used. You will to create your API keys and apply it to the code
- After code has been cloned, check to make sure all necessary library installations are done. Then simply run the program and follow the instructions as given. 
- The options are given in the order of a usual data project, starting with data collection up to NLP processes, but one can simply choose the process as they need them.
- A new file will soon be added that will hold the functions for corpus data analysis and visualization. 

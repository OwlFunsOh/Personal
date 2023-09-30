import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')

import nltk
#nltk.download()

# Read in data

#This section reads in where the review file is
df = pd.read_csv('Machine Learning\Reviews\Reviews.csv')

#df.shape will show how many rows of data we have
#print(df.shape)

#df.head will get the first 500 rows of data
df = df.head(500)
#print(df.shape)


#value_counts() shows how many reviews got each individual star. Ex: 339 5 star reviews
#sort index will just sort the star rating from 1-5
#then, we plot the bar graph
"""
ax = df['Score'].value_counts().sort_index() \
    .plot(kind='bar',
          title='Count of Reviews by Stars',
          figsize=(10, 5))
ax.set_xlabel('Review Stars')

plt.show()
"""


example = df['Text'][50]
#print(example)

#each word will get it's own token. separated by spaces
tokens = nltk.word_tokenize(example)
#print(tokens[:10])

#tagged will show the part of speech of each word
tagged = nltk.pos_tag(tokens)
#print(tagged[:10])

#chunks everything into a sentence
entities = nltk.chunk.ne_chunk(tagged)
#entities.pprint()

#VADER STUFF *****************************************************************
#compound score = overall score

from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm

#creating a sentiment intensity analyzer object
sia = SentimentIntensityAnalyzer()

#printing the score of a positive sentence
#print(sia.polarity_scores('I am so happy!'))

#printing the score of a negative sentence
#print(sia.polarity_scores('This is the worst thing ever.'))

#run the sia test on oatmeal comment
print(sia.polarity_scores(example))

# Run the polarity score on the entire dataset
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row['Text']
    myid = row['Id']
    res[myid] = sia.polarity_scores(text)
    #print(res[myid])

#use pandas to print out the dataframe
vader = pd.DataFrame(res).T
vader = vader.reset_index().rename(columns={'index': 'Id'})
vader = vader.merge(df, how='left')

#print(vaders)

# Now we have sentiment score and metadata
vader.head()

#ax = sns.barplot(data=vaders, x='Score', y='compound')
#ax.set_title('Compound Score by Amazon Star Review')
#plt.show()

"""
#just plotting
fig, axs = plt.subplots(1, 3, figsize=(12, 3))
sns.barplot(data=vader, x='Score', y='pos', ax=axs[0])
sns.barplot(data=vader, x='Score', y='neu', ax=axs[1])
sns.barplot(data=vader, x='Score', y='neg', ax=axs[2])
axs[0].set_title('Positive')
axs[1].set_title('Neutral')
axs[2].set_title('Negative')
plt.tight_layout()
plt.show()

"""

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Run for Roberta Model
encoded_text = tokenizer(example, return_tensors='pt')
output = model(**encoded_text)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
scores_dict = {
    'roberta_neg' : scores[0],
    'roberta_neu' : scores[1],
    'roberta_pos' : scores[2]
}
print(scores_dict)

def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2]
    }
    return scores_dict

res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        text = row['Text']
        myid = row['Id']
        vader_result = sia.polarity_scores(text)
        vader_result_rename = {}
        for key, value in vader_result.items():
            vader_result_rename[f"vader_{key}"] = value
        roberta_result = polarity_scores_roberta(text)
        both = {**vader_result_rename, **roberta_result}
        res[myid] = both
    #roberta model cant do reviews that are too long
    except RuntimeError:
        print(f'Broke for id {myid}')

results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns={'index': 'Id'})
results_df = results_df.merge(df, how='left')
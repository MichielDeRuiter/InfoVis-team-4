#%%
import pandas as pd
import numpy as np


#%%
# df = df[['SOURCE_SUBREDDIT', 'Positive sentiment calculated by VADER', 'Negative sentiment calculated by VADER', 'Automated readability index']]
# df['pos_neg_sentiment_ratio'] = round(df['Positive sentiment calculated by VADER'] / (df['Positive sentiment calculated by VADER'] + df['Negative sentiment calculated by VADER']) * 100)
# df['readability_index'] = df['Automated readability index'] / df['Automated readability index'].max()


# %%
df = pd.read_csv('../reddit_raw_data/reddit_body_props_seperated_1k.csv')
source_subreddit = df['SOURCE_SUBREDDIT']
anger_sad_columns = df[['LIWC_Anger', 'LIWC_Sad']]

df = df[['Positive sentiment calculated by VADER', 'Negative sentiment calculated by VADER', 'Automated readability index']]
df['pos_neg_sentiment_ratio'] = df['Positive sentiment calculated by VADER'] / (df['Positive sentiment calculated by VADER'] + df['Negative sentiment calculated by VADER'])
df = df.drop(['Positive sentiment calculated by VADER', 'Negative sentiment calculated by VADER'], axis=1)
df = pd.concat([df, anger_sad_columns], axis=1, join='inner')
df = round((df-df.min())/(df.max()-df.min())*100) # Normalize data
df = pd.concat([source_subreddit, df], axis=1, join='inner')
df = df.groupby(['SOURCE_SUBREDDIT']).mean()
# test = test.drop(['Automated readability index'], axis=1)
df = df.reset_index()

df = pd.melt(df, 
            id_vars=['SOURCE_SUBREDDIT'], 
            value_vars=list(df.columns[1:]), # list of days of the week
            # value_vars=["pos_neg_sentiment_ratio", "Automated readability index"] # list of days of the week
            # var_name='Column', 
            # value_name='Sum of Value'
            )

df = df.sort_values(by=['SOURCE_SUBREDDIT', 'variable'])
# del df['index']
df = df.reset_index(drop=True)
df = df.iloc[20:32] # first five rows of dataframe
df = df.rename(columns={'SOURCE_SUBREDDIT': 'group', 'variable': 'axis'})
df.to_csv('static/csv/data_the_avengers.csv', index=False)

#%%
# final_df = test.melt(id_vars=["SOURCE_SUBREDDIT", "Automated readability index"], var_name="Date", value_name="Value")

final_df = (test.set_index(["SOURCE_SUBREDDIT", "Automated readability index"])
         .stack()
         .reset_index(name='Value')
         .rename(columns={'level_2':'Date'}))

# %%
df = pd.DataFrame({'A': {0: 'a', 1: 'b', 2: 'c'},
                   'B': {0: 1, 1: 3, 2: 5},
                   'C': {0: 2, 1: 4, 2: 6}})

dff = pd.melt(df, id_vars=['A'], value_vars=['B', 'C'])

# %%

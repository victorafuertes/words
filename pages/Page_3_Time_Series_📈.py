import streamlit as st
import nltk
nltk.download('punkt')
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import matplotlib.dates as mdates


def tokenize_and_filter(text):
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [token for token in tokens if re.match(r'^\w+$', token)]
    return filtered_tokens

#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:
csv_directory = ('Main_Data.csv')

df = pd.read_csv(csv_directory)

df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

df['Word Count'] = df['Processed Lyrics'].apply(len)

df.drop(columns=['Lyrics','Entry #'], inplace=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

df['Unique Word Count'] = df['Processed Lyrics'].apply(lambda x: len(set(x)))
yearly_stats = df.groupby(df['Year'].dt.year).agg({'Word Count': 'mean', 'Unique Word Count': 'mean'}).reset_index()

time_series_table = pd.DataFrame({
    'Year': pd.date_range(start='2006-01-01', end='2023-01-01', freq='YS').year,
    'Average Word Count': np.nan,
    'Average Unique Word Count': np.nan
})

for index, row in time_series_table.iterrows():
    year = row['Year']
    if year in yearly_stats['Year'].values:
        avg_word_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Word Count'].values[0]
        avg_unique_word_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Unique Word Count'].values[0]
        time_series_table.loc[index, 'Average Word Count'] = avg_word_count
        time_series_table.loc[index, 'Average Unique Word Count'] = avg_unique_word_count
        
plt.figure(figsize=(10, 6))
plt.plot(time_series_table['Year'], time_series_table['Average Word Count'], label='Average Word Count', color='green')
plt.plot(time_series_table['Year'], time_series_table['Average Unique Word Count'], label='Average Unique Word Count', color='lightgreen')
plt.xlabel('Year')
plt.ylabel('Word Count')
plt.legend()
plt.grid(True)

#X AXIS FREQUENCY
plt.xticks(rotation=25)

plt.tight_layout()

st.title('Average Word Count (2006-2023)')
st.pyplot(plt)
st.write('The visualization above shows the fluctuations in word and unique word counts. Although not uniform, ultimately there has been a 10.06 percent decrease in the average unique words per song between 2006 and 2023. Which I initially thought agreed with my hypothesis, however, overall word count also decreased 22.578 percent.')
st.write('This prompted me to want to further analyze the lyrics I had gathered, especially considering how using non-words (like onomatopoeias) seems to be growing in popularity over the years.')
st.title('Average Word Count and Unique Word Count (2006-2023)')
st.table(time_series_table)

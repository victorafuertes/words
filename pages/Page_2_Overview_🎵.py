import streamlit as st
import nltk
nltk.download('punkt')
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# TOKENIZE WORDS
def tokenize_and_filter(text):
    tokens = nltk.word_tokenize(text)
    # Filter out non-alphanumeric tokens
    filtered_tokens = [token for token in tokens if re.match(r'^\w+$', token)]
    return filtered_tokens

# TOKENIZE GENRES
def tokenize_and_split_genres(genres):
    if pd.isna(genres):  # Handle missing values
        return []
    else:
        return re.split(r',\s*', genres)
    
#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:

csv_directory = ('Main_Data.csv')

df = pd.read_csv(csv_directory)

df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

df['Word Count'] = df['Processed Lyrics'].apply(len)

df['Processed Genres'] = df['Genres'].apply(tokenize_and_split_genres)

df['Genre Count'] = df['Processed Genres'].apply(len)

df.drop(columns=['Lyrics', 'Entry #'], inplace=True)


#-------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION II - CREATING VARIABLES AND FUNCTIONS TO BE CALLED IN STREAMLIT: 

# BRIEFS SUMMARY STATS 
TOTAL_WORDS = df['Word Count'].sum()
TOTAL_UNIQUE_WORDS = len(set(word for sublist in df['Processed Lyrics'] for word in sublist))
TOTAL_ENTRIES = len(df)
TOTAL_GENRES = len(set(genre for sublist in df['Processed Genres'] for genre in sublist))
TOTAL_SONGS = df['Title'].nunique()
TOTAL_ARTISTS = df['Artist'].nunique()
AVG_WORD_COUNT_PER_SONG = TOTAL_WORDS / TOTAL_SONGS
#----------------------------------------------------------------------------------------------------------------------------------------------
# SECTION III - STREAMLIT: 

st.title('BRIEF DATA OVERVIEW 👀')
st.write('')
st.text(f'TOTAL ENTRIES 1800: AFTER CLEANING AND FILTERING: {TOTAL_ENTRIES}')
st.text(f'TOTAL UNIQUE ARTISTS: {TOTAL_ARTISTS}')
st.text(f'TOTAL UNIQUE GENRES: {TOTAL_GENRES}')
st.text(f'TOTAL SONGS (Non-Duplicates): {TOTAL_SONGS}')
st.text(f'TOTAL WORDS: {TOTAL_WORDS}')
st.text(f'TOTAL UNIQUE WORDS: {TOTAL_UNIQUE_WORDS}')
st.text(f'AVERAGE WORD COUNT PER SONG: {AVG_WORD_COUNT_PER_SONG}')
st.write('')
st.write('This information helps get an idea of what the dataframe for this project looks like. The dataframe itself can be found in Page 9.')
st.write('I personally would have liked to add more features but due to time constraints and having to scramble through sources + how inaccessible some information seems to be with music APIs.')
st.write('I find the gap between "amount of words" and "unique words" to be particularly interesting.')


 

import streamlit as st
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def tokenize_and_filter(text, remove_stopwords=True):
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [token.lower() for token in tokens if re.match(r'^\w+$', token) and (not remove_stopwords or token.lower() not in stop_words)]
    return filtered_tokens

#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:
csv_directory = ('Main_Data.csv')

df = pd.read_csv(csv_directory)

df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

df['Word Count'] = df['Processed Lyrics'].apply(len)

df.drop(columns=['Lyrics','Entry #'], inplace=True)

def generate_wordcloud(data, column_name, title):
    word_freq = data.value_counts().to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

selected_year = st.sidebar.selectbox('Select a year', sorted(df['Year'].unique()))

selected_data = df[df['Year'] == selected_year]

show_filtered_words = st.sidebar.checkbox("WORD FILTER (remove 'boring' words)")

if show_filtered_words:
    filtered_words = [word for sublist in selected_data['Processed Lyrics'] for word in sublist]
    filtered_words_freq = nltk.FreqDist(filtered_words)
    filtered_words_freq_df = pd.DataFrame.from_dict(filtered_words_freq, orient='index', columns=['Frequency'])
    filtered_words_freq_df.index.name = 'Word'

    generate_wordcloud(filtered_words_freq_df.index, 'Filtered Words', f'Filtered Words Popularity {selected_year}')
else:
    st.subheader("Word Popularity")
    generate_wordcloud(selected_data['Processed Lyrics'].explode(), 'Processed Lyrics', f'Word Popularity in {selected_year}')

#MOST POPULAR GENRES
st.subheader("Genre Popularity")
genres = selected_data['Genres'].str.split(',').explode().str.strip()
generate_wordcloud(genres, 'Genres', f'Genre Popularity in {selected_year}')

#MOST POPULAR ARTISTS 
st.subheader("Artist Popularity")
generate_wordcloud(selected_data['Artist'], 'Artist', f'Artists Popularity in {selected_year}')

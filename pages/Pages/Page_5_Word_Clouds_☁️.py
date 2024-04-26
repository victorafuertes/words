import streamlit as st
import nltk
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords

# Get stopwords (if not already downloaded)
nltk.download('stopwords')

# list of English stopwords
stop_words = set(stopwords.words('english'))

# Function to tokenize and filter out non-alphanumeric tokens and stopwords
def tokenize_and_filter(text, remove_stopwords=True):
    tokens = nltk.word_tokenize(text)
    # Filter out non-alphanumeric tokens and stopwords
    filtered_tokens = [token.lower() for token in tokens if re.match(r'^\w+$', token) and (not remove_stopwords or token.lower() not in stop_words)]
    return filtered_tokens

#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:
csv_directory = ('Main_Data.csv')

df = pd.read_csv(csv_directory)

# Apply tokenization and filtering to the "Lyrics" column
df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

# Count the tokens in each row
df['Word Count'] = df['Processed Lyrics'].apply(len)

# Drop unnecessary columns
df.drop(columns=['Lyrics','Entry #'], inplace=True)

# Create a function to generate word clouds
def generate_wordcloud(data, column_name, title):
    word_freq = data.value_counts().to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

# Year selection in the sidebar
selected_year = st.sidebar.selectbox('Select a year', sorted(df['Year'].unique()))

# Filter data based on selected year
selected_data = df[df['Year'] == selected_year]

# Checkbox to display filtered words
show_filtered_words = st.sidebar.checkbox("WORD FILTER (remove 'boring' words)")

# Get all the filtered words if checkbox is checked
if show_filtered_words:
    # Get all the filtered words
    filtered_words = [word for sublist in selected_data['Processed Lyrics'] for word in sublist]
    filtered_words_freq = nltk.FreqDist(filtered_words)
    filtered_words_freq_df = pd.DataFrame.from_dict(filtered_words_freq, orient='index', columns=['Frequency'])
    filtered_words_freq_df.index.name = 'Word'

    # Display word cloud directly if filtered words
    generate_wordcloud(filtered_words_freq_df.index, 'Filtered Words', f'Filtered Words Popularity {selected_year}')
else:
    # Top 10 most popular words
    st.subheader("Word Popularity")
    generate_wordcloud(selected_data['Processed Lyrics'].explode(), 'Processed Lyrics', f'Word Popularity in {selected_year}')

# Top 10 most popular genres
st.subheader("Genre Popularity")
genres = selected_data['Genres'].str.split(',').explode().str.strip()
generate_wordcloud(genres, 'Genres', f'Genre Popularity in {selected_year}')

# Top 10 most popular artists
st.subheader("Artist Popularity")
generate_wordcloud(selected_data['Artist'], 'Artist', f'Artists Popularity in {selected_year}')

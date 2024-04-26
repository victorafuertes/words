import streamlit as st
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import matplotlib.dates as mdates
from nltk.corpus import stopwords

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Custom list of onomatopoeias and ad libs
custom_stopwords = ['la', 'na', 'oh', 'yeah', 'Ah', 'Eh', 'Oh', 'Uh', 'Ooh', 
                    'ahh', 'ahhh', 'ehh', 'ohh', 'ohhh',
                    'hmm', 'mhm', 'hm', 'mhmm', 'hmmm', 'hmmmmm',
                    'Ha', 'huh', 'ho', 'heh', 'hah', 'Haha', 'hehe', 'hihi', 'hoho', 
                    'ja', 'je', 'ji', 'jo', 'ju', 'jaja', 'jajaja', 'jejeje', 'jijiji',
                    'jojojo', 'jujuju','da', 'de', 'di', 'du', 'da-da-da-da', 
                    'de-de-de-de', 'di-di-di','Ye', 'Yuh', 'yas', 
                    'yup', 'yee', 'uh-huh', 'yass', 'Woo', 
                    'Wee-hoo', 'Yee-hoo', 'woo-hoo', 'woo', 'Ya-hoo', 
                    'whoah', 'whoah-ho', 
                    'La-la', 'la', 'la-di-da', 
                    'sh', 'sho', 'shh', 'shuh', 'sha-ba', 'shabadoobey', 'shoobie',
                    'Ay', 'ayy', 'ayyy', 'ayyyy',
                    'Na-na', 'na', 'nah', 'nuh', 'Hey',
                    'aw', 'aww', 'awww', 'Rr', 'rrr', 'rrrr', 'pr', 'prr', 'prrr',
                    'skrt', 'skrrt', 'skrrrt', 'skiat', 'skeet', 
                    'grr', 'gr', 'grrrr', 'grrrrrrrah', 'git']  # Add more as needed

# Function to tokenize and filter out stopwords, onomatopoeias, and ad libs
def tokenize_and_filter(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    
    # Get English stopwords
    english_stopwords = set(stopwords.words('english'))
    
    # Filter out stopwords, onomatopoeias, and ad libs
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in english_stopwords and token.lower() not in custom_stopwords and re.match(r'^\w+$', token)]
    non_words = [token.lower() for token in tokens if token.lower() in custom_stopwords]
    
    return filtered_tokens, non_words

#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:
csv_directory = 'Main_Data.csv'

df = pd.read_csv(csv_directory)

# Apply tokenization and filtering to the "Lyrics" column
df['Processed Lyrics'], df['Non-Words'] = zip(*df['Lyrics'].apply(tokenize_and_filter))

# Count the tokens in each row
df['Word Count'] = df['Processed Lyrics'].apply(len)
df['Non-Words Count'] = df['Non-Words'].apply(len)

# Drop unnecessary columns
df.drop(columns=['Lyrics','Entry #'], inplace=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------
st.title('TIME-SERIES PART II')
st.write('USE THE SIDEBAR TO DISPLAY THE TIME SERIES DATA FOR NON-WORDS')

# 1. Extract the year from the "Year" column
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# 2. Calculate the average word count, non-word count, and average unique word count for each year
df['Unique Word Count'] = df['Processed Lyrics'].apply(lambda x: len(set(x)))
df['Unique Non-Words Count'] = df['Non-Words'].apply(lambda x: len(set(x)))

yearly_stats = df.groupby(df['Year'].dt.year).agg({
    'Word Count': 'mean', 
    'Unique Word Count': 'mean',
    'Non-Words Count': 'mean',
    'Unique Non-Words Count': 'mean'
}).reset_index()

# 3. Create a time series table
time_series_table = pd.DataFrame({
    'Year': pd.date_range(start='2006-01-01', end='2023-01-01', freq='YS'),
    'Average Word Count': np.nan,
    'Average Unique Word Count': np.nan,
    'Average Non-Words Count': np.nan,
    'Average Unique Non-Words Count': np.nan
})

# 4. Populate the time series table with calculated averages
for index, row in time_series_table.iterrows():
    year = row['Year'].year
    if year in yearly_stats['Year'].values:
        avg_word_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Word Count'].values[0]
        avg_unique_word_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Unique Word Count'].values[0]
        avg_non_words_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Non-Words Count'].values[0]
        avg_unique_non_words_count = yearly_stats.loc[yearly_stats['Year'] == year, 'Unique Non-Words Count'].values[0]
        
        time_series_table.loc[index, 'Average Word Count'] = avg_word_count
        time_series_table.loc[index, 'Average Unique Word Count'] = avg_unique_word_count
        time_series_table.loc[index, 'Average Non-Words Count'] = avg_non_words_count
        time_series_table.loc[index, 'Average Unique Non-Words Count'] = avg_unique_non_words_count

# Add a select box to toggle Non-Words display
show_non_words = st.sidebar.checkbox('Show Non-Words', False)

# Plotting the time series data
plt.figure(figsize=(10, 6))

plt.plot(time_series_table['Year'], time_series_table['Average Word Count'], label='Average Word Count', color='green')
plt.plot(time_series_table['Year'], time_series_table['Average Unique Word Count'], label='Average Unique Word Count', color='lightgreen')

# Customize x-axis tick frequency
plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

# Adjusting y-axis ticks to go by 25's
plt.yticks(np.arange(0, max(time_series_table['Average Word Count']) + 25, 25))

# Adding Non-Words to the plot if selected
if show_non_words:
    plt.plot(time_series_table['Year'], time_series_table['Average Non-Words Count'], label='Average Non-Words Count', color='orange')
    plt.plot(time_series_table['Year'], time_series_table['Average Unique Non-Words Count'], label='Average Unique Non-Words Count', color='yellow')
    plt.title('Average Word Count and Non-Words Count (2006-2023)')
    plt.ylabel('Count')
    plt.legend()

else:
    plt.title('Average Word Count (2006-2023)')
    plt.ylabel('Word Count')
    plt.legend()

plt.xlabel('Year')
plt.grid(True)
plt.tight_layout()

# Display the plot
st.pyplot(plt)

st.write('Upon further investigation I found something that seemed once again, highly counterintuitive.')
st.write("In 2006, average percentage of a song's content that could be considered non-words was 5.55 percent. In 2023 that number seems to be only 4.41 percent. This genuinely came as a surprise to me and I essentially have to accept that my assumptions and initial hypothesis were incorrect.")
st.write("Of course, plenty of factors could have influenced these results; mainly that my results are reflective only of the songs used for this project as well as the timeframe I chose. It also varies seemingly unpredictably by year.") 
st.write("Music is something engraved in culture and directly linked to trends and historical events so its hard to see it as something plain and linear. So, although I would'nt call any of this conclusive evidence, it certainly is very interesting.")
# Convert the 'Year' column to integer type
time_series_table['Year'] = time_series_table['Year'].dt.year

# Calculate percentage of words and non-words for each year
time_series_table['Total Words'] = time_series_table['Average Word Count'] + time_series_table['Average Non-Words Count']
time_series_table['Percentage Words'] = (time_series_table['Average Word Count'] / time_series_table['Total Words']) * 100
time_series_table['Percentage Non-Words'] = (time_series_table['Average Non-Words Count'] / time_series_table['Total Words']) * 100

# Create a new dataframe for the table
percentage_table = pd.DataFrame({
    'Year': time_series_table['Year'].astype(int),  # Convert to integer type to remove commas
    '% Words': time_series_table['Percentage Words'],
    '% Non-Words': time_series_table['Percentage Non-Words']
})

st.header('LYRICAL CONTENT PERCENTAGES: WORDS vs NON-WORDS')

# Display the table
st.write(percentage_table)

# Ensure all years from 2006 to 2023 are included
all_years = np.arange(2006, 2024)

# Create arrays for % Words and % Non-Words for all years, filling NaNs with zeros
percent_words = percentage_table.set_index('Year')['% Words'].reindex(all_years, fill_value=0).values
percent_non_words = percentage_table.set_index('Year')['% Non-Words'].reindex(all_years, fill_value=0).values

# Plotting the bar graph
plt.figure(figsize=(10, 6))

bar_width = 0.35  # Width of the bars

# Plotting % Words
plt.bar(all_years - bar_width/2, percent_words, label='% Words', color='lightgreen', width=bar_width)

# Plotting % Non-Words
plt.bar(all_years + bar_width/2, percent_non_words, label='% Non-Words', color='green', width=bar_width)

# Adding lines across the tops of the bars
plt.plot(all_years - bar_width/2, percent_words, marker='o', color='black', linestyle='-')
plt.plot(all_years + bar_width/2, percent_non_words, marker='o', color='black', linestyle='-')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Percentage of Words and Non-Words Over the Years')
plt.xticks(all_years, rotation=45)  # Rotate x-axis labels for better readability
plt.legend()

# Show plot
st.pyplot(plt)
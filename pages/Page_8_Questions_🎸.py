import streamlit as st

st.title('Rubric Questions')

st.header('NOTABLE CHANGES SINCE MILESTONE 1:')
st.write('Current Data Sources:')
st.write('A) Billboard + Billboard.py (https://www.billboard.com/charts/year-end/2006/hot-100-songs/ + (https://github.com/guoguo12/billboard-charts/blob/master/billboard.py)')
st.write('B) Genius API + LyricsGenius (https://docs.genius.com/) + (https://lyricsgenius.readthedocs.io/en/master/)')
st.write('C) Spotify API (https://developer.spotify.com/documentation/web-api)')
st.write('(previous sources: Billboard, AZLyrics.com, Spotify CSV via Kaggle.com)')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header('RUBRIC QUESTIONS:')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('1) What did you set out to study? (i.e. what was the point of your project?  This should be close to your Milestone 1 assignment, but if you switched gears or changed things, note it here.)')
st.write('')
st.write('My main goal for project was to analyze the changes in the word count of popular song lyrics over the years. My main hypothesis being:')
st.write('Songs have gotten more and more repetitive over the years. I was expecting to find a downward trend in Unique words and an overall increase in word count')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('2) What did you Discover/what were your conclusions (i.e. what were your findings?  Were your original assumptions confirmed, etc.?)')
st.write('')
st.write('I learned that Music, specifically lyrics, from "back then" really arent so different from how it is now. I think people tend to look back on the past a lot through the eyes of nostalgia and that may give rise to common misconceptions and assumptions such as "music was less repetitive back then".')
st.write('I was confronted with unexpected results that went completely against what I thought I would observe. This of course can partly be attributed to my selection of songs, my sample size, my timeframe ("back then" isnt very specific and I could only access as far back as 2006), etc...')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('3) What difficulties did you have in completing the project?')  
st.write('')
st.write('My main limitations all revolved around accessing my data of interest. I think one of the main lessons I learned (from this project specifically) is that music APIs kinda suck at their job.')
st.write('Although, I understand, lots of company policies, privacy policies, protecting the users, etc. It still seems like there was a lot of data that genuinely seemed to be unnecessarily inaccesible')
st.write('')
st.write('I also got myself temporarily banned (on several occasions) from AZLyrics.com while trying to build a scraper that would not be detected by the site which I thought was kind of funny.')
st.write('It genuinely taught me a lot about being more sensible while scraping and trying to adhere to website limitations.')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('4) What skills did you wish you had while you were doing the project?')
st.write('')
st.write('I wish I was better at data visualization. I wish I was better at acquiring data in general (which although I managed to get three sources and in the end I "guess" it worked, my original plan was a lot more ambitious).')
st.write('One of the things this project made me realize is how much I actually want to grow as a data scientist. Even if its just to satisfy my own curiosity.')
st.write('')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.write('5) What would you do “next” to expand or augment the project?')
st.write('')
st.write('I would love to add geospatial data. I think a combination of timeseries and Geospatial data, seeing where certain songs/artists/genres are listened to the most could be very interesting')
st.write('especially when considering sentiment analysis and potentially trying to find some correlation between the sentiment and the weather conditions of the country or region, for example:')
st.write('"Countries with warmer/tropical climates tend to listen to more positive or "upbeat" songs, while countries with colder climates and more frequent rain tend to listen to...')
st.write('I also think that it would be good to expand my catalog of songs further back than 2006.')
st.write('')

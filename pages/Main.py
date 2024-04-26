import streamlit as st
import nltk
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.title('DSCI:510 FINAL PROJECT 📊')
st.subheader('VICTOR ABREU FUERTES UID:7879-2731-50')
st.write('')
st.write('')
st.header('WEBAPP/PROJECT EXPLANATION 📝')#An explanation of how to use your webapp: what interactivity there is, what the plots/charts mean, what your conclusions were, etc.
st.write('')
st.write('Throughout this app there are multiple pages which will present the findings of this project in a simple manner. Some of these pages will be interactive, allowing the user to explore beyond what is initially presented to them.')
st.write('On the lefthand side of your screen, you can find a sidebar containing the available pages of this project, along with a brief description of the contents of each page.')
st.write('')
st.text('INTERACTIVE PAGES: PAGE 4, PAGE 5, PAGE 7.')
st.write('')
st.write('')
st.header('BUGS/AREAS TO BE IMPROVED 🐜')#Any major “gotchas” (i.e. things that don’t work, go slowly, could be improved, etc.)
st.write('')
st.write('Honestly I feel like I got things working as intended. I think the main area(s) that I could improve upon, specifically in the context of this project, would be: amount of features, observations and sources (which I will touch upon later on in the questions page).')
st.write('')
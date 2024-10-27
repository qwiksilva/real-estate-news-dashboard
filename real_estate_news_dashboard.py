# Step 1: Install necessary libraries
# !pip install streamlit pandas eventregistry

import streamlit as st
import pandas as pd
# import requests
# import matplotlib.pyplot as plt

from eventregistry import EventRegistry, QueryArticlesIter

# Step 2: Fetch real estate news data
API_KEY = '25b445b9-a592-4014-a0c0-cd18a0428c79'  # Replace with your NewsAPI key
# NEWS_API_URL = 'https://newsapi.org/v2/everything?q=real%20estate&apiKey=' + API_KEY
NEWS_API_URL = 'https://newsapi.ai/api/v1/article/getArticles?query=%7B%22%24query%22%3A%7B%22conceptUri%22%3A%22http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FReal_estate%22%7D%2C%22%24filter%22%3A%7B%22forceMaxDataTimeWindow%22%3A%2231%22%7D%7D&resultType=articles&articlesSortBy=date&apiKey=25b445b9-a592-4014-a0c0-cd18a0428c79&callback=JSON_CALLBACK'
# response = requests.get(NEWS_API_URL)

er = EventRegistry(apiKey = API_KEY)
query = {
  "$query": {
    "$and": [
      {
        "conceptUri": "http://en.wikipedia.org/wiki/Real_estate"
      },
      {
        "lang": "eng"
      }
    ]
  },
  "$filter": {
    "forceMaxDataTimeWindow": "31"
  }
}
q = QueryArticlesIter.initWithComplexQuery(query)

# Step 3: Process the data
# articles = news_data['articles']
# news_df = pd.DataFrame(articles)
articles = []
# change maxItems to get the number of results that you want
for article in q.execQuery(er, maxItems=25):
    articles.append(article)

news_df = pd.DataFrame(articles)

# Step 4: Create a Streamlit dashboard
st.title('Real Estate News Dashboard')

# Search bar to filter news articles
search_query = st.text_input('Search News', '')

if search_query:
    filtered_df = news_df[news_df['title'].str.contains(search_query, case=False)]
else:
    filtered_df = news_df

# Display news articles
for index, row in filtered_df.iterrows():
    st.subheader(row['title'])
    st.write(row['body'])
    st.write(f"[Read more]({row['url']})")


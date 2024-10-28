import os
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=os.environ["GEMINI_API_KEY"])

# /v2/everything
all_articles = newsapi.get_everything(q='festivals',
                                      sources='bbc-news, cnn',
                                      domains='bbc.co.ca',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()
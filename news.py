import re
from gnews import GNews
from datetime import datetime, timedelta

def search_news(page_name, prediction_date):
    # Clean up the topic name
    cleaned_topic = re.sub(r'^\d+_|_en$', '', page_name)
    cleaned_topic = cleaned_topic.replace('_', ' ')

    # Convert the prediction_date to a datetime object
    start_date = datetime.strptime(prediction_date, "%Y-%m-%d")
    end_date = start_date - timedelta(days=7)  # 7 days before the prediction_date
    
    # Initialize GNews object
    gnews = GNews(
        language='en',
        country='CA',
        start_date=end_date,  # Pass datetime object directly
        end_date=start_date,  # Pass datetime object directly
        max_results=30,
    )

    # Search for news articles
    articles = gnews.get_news(cleaned_topic)

    # Process the articles to return the required information
    result = []
    for article in articles:
        article_data = {
            'title': article['title'],
            'publisher': article['publisher'],
            'summary': article['description'],
        }
        result.append(article_data)
    
    return result
import json
from news import search_news
from arima import predict_views
from llm import refine_predictions
from cache import add_cache, remove_cache

def main():
    try:
        # Prompt the user for inputs
        page_name = input("Enter the page name: ").strip()
        prediction_date = input("Enter the prediction date (YYYY-MM-DD): ").strip()

        if not page_name or not prediction_date:
            print("Error: Both 'page_name' and 'prediction_date' are required.")
            return
        
        # Call the predict_views function
        prediction = predict_views(page_name, prediction_date)

        # Search for relevant news articles
        relevant_news = search_news(page_name, prediction_date)

        # Refine predictions using the LLM
        llm_prediction = refine_predictions(prediction, relevant_news)

        # Update cache based on LLM recommendation
        if llm_prediction.get('cache_recommendation', False):
            add_cache(page_name)
        else:
            remove_cache(page_name)

        # Display the results
        print(json.dumps({"response": llm_prediction}, indent=4))
    
    except Exception as e:
        # Handle errors gracefully
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

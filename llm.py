import os
import google.generativeai as genai
import json

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to refine predicted Wikipedia page views and decide cache recommendation
def refine_predictions(arima_predicted_value: float, news_articles: list):
    """
    Refines predictions for Wikipedia page views based on ARIMA values and news articles.

    Args:
        arima_predicted_value (float): Predicted views from the ARIMA model.
        news_articles (list): A list of dictionaries containing news article details.

    Returns:
        dict: The refined prediction and cache recommendation in JSON format.
    """
    # Construct the input_message dynamically
    input_message = f"""
        Refine the predicted Wikipedia page views and decide whether the page should be cached.
        Initial predicted views (ARIMA model): {arima_predicted_value}.
        News articles related to the page:
        {[{
            f"Title: {article['title']}, Publisher: {article['publisher']}, Summary: {article['summary']}"
            for article in news_articles
        }]}
        Please provide the following details in JSON format:
        - ARIMA prediction score
        - Refined predicted views
        - Cache recommendation (true/false)
        - Reasoning for the recommendation
    """

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a chat session with history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Refine the predicted Wikipedia page views for the following data and decide whether the page should be cached.\n\nInputs:\n- Page Name: \"2015_in_film_en\"\n- Predicted Views: 14595.800598904765\n- News Articles:\n  [\n    { \"title\": \"Oscars 2015: A Look Back at Memorable Moments\", \"source\": \"Variety\", \"summary\": \"Retrospective article on notable moments from the 2015 Oscars.\" },\n    { \"title\": \"Analysis: Box Office Trends from 2015 to 2024\", \"source\": \"Deadline\", \"summary\": \"Insights into box office performance trends for films from 2015.\" }\n  ]\n\nOutput:\nProvide the refined prediction and reasons in the following JSON format:\n",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```json\n{\n  \"page_name\": \"2015_in_film_en\",\n  \"initial_predicted_views\": 14595.800598904765,\n  \"refined_predicted_views\": 17000,\n  \"cache_recommendation\": true,\n  \"reasoning\": [\n    \"The initial prediction of 14595 views is reasonable but can be adjusted upward due to the presence of relevant news articles.\",\n    \"The two news articles, one a retrospective on the 2015 Oscars and the other analyzing box office trends starting from 2015, suggest increased user interest in 2015 films.  These articles are likely to drive traffic to the Wikipedia page.\",\n    \"A 16% increase (from ~14600 to ~17000) accounts for the potential traffic boost from these articles. This is a conservative estimate; the actual increase could be higher or lower depending on various factors like article virality and time of year.\",\n    \"Caching the page is recommended because of the relatively high predicted view count (even the initial prediction) and the likelihood of sustained interest given the articles' topics.  Caching will improve page load times and reduce server load.\"\n  ]\n}\n```",
                ],
            },
        ]
    )

    # Send the user input message and get the response
    response = chat_session.send_message(input_message)

    # Extract JSON from the response
    response_text = response.text

    # Locate the JSON block
    start_idx = response_text.find("{")
    end_idx = response_text.rfind("}") + 1
    json_block = response_text[start_idx:end_idx]

    # Parse the JSON
    try:
        refined_data = json.loads(json_block)
        return refined_data
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

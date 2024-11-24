import os
from news import search_news
from arima import predict_views
from llm import refine_predictions
import google.generativeai as genai
from flask import Flask, request, jsonify
from cache import add_cache, remove_cache

# Configure the GenAI API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)

@app.route('/predict', methods=['POST']) # Corrected 'method' to 'methods' (Flask syntax)
def predict():
    try:
        # Parse the request body (assumes JSON input)
        data = request.get_json()
        
        # Extract page_name and prediction_date from the request body
        page_name = data.get('page_name')
        prediction_date = data.get('prediction_date')

        if not page_name or not prediction_date:
            return jsonify({"error": "Missing 'page_name' or 'prediction_date' in request body."}), 400

        # Call the predict_views function
        prediction = predict_views(page_name, prediction_date)

        relevant_news = search_news(page_name, prediction_date)

        llm_prediction = refine_predictions(prediction, relevant_news)

        if llm_prediction['cache_recommendation']:
            add_cache(page_name)
        else:    
            remove_cache(page_name)

        return jsonify({"response": llm_prediction}), 200
    
    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

add_cache
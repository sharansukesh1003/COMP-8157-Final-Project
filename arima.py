import os
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Paths
DATA_PATH = os.path.join("training", "data", "cleaned_data.csv")

# Function to preprocess and reshape the dataset
def preprocess_data():
    """
    Reads and reshapes the dataset to have 'Page', 'Date', and 'Views' columns.

    Returns:
        pd.DataFrame: Reshaped dataframe with 'Page', 'Date', and 'Views'.
    """
    # Read the data
    df = pd.read_csv(DATA_PATH)

    # Reshape the data from wide to long format
    df_reshaped = df.melt(id_vars=["Page"], var_name="Date", value_name="Views")

    # Convert Date column to datetime format (adjusting to the actual format in your data)
    df_reshaped["Date"] = pd.to_datetime(df_reshaped["Date"], format="%Y-%m-%d %H:%M")

    return df_reshaped

# Function to train a new ARIMA model
def train_arima_model(page_data):
    """
    Trains an ARIMA model for the given page data.

    Args:
        page_data (pd.DataFrame): Dataframe containing 'Views' for a single page.

    Returns:
        SARIMAXResults: Trained ARIMA model.
    """
    # Handle missing values using rolling mean
    page_data['Views'] = page_data['Views'].fillna(page_data['Views'].rolling(30, min_periods=1).mean())

    # Train ARIMA model
    arima_model = SARIMAX(page_data['Views'], order=(2, 1, 2))  # Adjust order as needed
    arima_result = arima_model.fit(disp=False)

    return arima_result

# Function to predict views for a specific page and date
def predict_views(page_name, prediction_date):
    """
    Predict the number of views for a specific page and date.

    Args:
        page_name (str): Name of the page to predict views for.
        prediction_date (str): Target prediction date in 'YYYY-MM-DD'.

    Returns:
        float: Predicted number of views.
    """
    df = preprocess_data()
    # Ensure the date is in datetime format
    prediction_date = pd.to_datetime(prediction_date)

    # Filter data for the specified page
    page_data = df[df['Page'] == page_name].copy()

    if page_data.empty:
        raise ValueError(f"No data found for page '{page_name}'.")

    # Set the 'Date' column as the index
    page_data.set_index('Date', inplace=True)
    page_data = page_data.loc[:prediction_date - pd.Timedelta(days=1)]

    # Load or train ARIMA model
    arima_model = train_arima_model(page_data)

    # Predict views for the specified date
    steps = (prediction_date - page_data.index[-1]).days

    if steps <= 0:
        raise ValueError("Prediction date must be in the future relative to training data.")

    forecast = arima_model.get_forecast(steps=steps)
    prediction = forecast.predicted_mean.iloc[-1]

    return max(0, prediction)  # Ensure no negative predictions

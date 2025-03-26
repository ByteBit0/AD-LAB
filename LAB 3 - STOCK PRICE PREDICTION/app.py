from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)

STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

def load_models(stock):
    try:
        lstm_model = load_model(f'models/{stock}_lstm_model.h5', custom_objects={'mse': MeanSquaredError()})
        linear_model = joblib.load(f'models/{stock}_linear_model.pkl')
        scaler = joblib.load(f'models/{stock}_scaler.pkl')
        return lstm_model, linear_model, scaler
    except Exception as e:
        raise RuntimeError(f"Error loading models for {stock}: {e}")

def prepare_data(data, lookback=60):
    X = []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
    return np.array(X)

@app.route('/')
def home():
    return render_template('index.html', stocks=STOCKS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        stock = request.json.get('stock')
        model_type = request.json.get('model_type')

        if not stock or not model_type:
            return jsonify({'error': 'Stock and model type are required'}), 400
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)
        df = yf.download(stock, start=start_date, end=end_date)

        if df.empty:
            return jsonify({'error': 'No data found for the given stock'}), 404

        lstm_model, linear_model, scaler = load_models(stock)

        # Extract closing prices and dates properly
        data = df['Close'].values.reshape(-1, 1)
        dates = df.index.strftime('%Y-%m-%d').tolist()
        historical = df['Close'].values.tolist()

        # Scale data
        scaled_data = scaler.transform(data)
        X = prepare_data(scaled_data)

        if X.shape[0] == 0:
            return jsonify({'error': 'Not enough data to make predictions'}), 400

        predictions = {}

        if model_type in ['lstm', 'comparison']:
            lstm_pred = lstm_model.predict(X)
            lstm_pred = scaler.inverse_transform(lstm_pred)
            predictions['lstm'] = lstm_pred.flatten().tolist()

        if model_type in ['linear', 'comparison']:
            X_2d = X.reshape(X.shape[0], -1)
            linear_pred = linear_model.predict(X_2d)
            linear_pred = scaler.inverse_transform(linear_pred.reshape(-1, 1))
            predictions['linear'] = linear_pred.flatten().tolist()

        return jsonify({
            'dates': dates[60:], 
            'historical': historical[60:],
            'predictions': predictions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

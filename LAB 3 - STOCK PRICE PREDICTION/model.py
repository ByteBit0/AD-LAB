# Install required libraries
# Import libraries
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Download stock price dataset
ticker = 'AAPL'  # Example: Apple stock
data = yf.download(ticker, start="2015-01-01", end="2023-01-01")
data.reset_index(inplace=True)

# Preprocessing
if 'Close' not in data.columns:
    raise KeyError("'Close' column not found in the dataset.")
    
data['Date'] = pd.to_datetime(data['Date'])
data['Close'] = data['Close'].fillna(method='ffill')  # Fill missing values

# Ensure there is enough data for processing
if len(data) < 11:  # LSTM requires a sequence length of at least 10
    raise ValueError("Dataset has insufficient rows for processing.")

# Features and labels
X = np.array(range(len(data['Close']))).reshape(-1, 1)
y = data['Close'].values

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)

# Prepare data for LSTM
seq_length = 10
X_lstm = []
y_lstm = []
for i in range(len(y) - seq_length):
    X_lstm.append(y[i:i + seq_length])
    y_lstm.append(y[i + seq_length])

X_lstm, y_lstm = np.array(X_lstm), np.array(y_lstm)
X_lstm = X_lstm.reshape((X_lstm.shape[0], X_lstm.shape[1], 1))

# Check if LSTM data is sufficient
if len(X_lstm) < 1:
    raise ValueError("Insufficient data for LSTM training.")

# Train-test split for LSTM
split = int(0.8 * len(X_lstm))
X_train_lstm, X_test_lstm = X_lstm[:split], X_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

# LSTM Model
lstm_model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
    LSTM(50),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train_lstm, y_train_lstm, epochs=20, batch_size=32)

# Predictions
lstm_predictions = lstm_model.predict(X_test_lstm)

# Compare models
lr_mse = mean_squared_error(y_test, lr_predictions[:len(y_test)])
lstm_mse = mean_squared_error(y_test_lstm, lstm_predictions)
print(f"Linear Regression MSE: {lr_mse}")
print(f"LSTM MSE: {lstm_mse}")

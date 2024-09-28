import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    df['SMA_20'] = df['Close'].rolling(window=window).mean()
    df['STD_20'] = df['Close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA_20'] + (df['STD_20'] * num_std_dev)
    df['Lower Band'] = df['SMA_20'] - (df['STD_20'] * num_std_dev)
    return df

def calculate_rsi(df, window=14):
    delta = df['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                          open=df['Open'],
                                          high=df['High'],
                                          low=df['Low'],
                                          close=df['Close'],
                                          name='Candlestick')])
    fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig, use_container_width=True)

def plot_bollinger_bands(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Upper Band'], mode='lines', name='Upper Band', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Lower Band'], mode='lines', name='Lower Band', line=dict(color='green')))
    fig.update_layout(title='Bollinger Bands', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig, use_container_width=True)

def plot_rsi(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='purple')))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="bottom right")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom right")
    fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI')
    st.plotly_chart(fig, use_container_width=True)

# Streamlit UI
st.set_page_config(page_title="Advanced Stock Market Screener", layout="wide")
st.title("📈 Advanced Stock Market Screener")
st.sidebar.header("Stock Input")
stock_symbol = st.sidebar.text_input("Enter stock symbol (e.g., AAPL)", "")

if stock_symbol:
    with st.spinner("Fetching stock data..."):
        stock_data = yf.download(stock_symbol, period='3mo', interval='1d')

        if stock_data.empty:
            st.error("No data found for the ticker")
        else:
            # Perform calculations
            stock_data = calculate_bollinger_bands(stock_data)
            stock_data = calculate_rsi(stock_data)

            # Display the last few rows of the data
            st.subheader("Stock Data")
            st.write(stock_data.tail())

            # Plotting the Candlestick chart
            st.subheader("Candlestick Chart")
            plot_candlestick(stock_data)

            # Plotting the Bollinger Bands
            st.subheader("Bollinger Bands")
            plot_bollinger_bands(stock_data)

            # Plotting the RSI
            st.subheader("Relative Strength Index (RSI)")
            plot_rsi(stock_data)

st.sidebar.header("About")
st.sidebar.text("This app allows you to analyze stock data with interactive charts for Bollinger Bands, RSI, and Candlestick patterns.")

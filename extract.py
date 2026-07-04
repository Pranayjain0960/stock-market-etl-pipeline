"""
extract.py

Downloads historical stock data using yfinance
and saves it as a CSV file.
"""

import os
import pandas as pd
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

DATA_DIR = "data"
RAW_FILE_PATH = os.path.join(DATA_DIR, "raw_stock_data.csv")


def fetch_stock_data(tickers, start_date, end_date):
    all_data = []

    for ticker in tickers:
        print(f"Fetching data for {ticker}...")

        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        hist.reset_index(inplace=True)
        hist["Ticker"] = ticker

        all_data.append(hist)

    combined_df = pd.concat(all_data, ignore_index=True)

    return combined_df


def save_raw_data(df, path):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(path, index=False)

    print(f"Raw data saved to: {path}")
    print(f"Total rows extracted: {len(df)}")


if __name__ == "__main__":
    raw_df = fetch_stock_data(TICKERS, START_DATE, END_DATE)
    save_raw_data(raw_df, RAW_FILE_PATH)

    print("\nPreview of raw data:")
    print(raw_df.head())
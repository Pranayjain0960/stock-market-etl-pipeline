"""
transform.py

Reads the raw stock data, cleans and transforms it,
then saves the cleaned data as a CSV file.
"""

import os
import pandas as pd

DATA_DIR = "data"
RAW_FILE_PATH = os.path.join(DATA_DIR, "raw_stock_data.csv")
CLEANED_FILE_PATH = os.path.join(DATA_DIR, "cleaned_stock_data.csv")


def load_raw_data(path):
    df = pd.read_csv(path)
    return df


def clean_data(df):
    df.columns = [col.lower() for col in df.columns]

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_localize(None)

    essential_columns = ["date", "open", "high", "low", "close", "volume", "ticker"]
    before_rows = len(df)
    df.dropna(subset=essential_columns, inplace=True)
    print(f"Dropped {before_rows - len(df)} rows with missing values.")

    before_rows = len(df)
    df.drop_duplicates(subset=["ticker", "date"], inplace=True)
    print(f"Removed {before_rows - len(df)} duplicate rows.")

    df.sort_values(by=["ticker", "date"], inplace=True)

    df["daily_return"] = df.groupby("ticker")["close"].pct_change() * 100
    df["daily_return"] = df["daily_return"].round(2)
    df["daily_return"] = df["daily_return"].fillna(0)

    final_columns = [
        "ticker",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "daily_return",
    ]
    df = df[final_columns]

    df.reset_index(drop=True, inplace=True)

    return df


def save_cleaned_data(df, path):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned data saved to: {path}")
    print(f"Total rows after cleaning: {len(df)}")


if __name__ == "__main__":
    raw_df = load_raw_data(RAW_FILE_PATH)
    cleaned_df = clean_data(raw_df)
    save_cleaned_data(cleaned_df, CLEANED_FILE_PATH)

    print("\nPreview of cleaned data:")
    print(cleaned_df.head())
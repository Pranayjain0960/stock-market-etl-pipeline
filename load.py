"""
load.py

Loads the cleaned stock data into a MySQL database.
"""

import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()

DATA_DIR = "data"
CLEANED_FILE_PATH = os.path.join(DATA_DIR, "cleaned_stock_data.csv")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "stock_market_db"),
}

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    daily_return FLOAT,
    UNIQUE KEY unique_ticker_date (ticker, date)
);
"""

INSERT_QUERY = """
INSERT INTO stock_data (ticker, date, open, high, low, close, volume, daily_return)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    open = VALUES(open),
    high = VALUES(high),
    low = VALUES(low),
    close = VALUES(close),
    volume = VALUES(volume),
    daily_return = VALUES(daily_return);
"""


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_QUERY)
    connection.commit()
    cursor.close()
    print("Table 'stock_data' is ready.")


def load_data_to_mysql(connection, df):
    cursor = connection.cursor()

    rows_inserted = 0

    for _, row in df.iterrows():
        date_value = row["date"]
        date_str = (
            date_value.strftime("%Y-%m-%d")
            if hasattr(date_value, "strftime")
            else date_value
        )

        values = (
            row["ticker"],
            date_str,
            float(row["open"]),
            float(row["high"]),
            float(row["low"]),
            float(row["close"]),
            int(row["volume"]),
            float(row["daily_return"]),
        )

        cursor.execute(INSERT_QUERY, values)
        rows_inserted += 1

    connection.commit()
    cursor.close()

    print(f"Inserted/updated {rows_inserted} rows into stock_data table.")


if __name__ == "__main__":
    cleaned_df = pd.read_csv(CLEANED_FILE_PATH, parse_dates=["date"])

    conn = get_connection()

    try:
        create_table(conn)
        load_data_to_mysql(conn, cleaned_df)
    finally:
        conn.close()
        print("MySQL connection closed.")
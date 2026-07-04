"""
main.py

Runs the complete ETL pipeline.
"""

from extract import (
    fetch_stock_data,
    save_raw_data,
    TICKERS,
    START_DATE,
    END_DATE,
    RAW_FILE_PATH,
)
from transform import (
    load_raw_data,
    clean_data,
    save_cleaned_data,
    CLEANED_FILE_PATH,
)
from load import get_connection, create_table, load_data_to_mysql


def run_pipeline():
    print("=" * 60)
    print("STEP 1/3: EXTRACT - Fetching data from Yahoo Finance")
    print("=" * 60)

    raw_df = fetch_stock_data(TICKERS, START_DATE, END_DATE)
    save_raw_data(raw_df, RAW_FILE_PATH)

    print("\n" + "=" * 60)
    print("STEP 2/3: TRANSFORM - Cleaning data with Pandas")
    print("=" * 60)

    raw_df_loaded = load_raw_data(RAW_FILE_PATH)
    cleaned_df = clean_data(raw_df_loaded)
    save_cleaned_data(cleaned_df, CLEANED_FILE_PATH)

    print("\n" + "=" * 60)
    print("STEP 3/3: LOAD - Inserting data into MySQL")
    print("=" * 60)

    connection = get_connection()

    try:
        create_table(connection)
        load_data_to_mysql(connection, cleaned_df)
    finally:
        connection.close()

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
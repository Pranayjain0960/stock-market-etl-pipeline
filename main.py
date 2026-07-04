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
   

    raw_df = fetch_stock_data(TICKERS, START_DATE, END_DATE)
    save_raw_data(raw_df, RAW_FILE_PATH)


    raw_df_loaded = load_raw_data(RAW_FILE_PATH)
    cleaned_df = clean_data(raw_df_loaded)
    save_cleaned_data(cleaned_df, CLEANED_FILE_PATH)


    connection = get_connection()

    try:
        create_table(connection)
        load_data_to_mysql(connection, cleaned_df)
    finally:
        connection.close()

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
# Stock Market ETL Pipeline

A beginner-friendly Data Engineering project that builds a simple ETL (Extract, Transform, Load) pipeline using Python, Pandas, MySQL, and the Yahoo Finance API.

The pipeline downloads historical stock market data, performs basic data cleaning and transformation, and loads the processed data into MySQL for SQL-based analysis.

---

## Project Objective

The goal of this project is to understand the fundamentals of a batch ETL pipeline by working with real-world stock market data.

The pipeline performs the following tasks:

- Extracts historical stock data using the Yahoo Finance API
- Saves the raw dataset as a CSV file
- Cleans and transforms the data using Pandas
- Calculates daily stock returns
- Loads the cleaned dataset into MySQL
- Runs SQL queries for analysis

---

## Technologies Used

- Python
- Pandas
- MySQL
- yfinance
- mysql-connector-python
- SQL
- python-dotenv

---

## Project Structure

```text
stock-market-etl/
│
├── data/
│   ├── raw_stock_data.csv
│   └── cleaned_stock_data.csv
│
├── extract.py
├── transform.py
├── load.py
├── main.py
├── analysis.sql
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Workflow

### 1. Extract

Downloads approximately two years of historical stock data for:

- AAPL
- MSFT
- GOOGL
- TSLA
- NVDA

The raw dataset is stored in:

```
data/raw_stock_data.csv
```

---

### 2. Transform

The extracted dataset is cleaned by:

- Removing missing values
- Removing duplicate records
- Converting the Date column to datetime
- Renaming column names to lowercase
- Calculating Daily Return for each stock

The cleaned data is saved as:

```
data/cleaned_stock_data.csv
```

---

### 3. Load

The cleaned dataset is loaded into a MySQL table named:

```
stock_data
```

The pipeline uses an **UPSERT** approach (`ON DUPLICATE KEY UPDATE`) so running it multiple times does not create duplicate records.

---

## SQL Analysis

The `analysis.sql` file contains queries for:

- Highest closing price
- Average closing price
- Monthly average closing price
- Highest trading volume
- Top trading days
- Daily return analysis
- GROUP BY
- ORDER BY
- Common Table Expressions (CTEs)
- Window Functions

---

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create MySQL database

```sql
CREATE DATABASE stock_market_db;
```

### Create a `.env` file

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=stock_market_db
```

### Run the pipeline

```bash
python main.py
```

---

## Sample Output

```
STEP 1/3 : Extract
✔ Downloaded stock data

STEP 2/3 : Transform
✔ Data cleaned successfully

STEP 3/3 : Load
✔ Data loaded into MySQL

Pipeline completed successfully.
```

---

## Future Improvements

Some possible improvements include:

- Scheduling the pipeline using cron or Windows Task Scheduler
- Adding more stock symbols
- Building a Streamlit dashboard
- Exporting reports automatically
- Writing unit tests

---

## Author

**Pranay Jain**

B.Tech Information Technology

Interested in Data Engineering, ETL Pipelines, SQL, and Python.
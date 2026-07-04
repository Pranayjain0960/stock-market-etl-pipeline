USE stock_market_db;

-- 1. Highest closing price for each company
SELECT
    ticker,
    MAX(close) AS highest_close
FROM stock_data
GROUP BY ticker
ORDER BY highest_close DESC;

-- 2. Average closing price by company
SELECT
    ticker,
    ROUND(AVG(close), 2) AS avg_close
FROM stock_data
GROUP BY ticker
ORDER BY avg_close DESC;

-- 3. Monthly average closing price
SELECT
    ticker,
    DATE_FORMAT(date, '%Y-%m') AS month,
    ROUND(AVG(close), 2) AS avg_monthly_close
FROM stock_data
GROUP BY ticker, DATE_FORMAT(date, '%Y-%m')
ORDER BY ticker, month;

-- 4. Highest trading volume day for each company
SELECT
    ticker,
    date,
    volume
FROM stock_data s
WHERE volume = (
    SELECT MAX(volume)
    FROM stock_data
    WHERE ticker = s.ticker
)
ORDER BY volume DESC;

-- 5. Top 5 trading days by volume
SELECT
    ticker,
    date,
    volume
FROM stock_data
ORDER BY volume DESC
LIMIT 5;

-- 6. Top 5 daily gains
SELECT
    ticker,
    date,
    daily_return
FROM stock_data
ORDER BY daily_return DESC
LIMIT 5;

-- 7. Top 5 daily losses
SELECT
    ticker,
    date,
    daily_return
FROM stock_data
ORDER BY daily_return ASC
LIMIT 5;

-- 8. Average daily return and volatility
SELECT
    ticker,
    ROUND(AVG(daily_return), 3) AS avg_daily_return,
    ROUND(STDDEV(daily_return), 3) AS volatility
FROM stock_data
GROUP BY ticker
ORDER BY volatility DESC;

-- 9. Count of up, down, and flat days
SELECT
    ticker,
    CASE
        WHEN daily_return > 0 THEN 'Up'
        WHEN daily_return < 0 THEN 'Down'
        ELSE 'Flat'
    END AS movement,
    COUNT(*) AS num_days
FROM stock_data
GROUP BY ticker, movement
ORDER BY ticker, movement;

-- 10. 7-day moving average (Window Function)
SELECT
    ticker,
    date,
    close,
    ROUND(
        AVG(close) OVER (
            PARTITION BY ticker
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_7day
FROM stock_data
ORDER BY ticker, date;

-- 11. Rank closing prices (Window Function)
SELECT
    ticker,
    date,
    close,
    RANK() OVER (
        PARTITION BY ticker
        ORDER BY close DESC
    ) AS close_rank
FROM stock_data
ORDER BY ticker, close_rank;

-- 12. Best trading day for each company (CTE)
WITH ranked_returns AS (
    SELECT
        ticker,
        date,
        daily_return,
        ROW_NUMBER() OVER (
            PARTITION BY ticker
            ORDER BY daily_return DESC
        ) AS rn
    FROM stock_data
)
SELECT
    ticker,
    date,
    daily_return
FROM ranked_returns
WHERE rn = 1
ORDER BY daily_return DESC;

-- 13. Companies above the overall average closing price (CTE)
WITH overall_avg AS (
    SELECT AVG(close) AS market_avg_close
    FROM stock_data
),
company_avg AS (
    SELECT
        ticker,
        AVG(close) AS avg_close
    FROM stock_data
    GROUP BY ticker
)
SELECT
    c.ticker,
    ROUND(c.avg_close, 2) AS avg_close,
    ROUND(o.market_avg_close, 2) AS market_avg
FROM company_avg c
JOIN overall_avg o
ON c.avg_close > o.market_avg_close
ORDER BY c.avg_close DESC;

-- 14. Dataset summary
SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    COUNT(*) AS total_rows
FROM stock_data;
-- Advanced Analytical Patterns

-- 1. Compute z-score normalization of customer credit limits.
SELECT
  cust_id,
  cust_credit_limit,
  ROUND((cust_credit_limit - AVG(cust_credit_limit) OVER ()) 
    / STDDEV(cust_credit_limit) OVER (), 2) AS z_score
FROM sh.customers;

-- 2. Calculate the Gini coefficient of credit limit inequality per country.
-- Formula*
SELECT
  country_id,
  1 - (2 * SUM((rn / total_n) * credit) / SUM(credit)) AS gini_coeff
FROM (
  SELECT
    country_id,
    cust_credit_limit AS credit,
    ROW_NUMBER() OVER (PARTITION BY country_id ORDER BY cust_credit_limit) AS rn,
    COUNT(*) OVER (PARTITION BY country_id) AS total_n
  FROM sh.customers
  WHERE cust_credit_limit IS NOT NULL
) t
GROUP BY country_id;

-- 3. Find customers whose credit limit is above the 75th percentile and below the 90th percentile.
SELECT
  cust_id,
  cust_credit_limit
FROM (
  SELECT
    cust_id,
    cust_credit_limit,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY cust_credit_limit) OVER () AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY cust_credit_limit) OVER () AS p90
  FROM sh.customers
) t
WHERE cust_credit_limit > p75
  AND cust_credit_limit < p90;

-- 4. Use analytical functions to compute the rank difference between two states.
-- Maharashtra
-- England - Greater London

SELECT
  cust_state_province,
  cust_id,
  total_sales,
  RANK() OVER (PARTITION BY cust_state_province ORDER BY total_sales DESC) AS state_rank
FROM (
  SELECT
    cu.cust_state_province,
    cu.cust_id,
    SUM(s.amount_sold) AS total_sales
  FROM sh.customers cu
  JOIN sh.sales s ON cu.cust_id = s.cust_id
  GROUP BY cu.cust_state_province, cu.cust_id
) t
WHERE cust_state_province IN ('Maharashtra','England - Greater London');

-- 5. Find the median and interquartile range of credit limit per state.
SELECT
  cust_state_province,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cust_credit_limit) AS median_credit,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY cust_credit_limit) -
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY cust_credit_limit) AS iqr_credit
FROM sh.customers
GROUP BY cust_state_province;

-- 6. Identify outliers in credit limit using IQR method.
SELECT
  cust_id,
  cust_credit_limit
FROM (
  SELECT
    cust_id,
    cust_credit_limit,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY cust_credit_limit)
      OVER (PARTITION BY cust_state_province) AS q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY cust_credit_limit)
      OVER (PARTITION BY cust_state_province) AS q3
  FROM sh.customers
) t
WHERE cust_credit_limit > (q3 + 1.5*(q3 - q1))
   OR cust_credit_limit < (q1 - 1.5*(q3 - q1));

-- 7. Calculate credit limit growth per customer over years (if historical data exists).
SELECT
  cust_id,
  year,
  credit_limit,
  credit_limit - LAG(credit_limit) OVER (PARTITION BY cust_id ORDER BY year) AS growth
FROM customer_credit_history;

-- 8. Create a running average of credit limit by customer ID.
SELECT
  cust_id,
  cust_credit_limit,
  AVG(cust_credit_limit) OVER (
    PARTITION BY cust_id ORDER BY cust_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_avg_credit
FROM sh.customers;

-- 9. Compute total cumulative credit per income group sorted by rank.
SELECT
  income_group,
  SUM(cust_credit_limit) AS total_credit,
  SUM(SUM(cust_credit_limit)) OVER (
    ORDER BY SUM(cust_credit_limit) DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS cumulative_credit
FROM (
  SELECT
    SUBSTR(cust_income_level,1,1) AS income_group,
    cust_credit_limit
  FROM sh.customers
) t
GROUP BY income_group
ORDER BY total_credit DESC;

-- 10. Generate a leaderboard view showing top N customers dynamically using analytic functions.
SELECT
  cust_id,
  cust_first_name,
  cust_last_name,
  total_sales,
  ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS rank_overall
FROM (
  SELECT
    cu.cust_id,
    cu.cust_first_name,
    cu.cust_last_name,
    NVL(SUM(s.amount_sold),0) AS total_sales
  FROM sh.customers cu
  LEFT JOIN sh.sales s ON cu.cust_id = s.cust_id
  GROUP BY cu.cust_id, cu.cust_first_name, cu.cust_last_name
) t
WHERE rank_overall <= :N;
-- Bonus: Scenario-Based SQL on SH.CUSTOMERS

-- 1. Display the top 5 customers with the highest credit limit.
SELECT cust_id, 
       cust_first_name, 
       cust_last_name, 
       cust_credit_limit
FROM (
  SELECT cust_id,
         cust_first_name,
         cust_last_name,
         cust_credit_limit,
         RANK() OVER (ORDER BY cust_credit_limit DESC) AS rnk
  FROM sh.customers
)
WHERE rnk <= 5;

-- 2. Find customers having the same income level as the customer with the maximum credit limit.
WITH max_cust AS (
  SELECT cust_income_level
  FROM sh.customers
  ORDER BY cust_credit_limit DESC
  FETCH FIRST 1 ROWS ONLY
)
SELECT cust_id, 
       cust_first_name, 
       cust_last_name, 
       cust_income_level, 
       cust_credit_limit
FROM sh.customers
WHERE cust_income_level = (SELECT cust_income_level FROM max_cust);

-- 3. Display customers who have a credit limit higher than the average credit limit of all customers.
SELECT cust_id, cust_credit_limit
FROM sh.customers
WHERE cust_credit_limit > (SELECT AVG(cust_credit_limit) FROM sh.customers);

-- 4. Rank all customers based on their credit limit in descending order and display rank along with name.
SELECT
  cust_id,
  cust_first_name || ' ' || cust_last_name AS name,
  cust_credit_limit,
  RANK() OVER (ORDER BY cust_credit_limit DESC) AS credit_rank
FROM sh.customers
ORDER BY credit_rank;

-- 5. Find customers who belong to the top 3 credit limit ranks in each income level.
SELECT cust_id, cust_income_level, cust_credit_limit
FROM (
  SELECT
    cust_id,
    cust_income_level,
    cust_credit_limit,
    RANK() OVER (PARTITION BY cust_income_level ORDER BY cust_credit_limit DESC) AS rk
  FROM sh.customers
)
WHERE rk <= 3
ORDER BY cust_income_level, rk;

-- 6. Categorize customers into “Platinum”, “Gold”, and “Standard” tiers based on their credit limit ranges.
SELECT
  cust_id,
  cust_credit_limit,
  CASE
    WHEN cust_credit_limit >= 100000 THEN 'Platinum'
    WHEN cust_credit_limit >= 50000  THEN 'Gold'
    ELSE 'Standard'
  END AS tier
FROM sh.customers;

-- 7. Display each customer’s credit limit along with the previous and next customer’s limit (using LAG and LEAD).
SELECT
  cust_id,
  cust_credit_limit,
  LAG(cust_credit_limit) OVER (ORDER BY cust_credit_limit DESC) AS prev_limit,
  LEAD(cust_credit_limit) OVER (ORDER BY cust_credit_limit DESC) AS next_limit
FROM sh.customers
ORDER BY cust_credit_limit DESC;

-- 8. Find customers whose credit limit difference from the previous customer is more than 10,000.
SELECT 
    cust_id,
    cust_credit_limit,
    prev_limit,
    ABS(cust_credit_limit - prev_limit) AS diff
FROM (
    SELECT 
        cust_id,
        cust_credit_limit,
        LAG(cust_credit_limit) OVER (ORDER BY cust_credit_limit DESC) AS prev_limit
    FROM sh.customers
) t
WHERE prev_limit IS NOT NULL
  AND ABS(cust_credit_limit - prev_limit) > 10000
ORDER BY diff DESC;

-- 9. Display the highest, lowest, and average credit limit per income level.
SELECT
  cust_income_level,
  MAX(cust_credit_limit) AS max_credit,
  MIN(cust_credit_limit) AS min_credit,
  ROUND(AVG(cust_credit_limit),2) AS avg_credit
FROM sh.customers
GROUP BY cust_income_level
ORDER BY cust_income_level;

-- 10. Find the youngest and oldest customers (based on CUST_YEAR_OF_BIRTH).
--vYoungest (largest year):
SELECT cust_id, cust_first_name, cust_last_name, cust_year_of_birth
FROM sh.customers
ORDER BY cust_year_of_birth DESC
FETCH FIRST 1 ROW ONLY;

-- Oldest (smallest year):
SELECT cust_id, cust_first_name, cust_last_name, cust_year_of_birth
FROM sh.customers
ORDER BY cust_year_of_birth ASC
FETCH FIRST 1 ROW ONLY;
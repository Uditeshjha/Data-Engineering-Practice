-- Aggregation & Grouping

-- 1. Find the total, average, minimum, and maximum credit limit of all customers.
SELECT 
  SUM(cust_credit_limit)   AS total_credit,
  AVG(cust_credit_limit)   AS avg_credit,
  MIN(cust_credit_limit)   AS min_credit,
  MAX(cust_credit_limit)   AS max_credit
FROM sh.customers;

-- 2. Count the number of customers in each income level.
SELECT 
  cust_income_level,
  COUNT(*) AS customers_count
FROM sh.customers
GROUP BY cust_income_level
ORDER BY customers_count DESC;

-- 3. Show total credit limit by state and country.
SELECT 
  c.cust_state_province,
  co.country_name,
  SUM(c.cust_credit_limit) AS total_credit
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
GROUP BY c.cust_state_province, co.country_name
ORDER BY co.country_name, total_credit DESC;

-- 4. Display average credit limit for each marital status and gender combination.
SELECT 
  cust_marital_status,
  cust_gender,
  AVG(cust_credit_limit) AS avg_credit
FROM sh.customers
GROUP BY cust_marital_status, cust_gender
ORDER BY cust_marital_status, cust_gender;

-- 5. Find the top 3 states with the highest average credit limit.
SELECT 
  cust_state_province,
  AVG(cust_credit_limit) AS avg_credit
FROM sh.customers
GROUP BY cust_state_province
ORDER BY AVG(cust_credit_limit) DESC
FETCH FIRST 3 ROWS ONLY;

-- window func
SELECT cust_state_province, avg_credit
FROM (
  SELECT 
    cust_state_province,
    AVG(cust_credit_limit) AS avg_credit,
    DENSE_RANK() OVER (ORDER BY AVG(cust_credit_limit) DESC) AS rank_no
  FROM sh.customers
  GROUP BY cust_state_province
)
WHERE rank_no <= 3;

-- window fun with partition by
SELECT *
FROM (
  SELECT 
    cust_state_province,
    cust_first_name,
    cust_last_name,
    cust_credit_limit,
    DENSE_RANK() OVER (
      PARTITION BY cust_state_province 
      ORDER BY cust_credit_limit DESC
    ) AS rank_no
  FROM sh.customers
)
WHERE rank_no <= 3;


-- 6. Find the country with the maximum total customer credit limit.
SELECT
  co.country_name,
  SUM(c.cust_credit_limit) AS total_credit
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
GROUP BY co.country_name
ORDER BY total_credit DESC
FETCH FIRST 1 ROWS ONLY;

-- 7. Show the number of customers whose credit limit exceeds their state average.
SELECT COUNT(*) AS num_customers_above_state_avg
FROM (
  SELECT 
    cust_id,
    cust_credit_limit,
    AVG(cust_credit_limit) OVER (PARTITION BY cust_state_province) AS state_avg
  FROM sh.customers
) t
WHERE t.cust_credit_limit > t.state_avg;

-- 8. Calculate total and average credit limit for customers born after 1980.
SELECT 
  SUM(cust_credit_limit) AS total_credit_after_1980,
  AVG(cust_credit_limit) AS avg_credit_after_1980
FROM sh.customers
WHERE cust_year_of_birth > 1980;

-- 9. Find states having more than 50 customers.
SELECT 
  cust_state_province,
  COUNT(*) AS num_customers
FROM sh.customers
GROUP BY cust_state_province
HAVING COUNT(*) > 50
ORDER BY num_customers DESC;

-- 10. List countries where the average credit limit is higher than the global average.
SELECT
  co.country_name,
  AVG(c.cust_credit_limit) AS country_avg_credit
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
GROUP BY co.country_name
HAVING AVG(c.cust_credit_limit) > (SELECT AVG(cust_credit_limit) FROM sh.customers);

-- 11. Calculate the variance and standard deviation of customer credit limits by country.
SELECT
  co.country_name,
  VAR_POP(c.cust_credit_limit)   AS population_variance,
  STDDEV_POP(c.cust_credit_limit) AS population_stddev
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
GROUP BY co.country_name
ORDER BY co.country_name;

-- 12. Find the state with the smallest range (max–min) in credit limits.
SELECT cust_state_province, credit_range
FROM (
  SELECT 
    cust_state_province,
    MAX(cust_credit_limit) - MIN(cust_credit_limit) AS credit_range
  FROM sh.customers
  GROUP BY cust_state_province
  ORDER BY credit_range ASC
)
WHERE ROWNUM = 1;

-- 13. Show the total number of customers per income level and the percentage contribution of each.
WITH total AS (
  SELECT COUNT(*) AS total_customers FROM sh.customers
)
SELECT
  c.cust_income_level,
  COUNT(*) AS num_customers,
  ROUND(COUNT(*) * 100 / t.total_customers, 2) AS pct_of_total
FROM sh.customers c, total t
GROUP BY c.cust_income_level, t.total_customers
ORDER BY num_customers DESC;
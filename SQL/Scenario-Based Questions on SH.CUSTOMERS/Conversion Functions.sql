-- Date & Conversion Functions

-- 1. Convert CUST_YEAR_OF_BIRTH to age as of today.
SELECT
  cust_id,
  (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) AS age
FROM sh.customers;

-- 2. Display all customers born between 1980 and 1990.
SELECT cust_id, cust_year_of_birth
FROM sh.customers
WHERE cust_year_of_birth BETWEEN 1980 AND 1990;

-- 3. Format date of birth into “Month YYYY” using TO_CHAR.
SELECT
  cust_id,
  TO_CHAR(TO_DATE(TO_CHAR(cust_year_of_birth),'YYYY'),'Month YYYY') AS birth_month_year
FROM sh.customers;

-- 4. Convert income level text (like 'A: Below 30,000') to numeric lower limit.
-- select cust_income_level,SUBSTR(cust_income_level, 4, 6) as t 
-- from sh.customers;
SELECT
  cust_id,
  CASE
    WHEN cust_income_level LIKE '%Below%' THEN 0
    ELSE TO_NUMBER(REPLACE(SUBSTR(cust_income_level, 4, 6), ',', ''))
  END AS income_lower_limit
FROM sh.customers;

-- 5. Display customer birth decades (e.g., 1960s, 1970s).
SELECT
  cust_id,cust_year_of_birth,
  TRUNC(cust_year_of_birth, -1) || 's' AS birth_decade
FROM sh.customers;

-- 6. Show customers grouped by age bracket (10-year intervals).
-- Find the age
-- Divides the age by 10 to find its decade group
-- Removes the decimal (keeps only the full decade)
-- Converts the group back to a number like 30
SELECT
  FLOOR((EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth)/10)*10 || 's' AS age_group,
  COUNT(*) AS total_customers
FROM sh.customers
GROUP BY FLOOR((EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth)/10)*10
ORDER BY age_group;

-- 7. Convert country_id to uppercase and state name to lowercase.
SELECT
  c.cust_id,
  UPPER(co.country_name)      AS country_upper,
  LOWER(c.cust_state_province) AS state_lower
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id;

-- 8. Show customers where credit limit > average of their birth decade.
SELECT cust_id,
       cust_credit_limit,
       birth_decade
FROM (
    SELECT cust_id,
           cust_credit_limit,
           TRUNC(cust_year_of_birth, -1) AS birth_decade,
           AVG(cust_credit_limit) OVER (PARTITION BY TRUNC(cust_year_of_birth, -1)) AS decade_avg
    FROM sh.customers
) 
WHERE cust_credit_limit > decade_avg;

-- 9. Convert all numeric credit limits to currency format $999,999.00.
SELECT
  cust_id,
  TO_CHAR(cust_credit_limit, '$999,999,999.00') AS credit_formatted
FROM sh.customers;

-- 10. Find customers whose credit limit was NULL and replace with average (using NVL).
SELECT
  cust_id,
  NVL(cust_credit_limit, (SELECT AVG(cust_credit_limit) FROM sh.customers)) AS credit_filled
FROM sh.customers;
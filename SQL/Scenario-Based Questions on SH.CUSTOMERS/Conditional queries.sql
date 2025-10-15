-- Conditional, CASE, and DECODE

-- 1. Categorize customers into income tiers: Platinum, Gold, Silver, Bronze.
SELECT 
  cust_id,
  cust_credit_limit,
  CASE
    WHEN cust_credit_limit >= 100000 THEN 'Platinum'
    WHEN cust_credit_limit >= 50000  THEN 'Gold'
    WHEN cust_credit_limit >= 20000  THEN 'Silver'
    ELSE 'Bronze'
  END AS income_tier
FROM sh.customers;

-- 2. Display “High”, “Medium”, or “Low” income categories based on credit limit.
SELECT 
  cust_id,
  cust_credit_limit,
  CASE
    WHEN cust_credit_limit > 80000 THEN 'High'
    WHEN cust_credit_limit BETWEEN 40000 AND 80000 THEN 'Medium'
    ELSE 'Low'
  END AS income_category
FROM sh.customers;

-- 3. Replace NULL income levels with “Unknown” using NVL.
SELECT 
  cust_id,
  NVL(cust_income_level, 'Unknown') AS income_level
FROM sh.customers;

-- 4. Show customer details and mark whether they have above-average credit limit or not.
SELECT 
  cust_id,
  cust_credit_limit,
  CASE 
    WHEN cust_credit_limit > (SELECT AVG(cust_credit_limit) FROM sh.customers)
      THEN 'Above Average'
    ELSE 'Below Average'
  END AS credit_category
FROM sh.customers;

-- 5. Use DECODE to convert marital status codes (S/M/D) into full text.
-- already in full text!
SELECT 
  cust_id,
  cust_marital_status,
  DECODE(cust_marital_status, 
         'S', 'Single', 
         'M', 'Married', 
         'D', 'Divorced', 
         'Unknown') AS marital_status_full
FROM sh.customers;

-- 6. Use CASE to show age group (≤30, 31–50, >50) from CUST_YEAR_OF_BIRTH.
SELECT 
  cust_id,
  cust_year_of_birth,
  CASE
    WHEN (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) <= 30 THEN '≤30'
    WHEN (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) <= 50 THEN '31–50'
    ELSE '>50'
  END AS age_group
FROM sh.customers;

-- 7. Label customers as “Old Credit Holder” or “New Credit Holder” based on year of birth < 1980.
SELECT 
  cust_id,
  cust_year_of_birth,
  CASE
    WHEN cust_year_of_birth < 1960 THEN 'Old Credit Holder'
    ELSE 'New Credit Holder'
  END AS holder_type
FROM sh.customers;

-- 8. Create a loyalty tag — “Premium” if credit limit > 50,000 and income_level = ‘E’.
SELECT 
  cust_id,
  cust_credit_limit,
  cust_income_level,
  CASE 
    WHEN cust_credit_limit > 50000 AND cust_income_level = 'E' THEN 'Premium'
    ELSE 'Regular'
  END AS loyalty_tag
FROM sh.customers;

-- 9. Assign grades (A–F) based on credit limit range using CASE.
SELECT 
  cust_id,
  cust_credit_limit,
  CASE
    WHEN cust_credit_limit >= 100000 THEN 'A'
    WHEN cust_credit_limit >= 80000 THEN 'B'
    WHEN cust_credit_limit >= 60000 THEN 'C'
    WHEN cust_credit_limit >= 40000 THEN 'D'
    WHEN cust_credit_limit >= 20000 THEN 'E'
    ELSE 'F'
  END AS grade
FROM sh.customers;

-- 10. Show country, state, and number of premium customers using conditional aggregation.
SELECT 
  co.country_name,
  c.cust_state_province,
  COUNT(CASE WHEN c.cust_credit_limit > 10000 THEN 1 END) AS premium_customers
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
GROUP BY co.country_name, c.cust_state_province

ORDER BY co.country_name, c.cust_state_province;

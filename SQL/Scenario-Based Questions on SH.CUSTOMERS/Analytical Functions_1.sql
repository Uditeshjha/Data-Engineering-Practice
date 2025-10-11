-- B. Analytical / Window Functions

-- 1. Assign row numbers to customers ordered by credit limit descending.
select cust_id,cust_credit_limit, 
ROW_NUMBER() over(order by cust_credit_limit desc) as r_num 
from sh.CUSTOMERS;

-- 2. Rank customers within each state by credit limit.
select cust_state_province,cust_id,cust_credit_limit,
rank() over(partition by cust_state_province order by cust_credit_limit) as rnk
from sh.customers
order by cust_state_province,rnk;


-- 3. Use DENSE_RANK() to find the top 5 credit holders per country.
select * from
(select co.country_name,c.cust_credit_limit,
dense_rank() over(partition by co.country_name order by c.cust_credit_limit) as rnk
from sh.customers c
join sh.countries co on c.country_id = co.country_id) 
WHERE rnk <= 5
ORDER BY country_name, rnk;

-- 4. Divide customers into 4 quartiles based on their credit limit using NTILE(4).
SELECT 
  cust_id,
  cust_first_name,
  cust_last_name,
  cust_credit_limit,
  NTILE(4) OVER (ORDER BY cust_credit_limit) AS quartile
FROM sh.customers
ORDER BY quartile, cust_credit_limit;

-- 5. Calculate a running total of credit limits ordered by customer_id.
SELECT 
  cust_id,
  cust_state_province,
  cust_credit_limit,
  SUM(cust_credit_limit) 
    OVER (PARTITION BY cust_state_province ORDER BY cust_id) AS running_total_by_state
FROM sh.customers
ORDER BY cust_state_province, cust_id;

-- 6. Show cumulative average credit limit by country.
SELECT
  co.country_name,
  c.cust_id,
  c.cust_credit_limit,
  AVG(c.cust_credit_limit)
      OVER (
        PARTITION BY co.country_name
        ORDER BY c.cust_id
      )
  AS cumulative_avg
FROM sh.customers c
JOIN sh.countries co 
  ON c.country_id = co.country_id
ORDER BY co.country_name, c.cust_id;

-- 7. Compare each customer’s credit limit to the previous one using LAG().
SELECT
  cust_id,
  cust_first_name,
  cust_last_name,
  cust_credit_limit,
  LAG(cust_credit_limit) 
    OVER (ORDER BY cust_id) AS prev_credit_limit,
  cust_credit_limit - LAG(cust_credit_limit) 
    OVER (ORDER BY cust_id) AS diff_from_prev
FROM sh.customers
ORDER BY cust_id;

-- 8. Show next customer’s credit limit using LEAD().
SELECT
  cust_id,
  cust_credit_limit,
  LEAD(cust_credit_limit) OVER (ORDER BY cust_id) AS next_credit_limit,
  LEAD(cust_credit_limit) OVER (ORDER BY cust_id) - cust_credit_limit AS diff_with_next
FROM sh.customers
ORDER BY cust_id;

-- 9. Display the difference between each customer’s credit limit and the previous one.
SELECT
  cust_id,
  cust_credit_limit,
  cust_credit_limit - LAG(cust_credit_limit) 
    OVER (ORDER BY cust_id) AS diff_from_prev
FROM sh.customers
ORDER BY cust_id;

-- 10. For each country, display the first and last credit limit using FIRST_VALUE() and LAST_VALUE().
SELECT
  co.country_name,
  c.cust_id,
  c.cust_credit_limit,
  FIRST_VALUE(c.cust_credit_limit) 
    OVER (PARTITION BY co.country_name ORDER BY c.cust_credit_limit) AS first_credit_limit,
  LAST_VALUE(c.cust_credit_limit) 
    OVER (
      PARTITION BY co.country_name 
      ORDER BY c.cust_credit_limit 
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_credit_limit
FROM sh.customers c
JOIN sh.countries co 
  ON c.country_id = co.country_id
ORDER BY co.country_name, c.cust_credit_limit;

-- 11. Compute percentage rank (PERCENT_RANK()) of customers based on credit limit.
SELECT
    cust_id,
    cust_credit_limit,
    PERCENT_RANK() OVER (ORDER BY cust_credit_limit) AS percent_rank
FROM sh.customers
ORDER BY percent_rank;

-- 12. Show each customer’s position in percentile (CUME_DIST() function).
SELECT
    cust_id,
    cust_credit_limit,
    CUME_DIST() OVER (ORDER BY cust_credit_limit) AS percentile_position
FROM sh.customers
ORDER BY percentile_position;

-- 13. Display the difference between the maximum and current credit limit for each customer.
SELECT
    cust_id,
    cust_credit_limit,
    MAX(cust_credit_limit) OVER () AS max_credit_limit,
    MAX(cust_credit_limit) OVER () - cust_credit_limit AS credit_diff_from_max
FROM sh.customers
ORDER BY credit_diff_from_max DESC;

-- 14. Rank income levels by their average credit limit.
SELECT
    cust_income_level,
    ROUND(AVG(cust_credit_limit), 2) AS avg_credit_limit,
    RANK() OVER (ORDER BY AVG(cust_credit_limit) DESC) AS rank_by_avg_credit
FROM sh.customers
GROUP BY cust_income_level
ORDER BY rank_by_avg_credit;

-- 15. Calculate the average credit limit over the last 10 customers (sliding window).
SELECT
    cust_id,
    cust_credit_limit,
    ROUND(
        AVG(cust_credit_limit)
        OVER (
            ORDER BY cust_id
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ), 2
    ) AS avg_last_10_customers
FROM sh.customers
ORDER BY cust_id;
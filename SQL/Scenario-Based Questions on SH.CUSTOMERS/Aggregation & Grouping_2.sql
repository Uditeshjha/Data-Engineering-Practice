-- 14. For each income level, find how many customers have NULL credit limits.
SELECT cust_income_level,COUNT(
    CASE WHEN cust_credit_limit is NULL
    THEN 1
    END
) AS customers_null_credit_limit
FROM SH.CUSTOMERS
GROUP BY cust_income_level;

-- 15. Display countries where the sum of credit limits exceeds 10 million.
select co.COUNTRY_NAME,c.CUST_CREDIT_LIMIT, SUM(CUST_CREDIT_LIMIT) 
from SH.CUSTOMERS c
JOIN SH.COUNTRIES co ON c.COUNTRY_ID = co.COUNTRY_ID
GROUP BY co.COUNTRY_NAME,c.CUST_CREDIT_LIMIT
HAVING SUM(CUST_CREDIT_LIMIT) > 10000000;

-- 16. Find the state that contributes the highest total credit limit to its country.
with state_with_total_credit AS(
select co.COUNTRY_NAME,c.cust_state_province,SUM(cust_credit_limit) AS total_credit
from sh.CUSTOMERS c
join sh.COUNTRIES co on c.COUNTRY_ID = co.COUNTRY_ID
group by co.COUNTRY_NAME,c.cust_state_province
order by co.COUNTRY_NAME, total_credit DESC
)
select country_name,cust_state_province,total_credit
FROM (
    select COUNTRY_NAME, cust_state_province, total_credit,
    rank() over(partition by country_name order by total_credit desc) as rnk
    from state_with_total_credit
) where rnk = 1;

-- 17. Show total credit limit per year of birth, sorted by total descending.
select cust_year_of_birth, SUM(cust_credit_limit) as total_credit
from sh.CUSTOMERS
group by cust_year_of_birth
order by total_credit desc;

-- 18. Identify customers who hold the maximum credit limit in their respective country.
with customer_total_credit as(
select co.country_name,c.cust_id,SUM(c.cust_credit_limit) as total_credit
from sh.customers c 
join sh.countries co on c.country_id = co.country_id
group by co.country_name,c.cust_id
order by co.country_name,total_credit desc
)

select t.country_name, t.cust_id, t.total_credit
from customer_total_credit t
where t.total_credit =(
    select max(t2.total_credit)
    from customer_total_credit t2
    where t2.country_name = t.country_name
)
ORDER BY t.country_name;

-- 19. Show the difference between maximum and average credit limit per country.
select co.COUNTRY_NAME,MAX(c.cust_credit_limit) - AVG(c.cust_credit_limit) AS diffn
from sh.CUSTOMERS c
join sh.COUNTRIES co on c.COUNTRY_ID = co.COUNTRY_ID
group by co.COUNTRY_NAME
order by co.COUNTRY_NAME

-- 20. Display the overall rank of each state based on its total credit limit 
-- (using GROUP BY + analytic rank).

SELECT
  cust_state_province,
  total_credit,
  RANK() OVER (ORDER BY total_credit DESC) AS overall_rank
FROM (
  SELECT cust_state_province, SUM(cust_credit_limit) AS total_credit
  FROM sh.customers
  GROUP BY cust_state_province
) t
ORDER BY overall_rank;
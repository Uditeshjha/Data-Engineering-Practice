-- 16. For each state, calculate the cumulative total of credit limits ordered by city.
SELECT
    cust_state_province,
    cust_city,
    SUM(city_total) OVER (
        PARTITION BY cust_state_province
        ORDER BY cust_city
    ) AS cumulative_credit_limit
FROM (
    SELECT
        cust_state_province,
        cust_city,
        SUM(cust_credit_limit) AS city_total
    FROM sh.customers
    GROUP BY cust_state_province, cust_city
)
ORDER BY cust_state_province, cust_city;

-- 17. Find customers whose credit limit equals the median credit limit (use PERCENTILE_CONT(0.5)).
SELECT cust_id, cust_first_name, cust_last_name, cust_credit_limit
FROM sh.customers
WHERE cust_credit_limit = (
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cust_credit_limit)
    FROM sh.customers
);

-- 18. Display the highest 3 credit holders per state using ROW_NUMBER() and PARTITION BY.
SELECT *
FROM (
    SELECT
        cust_state_province,
        cust_id,
        cust_credit_limit,
        ROW_NUMBER() OVER (
            PARTITION BY cust_state_province
            ORDER BY cust_credit_limit DESC
        ) AS rn
    FROM sh.customers
    WHERE cust_credit_limit IS NOT NULL
)
WHERE rn <= 3
ORDER BY cust_state_province, rn;

-- 19. Identify customers whose credit limit increased compared to previous row (using LAG).
SELECT *
FROM (
    SELECT
        cust_id,
        cust_credit_limit,
        LAG(cust_credit_limit) OVER (ORDER BY cust_id) AS prev_credit_limit
    FROM sh.customers
)
WHERE cust_credit_limit > prev_credit_limit
ORDER BY cust_id;

-- 20. Calculate moving average of credit limits with a window of 3.
SELECT
    cust_id,
    cust_credit_limit,
    ROUND(
        AVG(cust_credit_limit) OVER (
            ORDER BY cust_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS moving_avg_3
FROM sh.customers
ORDER BY cust_id;

-- 21. Show cumulative percentage of total credit limit per country.
SELECT
    co.country_name,
    c.cust_credit_limit,
    ROUND(
        SUM(c.cust_credit_limit) OVER (
            PARTITION BY co.country_name
            ORDER BY c.cust_credit_limit
        )
        / SUM(c.cust_credit_limit) OVER (PARTITION BY co.country_name) * 100,
        2
    ) AS cumulative_pct
FROM sh.customers c
JOIN sh.countries co ON c.country_id = co.country_id
WHERE c.cust_credit_limit IS NOT NULL
ORDER BY co.country_name, c.cust_credit_limit;

-- 22. Rank customers by age (derived from CUST_YEAR_OF_BIRTH).
SELECT
    cust_id,
    cust_first_name,
    cust_last_name,
    (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) AS age,
    RANK() OVER (ORDER BY (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) DESC) AS age_rank
FROM sh.customers
WHERE cust_year_of_birth IS NOT NULL
ORDER BY age_rank;

-- 23. Calculate difference in age between current and previous customer in the same state.
SELECT
    cust_state_province,
    cust_id,
    (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth) AS age,
    LAG(EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth)
        OVER (PARTITION BY cust_state_province ORDER BY cust_id) AS prev_age,
    (EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth)
      - LAG(EXTRACT(YEAR FROM SYSDATE) - cust_year_of_birth)
        OVER (PARTITION BY cust_state_province ORDER BY cust_id) AS age_difference
FROM sh.customers
WHERE cust_year_of_birth IS NOT NULL
ORDER BY cust_state_province, cust_id;

-- 24. Use RANK() and DENSE_RANK() to show how ties are treated differently.
SELECT
    cust_state_province,
    cust_id,
    cust_credit_limit,
    RANK() OVER (PARTITION BY cust_state_province ORDER BY cust_credit_limit DESC) AS rank_,
    DENSE_RANK() OVER (PARTITION BY cust_state_province ORDER BY cust_credit_limit DESC) AS dense_rank_
FROM sh.customers
WHERE cust_credit_limit IS NOT NULL
ORDER BY cust_state_province, cust_credit_limit DESC;

-- 25. Compare each state’s average credit limit with country average using window partition.
SELECT
    country_id,
    cust_state_province,
    ROUND(AVG(cust_credit_limit), 2) AS state_avg,
    ROUND(
        AVG(AVG(cust_credit_limit)) OVER (PARTITION BY country_id),
        2
    ) AS country_avg,
    ROUND(
        AVG(cust_credit_limit) - 
        AVG(AVG(cust_credit_limit)) OVER (PARTITION BY country_id),
        2
    ) AS diff_from_country_avg
FROM sh.customers
WHERE cust_credit_limit IS NOT NULL
GROUP BY country_id, cust_state_province
ORDER BY country_id, diff_from_country_avg DESC;

-- 26. Show total credit per state and also its rank within each country.
SELECT
    country_id,
    cust_state_province,
    SUM(cust_credit_limit) AS total_credit,
    RANK() OVER (
        PARTITION BY country_id
        ORDER BY SUM(cust_credit_limit) DESC
    ) AS state_rank
FROM sh.customers
WHERE cust_credit_limit IS NOT NULL
GROUP BY country_id, cust_state_province
ORDER BY country_id, state_rank;

-- 27. Find customers whose credit limit is above the 90th percentile of their income level.
SELECT
    cust_id,
    cust_income_level,
    cust_credit_limit
FROM (
    SELECT
        cust_id,
        cust_income_level,
        cust_credit_limit,
        PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY cust_credit_limit)
            OVER (PARTITION BY cust_income_level) AS p90
    FROM sh.customers
    WHERE cust_credit_limit IS NOT NULL
)
WHERE cust_credit_limit > p90
ORDER BY cust_income_level, cust_credit_limit DESC;

-- 28. Display top 3 and bottom 3 customers per country by credit limit.
SELECT *
FROM (
    SELECT
        country_id,
        cust_id,
        cust_credit_limit,
        ROW_NUMBER() OVER (
            PARTITION BY country_id
            ORDER BY cust_credit_limit DESC
        ) AS rank_desc,
        ROW_NUMBER() OVER (
            PARTITION BY country_id
            ORDER BY cust_credit_limit ASC
        ) AS rank_asc
    FROM sh.customers
    WHERE cust_credit_limit IS NOT NULL
)
WHERE rank_desc <= 3 OR rank_asc <= 3
ORDER BY country_id, cust_credit_limit DESC;

-- 29. Calculate rolling sum of 5 customers’ credit limit within each country.
SELECT
    country_id,
    cust_id,
    cust_credit_limit,
    SUM(cust_credit_limit) OVER (
        PARTITION BY country_id
        ORDER BY cust_id
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS rolling_sum_5
FROM sh.customers
WHERE cust_credit_limit IS NOT NULL
ORDER BY country_id, cust_id;

-- 30. For each marital status, display the most and least wealthy customers using analytical functions.
SELECT *
FROM (
    SELECT
        cust_id,
        cust_marital_status,
        cust_credit_limit,
        FIRST_VALUE(cust_id) OVER (
            PARTITION BY cust_marital_status
            ORDER BY cust_credit_limit DESC
        ) AS richest_customer,
        FIRST_VALUE(cust_id) OVER (
            PARTITION BY cust_marital_status
            ORDER BY cust_credit_limit ASC
        ) AS poorest_customer
    FROM sh.customers
    WHERE cust_credit_limit IS NOT NULL
)
ORDER BY cust_marital_status;
-- Identify Top 3 Item Types by Retail Sales for Each Year
-- This query utilizes Common Table Expressions (CTEs) and Window Functions (DENSE_RANK) 
-- to partition the data by year and rank the most popular item types.

WITH ranked_item_sales AS (
    SELECT 
        f.year,
        i.item_type,
        SUM(f.retail_sales) AS total_retail_sales,
        DENSE_RANK() OVER (
            PARTITION BY f.year 
            ORDER BY SUM(f.retail_sales) DESC
        ) AS sales_rank
    FROM fact_sales_performance f
    JOIN dim_item i ON f.item_id = i.item_id
    GROUP BY f.year, i.item_type
)
SELECT 
    year,
    item_type,
    total_retail_sales,
    sales_rank
FROM ranked_item_sales
WHERE sales_rank <= 3
ORDER BY year DESC, sales_rank ASC;
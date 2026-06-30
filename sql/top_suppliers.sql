-- Identify the Top 5 Suppliers by Total Sales Volume
-- This query aggregates both retail and warehouse sales to find the biggest revenue drivers.

SELECT 
    s.supplier_name,
    SUM(f.retail_sales + f.warehouse_sales) AS total_sales_volume,
    SUM(f.retail_sales) AS total_retail_sales,
    SUM(f.warehouse_sales) AS total_warehouse_sales
FROM fact_sales_performance f
JOIN dim_supplier s ON f.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY total_sales_volume DESC
LIMIT 5;
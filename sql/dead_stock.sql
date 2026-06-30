-- ============================================================================
-- INITIAL: DETECT ABSOLUTE DEAD STOCK ITEMS
-- Hypothesis: High transfers (>5000) but exactly zero sales.
-- Result: No data returned (indicates very healthy stock rotation).
-- ============================================================================

SELECT 
    i.item_description,
    i.item_type,
    SUM(f.retail_transfers) AS total_transfers,
    SUM(f.retail_sales) AS total_retail_sales,
    (SUM(f.retail_transfers) - SUM(f.retail_sales)) AS remaining_unsold_stock
FROM fact_sales_performance f
JOIN dim_item i ON f.item_id = i.item_id
GROUP BY i.item_description, i.item_type
HAVING SUM(f.retail_transfers) > 5000 AND SUM(f.retail_sales) = 0
ORDER BY total_transfers DESC;


-- ============================================================================
-- ADJUSTED: DETECT HIGH-RISK LOW-TURNOVER ITEMS
-- Iteration: Lowering threshold (>1000 transfers) and allowing minimal sales (<50).
-- Objective: Capture slow-moving items gridlocked in retail stores.
-- ============================================================================

SELECT 
    i.item_description,
    i.item_type,
    SUM(f.retail_transfers) AS total_transfers,
    SUM(f.retail_sales) AS total_retail_sales,
    (SUM(f.retail_transfers) - SUM(f.retail_sales)) AS remaining_unsold_stock
FROM fact_sales_performance f
JOIN dim_item i ON f.item_id = i.item_id
GROUP BY i.item_description, i.item_type
HAVING SUM(f.retail_transfers) > 1000 AND SUM(f.retail_sales) < 50
ORDER BY total_transfers DESC
LIMIT 10;
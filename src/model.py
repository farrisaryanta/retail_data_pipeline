import os
import logging
from sqlalchemy import text
from config.database import get_db_engine

# Ensure logging configuration aligns with the main pipeline standard
LOG_DIR = "logs"
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def build_star_schema():
    """
    Automates the creation and population of the Star Schema (Dimension & Fact tables)
    directly inside the PostgreSQL database.
    """
    logging.info("Data Modeling phase initiated: Building Star Schema.")
    print("[4/4] Initiating Data Modeling (Star Schema)...")

    engine = get_db_engine()
    if engine is None:
        logging.error("Data Modeling failed: Database connection engine is not available.")
        return False

    # Collection of DDL & DML queries executed within a single database transaction block
    queries = {
        "Create dim_supplier": """
            CREATE TABLE IF NOT EXISTS dim_supplier (
                supplier_id SERIAL PRIMARY KEY,
                supplier_name VARCHAR(255) NOT NULL UNIQUE
            );
        """,
        "Create dim_item": """
            CREATE TABLE IF NOT EXISTS dim_item (
                item_id SERIAL PRIMARY KEY,
                item_code VARCHAR(50) NOT NULL UNIQUE,
                item_description TEXT,
                item_type VARCHAR(100)
            );
        """,
        "Create fact_sales_performance": """
            CREATE TABLE IF NOT EXISTS fact_sales_performance (
                sales_id SERIAL PRIMARY KEY,
                year INT NOT NULL,
                month INT NOT NULL,
                supplier_id INT REFERENCES dim_supplier(supplier_id),
                item_id INT REFERENCES dim_item(item_id),
                retail_sales NUMERIC(12, 2),
                retail_transfers NUMERIC(12, 2),
                warehouse_sales NUMERIC(12, 2)
            );
        """,
        "Populate dim_supplier": """
            INSERT INTO dim_supplier (supplier_name)
            SELECT DISTINCT supplier
            FROM fact_warehouse_retail_sales
            WHERE supplier IS NOT NULL
            ON CONFLICT (supplier_name) DO NOTHING;
        """,
        "Populate dim_item": """
            INSERT INTO dim_item (item_code, item_description, item_type)
            SELECT DISTINCT item_code, item_description, item_type
            FROM fact_warehouse_retail_sales
            WHERE item_code IS NOT NULL
            ON CONFLICT (item_code) DO NOTHING;
        """,
        "Clear existing fact data": """
            TRUNCATE TABLE fact_sales_performance RESTART IDENTITY CASCADE;
        """,
        "Populate fact_sales_performance": """
            INSERT INTO fact_sales_performance (
                year, month, supplier_id, item_id, 
                retail_sales, retail_transfers, warehouse_sales
            )
            SELECT 
                f.year,
                f.month,
                s.supplier_id,
                i.item_id,
                f.retail_sales,
                f.retail_transfers,
                f.warehouse_sales
            FROM fact_warehouse_retail_sales f
            LEFT JOIN dim_supplier s ON f.supplier = s.supplier_name
            LEFT JOIN dim_item i ON f.item_code = i.item_code;
        """
    }

    try:
        # Utilizing engine.begin() context manager to ensure atomic operations (All-or-Nothing)
        with engine.begin() as connection:
            for step_name, sql_query in queries.items():
                logging.info(f"Executing: {step_name}")
                connection.execute(text(sql_query))
        
        success_msg = "Successfully built and populated Star Schema (Dimensions & Fact tables)."
        logging.info(success_msg)
        print(f"Success: {success_msg}")
        return True

    except Exception as e:
        error_msg = f"An error occurred during Data Modeling: {e}"
        logging.error(error_msg)
        print(f"Error: {error_msg}")
        return False

if __name__ == "__main__":
    # Standalone verification block to test this module independently
    print("--- Running Data Modeling Independent Test ---")
    build_star_schema()
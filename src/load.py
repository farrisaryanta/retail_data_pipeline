import os
import pandas as pd
import logging
from config.database import get_db_engine

# Ensure logging configuration matches the pipeline standard
LOG_DIR = "logs"
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def load_data_to_postgres(df, target_table_name):
    """
    Loads a cleaned Pandas DataFrame into the specified PostgreSQL table.
    Uses SQLAlchemy engine for secure and efficient ingestion.
    """
    if df is None or df.empty:
        logging.error(f"Ingestion failed. No data provided for table: {target_table_name}")
        return False

    logging.info(f"Database ingestion initiated for table: {target_table_name}")
    
    # Get the database connection engine
    engine = get_db_engine()
    if engine is None:
        logging.error("Ingestion failed. Unable to establish database connection engine.")
        return False

    try:
        # Pushing data to PostgreSQL
        # if_exists='replace' means it will create the table if it doesn't exist, 
        # or overwrite it if it does. chunksize speeds up loading for large datasets.
        logging.info(f"Writing {len(df)} rows to database...")
        
        df.to_sql(
            name=target_table_name,
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=10000
        )
        
        success_message = f"Successfully loaded {len(df)} rows into PostgreSQL table: '{target_table_name}'."
        logging.info(success_message)
        print(f"Success: {success_message}")
        return True

    except Exception as e:
        error_message = f"An error occurred during database ingestion: {e}"
        logging.error(error_message)
        print(f"Error: {error_message}")
        return False

# Self-test block to verify ingestion logic independently
if __name__ == "__main__":
    # Import previous steps to build a local mini-pipeline for testing
    from src.extract import extract_raw_data
    from src.transform import transform_sales_data
    
    print("--- Running End-to-End Test for ETL (Extract, Transform, Load) ---")
    
    # 1. Extract
    raw_df = extract_raw_data("data/landing_zone/Warehouse_and_Retail_Sales.csv")
    
    # 2. Transform
    if raw_df is not None:
        cleaned_df = transform_sales_data(raw_df)
        
        # 3. Load
        if cleaned_df is not None:
            # We will name our production table 'fact_warehouse_retail_sales'
            table_name = "fact_warehouse_retail_sales"
            load_data_to_postgres(cleaned_df, table_name)
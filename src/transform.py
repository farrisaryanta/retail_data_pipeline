import os
import pandas as pd
import logging

# Ensure logging configuration matches the pipeline standard
LOG_DIR = "logs"
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def transform_sales_data(df):
    """
    Cleans and standardizes the extracted sales DataFrame.
    Prepares the data for clean ingestion into PostgreSQL.
    """
    if df is None or df.empty:
        logging.error("Transformation failed. Input DataFrame is empty or None.")
        return None

    logging.info("Transformation process initiated.")
    
    try:
        # Create a copy to avoid setting-with-copy warnings
        cleaned_df = df.copy()

        # 1. Standardize column names (Uppercase with spaces -> lowercase with underscores)
        # Example: 'ITEM CODE' becomes 'item_code'
        logging.info("Standardizing column names to lowercase snake_case.")
        cleaned_df.columns = (
            cleaned_df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
        )

        # 2. Handle Missing Values (Imputation)
        logging.info("Handling missing values across specific columns.")
        
        # Fill missing suppliers and item types with placeholder text
        cleaned_df['supplier'] = cleaned_df['supplier'].fillna('UNKNOWN SUPPLIER')
        cleaned_df['item_type'] = cleaned_df['item_type'].fillna('UNKNOWN')
        
        # Fill missing sales metrics with 0.0 numerical values
        cleaned_df['retail_sales'] = cleaned_df['retail_sales'].fillna(0.0)

        # 3. Clean and Trim text data columns
        logging.info("Trimming whitespace from string columns.")
        string_columns = ['supplier', 'item_description', 'item_type']
        for col in string_columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

        # 4. Preliminary deduplication
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        final_count = len(cleaned_df)
        
        if initial_count > final_count:
            logging.info(f"Removed {initial_count - final_count} duplicate rows during transformation.")

        success_message = f"Successfully transformed {len(cleaned_df)} rows of data."
        logging.info(success_message)
        print(f"Success: {success_message}")

        return cleaned_df

    except Exception as e:
        error_message = f"An error occurred during data transformation: {e}"
        logging.error(error_message)
        print(f"Error: {error_message}")
        return None

# Self-test block to verify transformation logic independently
if __name__ == "__main__":
    # Import the extraction function we completed in the previous step
    from src.extract import extract_raw_data
    
    target_file = "data/landing_zone/Warehouse_and_Retail_Sales.csv"
    print("--- Running End-to-End Test for Extract & Transform ---")
    
    # 1. Extract
    raw_data = extract_raw_data(target_file)
    
    # 2. Transform
    if raw_data is not None:
        transformed_data = transform_sales_data(raw_data)
        
        if transformed_data is not None:
            print("\n--- Preview of Transformed Data (Notice the clean column headers) ---")
            print(transformed_data.head(3))
            print("\nColumns now available:", transformed_data.columns.tolist())
import os
import pandas as pd
import logging

# Setup directory for logs if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure the logging system
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def extract_raw_data(file_path):
    """
    Reads a raw CSV file from the landing zone and returns a Pandas DataFrame.
    Includes automated logging for tracking and error handling.
    """
    logging.info(f"Extraction process initiated for file: {file_path}")
    
    # Check if the file actually exists before reading
    if not os.path.exists(file_path):
        error_message = f"Extraction failed. File not found at path: {file_path}"
        logging.error(error_message)
        print(f"Error: {error_message}")
        return None
    
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        success_message = f"Successfully extracted {len(df)} rows from {file_path}"
        logging.info(success_message)
        print(f"Success: {success_message}")
        
        return df
        
    except Exception as e:
        error_message = f"An error occurred during CSV extraction: {e}"
        logging.error(error_message)
        print(f"Error: {error_message}")
        return None

# Self-test block to verify extraction logic independently
if __name__ == "__main__":
    target_file = "data/landing_zone/Warehouse_and_Retail_Sales.csv"
    print(f"Executing self-test for extraction on: {target_file}")
    
    raw_dataframe = extract_raw_data(target_file)
    if raw_dataframe is not None:
        print("\n--- Preview of Extracted Data ---")
        print(raw_dataframe)
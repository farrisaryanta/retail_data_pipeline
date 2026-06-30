import os
import logging
from src.extract import extract_raw_data
from src.transform import transform_sales_data
from src.load import load_data_to_postgres
from src.model import build_star_schema  # Orchestrating the new modeling component

# Configure centralized logging directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Global logging system setup for tracking production pipeline runs
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def run_etl_pipeline():
    """
    Main orchestration function that triggers the end-to-end data engineering pipeline.
    """
    logging.info("========================================")
    logging.info("ETL PIPELINE EXECUTION STARTED")
    logging.info("========================================")
    print("Starting End-to-End ETL Pipeline...\n")

    # Defining project path configurations
    source_file = "data/landing_zone/Warehouse_and_Retail_Sales.csv"
    target_table = "fact_warehouse_retail_sales"

    # 1. EXTRACT PHASE
    print("[1/4] Initiating Data Extraction...")
    raw_data = extract_raw_data(source_file)
    if raw_data is None:
        logging.error("Pipeline aborted during the extraction phase.")
        print("Pipeline Failed at Extraction Phase.")
        return

    # 2. TRANSFORM PHASE
    print("\n[2/4] Initiating Data Transformation...")
    cleaned_data = transform_sales_data(raw_data)
    if cleaned_data is None:
        logging.error("Pipeline aborted during the transformation phase.")
        print("Pipeline Failed at Transformation Phase.")
        return

    # 3. LOAD PHASE (Staging Environment Ingestion)
    print("\n[3/4] Initiating Database Ingestion...")
    success = load_data_to_postgres(cleaned_data, target_table)
    if not success:
        logging.error("Pipeline aborted during the database ingestion phase.")
        print("Pipeline Failed at Loading Phase.")
        return

    # 4. DATA MODELING PHASE (Automated Data Warehouse Transformation)
    print("\n")
    modeling_success = build_star_schema()
    if not modeling_success:
        logging.error("Pipeline aborted during the dimensional modeling phase.")
        print("Pipeline Failed at Data Modeling Phase.")
        return

    logging.info("========================================")
    logging.info("ETL PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    logging.info("========================================")
    print("\nComplete Success: End-to-End Pipeline & Data Modeling automated successfully!")

if __name__ == "__main__":
    run_etl_pipeline()
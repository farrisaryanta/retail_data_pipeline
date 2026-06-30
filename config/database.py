import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from the .env file
load_dotenv()

def get_db_engine():
    """
    Creates and returns a PostgreSQL connection engine using SQLAlchemy.
    """
    # Fetch credentials from environment variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Construct the PostgreSQL connection URL
    # Format: postgresql://user:password@host:port/database_name
    connection_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(connection_url)
        return engine
    except Exception as e:
        print(f"Failed to create database connection: {e}")
        return None

# This block only runs if the script is executed directly (for testing purposes)
if __name__ == "__main__":
    engine = get_db_engine()
    if engine:
        try:
            # Attempt to connect to the database
            connection = engine.connect()
            print("Success! Python is successfully connected to the 'retail_db' PostgreSQL database.")
            connection.close()
        except Exception as e:
            print(f"Connection failed. Please check your credentials or ensure the PostgreSQL service is running. Error: {e}")
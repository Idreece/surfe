from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from utils.database import get_database_connection

def clean_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert datetime columns and handle NaT values"""
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_date'] = df['created_at'].dt.date
    return df

def clean_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert boolean columns"""
    df['tax_location_recognized'] = df['tax_location_recognized'].astype(bool)
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename CSV columns to match database schema"""
    column_mapping = {
        'id': 'customer_id',
        'Created (UTC)': 'created_at',
        'Tax Location Recognized': 'tax_location_recognized'
    }
    return df.rename(columns=column_mapping)

def get_upsert_query() -> str:
    """Return the SQL upsert query"""
    return """
        INSERT INTO customers (customer_id, created_at, created_date, tax_location_recognized)
        VALUES (:customer_id, :created_at, :created_date, :tax_location_recognized)
        ON CONFLICT (customer_id) 
        DO UPDATE SET
            created_at = EXCLUDED.created_at,
            created_date = EXCLUDED.created_date,
            tax_location_recognized = EXCLUDED.tax_location_recognized
    """

def update_customers() -> None:
    try:
        engine = get_database_connection()
        
        df = pd.read_csv('data/customers.csv')
        
        df = rename_columns(df)
        df = clean_datetime_columns(df)
        df = clean_boolean_columns(df)
        
        upsert_query = get_upsert_query()
        
        with engine.connect() as conn:
            for _, row in df.iterrows():
                conn.execute(
                    text(upsert_query),
                    {
                        'customer_id': row['customer_id'],
                        'created_at': row['created_at'],
                        'created_date': row['created_date'],
                        'tax_location_recognized': row['tax_location_recognized']
                    }
                )
            conn.commit()
            
        print(f"Successfully processed {len(df)} customer records")
        
    except Exception as e:
        print(f"Error updating customers: {e}")

if __name__ == "__main__":
    update_customers() 
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

def update_customers():
    try:
        # Create SQLAlchemy engine
        engine = create_engine('postgresql://surfe_user:surfe_password@postgres:5432/surfe_db')
        
        # Read the CSV file
        df = pd.read_csv('data/customers.csv')
        
        # Rename columns to match database schema
        df = df.rename(columns={
            'id': 'customer_id',
            'Created (UTC)': 'created_at',
            'Tax Location Recognized': 'tax_location_recognized'
        })
        
        # Ensure required columns exist
        required_columns = ['customer_id', 'created_at', 'tax_location_recognized']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        
        # Convert created_at to datetime if it's not already
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Extract date for created_date column
        df['created_date'] = df['created_at'].dt.date
        
        # Prepare the upsert query
        upsert_query = """
            INSERT INTO customers (customer_id, created_at, created_date, tax_location_recognized)
            VALUES (:customer_id, :created_at, :created_date, :tax_location_recognized)
            ON CONFLICT (customer_id) 
            DO UPDATE SET
                created_at = EXCLUDED.created_at,
                created_date = EXCLUDED.created_date,
                tax_location_recognized = EXCLUDED.tax_location_recognized
        """
        
        # Execute upsert for each row
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
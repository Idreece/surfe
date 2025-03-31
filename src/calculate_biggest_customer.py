from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Optional
from utils.database import get_database_connection

def get_biggest_customers_query() -> str:
    return """
    WITH weekly_customer_spend AS (
        SELECT 
            DATE_TRUNC('week', created_at) as week,
            EXTRACT(YEAR FROM created_at) as year,
            EXTRACT(WEEK FROM created_at) as week_number,
            customer_id,
            currency,
            SUM(total) as total_spend
        FROM invoices
        WHERE is_forgiven = FALSE
        GROUP BY 
            DATE_TRUNC('week', created_at),
            EXTRACT(YEAR FROM created_at),
            EXTRACT(WEEK FROM created_at),
            customer_id,
            currency
    ),
    ranked_customers AS (
        SELECT 
            year,
            week_number,
            customer_id,
            currency,
            total_spend,
            ROW_NUMBER() OVER (
                PARTITION BY year, week_number, currency 
                ORDER BY total_spend DESC
            ) as rank
        FROM weekly_customer_spend
    )
    SELECT 
        year,
        week_number,
        MAX(CASE WHEN currency = 'eur' AND rank = 1 THEN customer_id END) as top_eur_customer,
        MAX(CASE WHEN currency = 'eur' AND rank = 1 THEN total_spend END) as top_eur_spend,
        MAX(CASE WHEN currency = 'usd' AND rank = 1 THEN customer_id END) as top_usd_customer,
        MAX(CASE WHEN currency = 'usd' AND rank = 1 THEN total_spend END) as top_usd_spend
    FROM ranked_customers
    GROUP BY year, week_number
    ORDER BY year, week_number;
    """

def execute_biggest_customers_query(engine: create_engine) -> Optional[pd.DataFrame]:
    try:
        query = get_biggest_customers_query()
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing biggest customers query: {e}")
        return None

def save_biggest_customers_to_csv(df: Optional[pd.DataFrame]) -> None:
    if df is not None:
        try:
            df['week_year'] = df['year'].astype(str) + '-W' + df['week_number'].astype(str)
            
            df = df[[
                'week_year',
                'top_eur_customer',
                'top_eur_spend',
                'top_usd_customer',
                'top_usd_spend'
            ]]
            
            df['top_eur_spend'] = df['top_eur_spend'].round(2)
            df['top_usd_spend'] = df['top_usd_spend'].round(2)
            
            date_tag = datetime.now().strftime('%Y%m%d')
            output_file = f"output/biggest_customers_{date_tag}.csv"
            
            df.to_csv(output_file, index=False)
            print(f"Biggest customers data saved to {output_file}")
        except Exception as e:
            print(f"Error saving biggest customers data to CSV: {e}")
    else:
        print("No biggest customers data available to save.")

def calculate_biggest_customers() -> None:
    try:
        engine = get_database_connection()
        df = execute_biggest_customers_query(engine)
        save_biggest_customers_to_csv(df)
    except Exception as e:
        print(f"Error calculating biggest customers: {e}")

if __name__ == "__main__":
    calculate_biggest_customers() 
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Optional
from utils.database import get_database_connection

def get_weekly_metrics_query() -> str:
    return """
    WITH weekly_metrics AS (
        SELECT 
            DATE_TRUNC('week', created_at) as week,
            EXTRACT(YEAR FROM created_at) as year,
            EXTRACT(WEEK FROM created_at) as week_number,
            SUM(CASE WHEN currency = 'eur' THEN total ELSE 0 END) as eur_total,
            SUM(CASE WHEN currency = 'usd' THEN total ELSE 0 END) as usd_total,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM invoices
        WHERE is_forgiven = FALSE
        GROUP BY 
            DATE_TRUNC('week', created_at),
            EXTRACT(YEAR FROM created_at),
            EXTRACT(WEEK FROM created_at)
    )
    SELECT 
        year,
        week_number,
        eur_total,
        usd_total,
        unique_customers,
        LAG(unique_customers) OVER (ORDER BY year, week_number) as prev_week_customers,
        unique_customers - LAG(unique_customers) OVER (ORDER BY year, week_number) as customer_delta
    FROM weekly_metrics
    ORDER BY year, week_number;
    """

def execute_weekly_metrics_query(engine: create_engine) -> Optional[pd.DataFrame]:
    try:
        query = get_weekly_metrics_query()
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing weekly metrics query: {e}")
        return None

def save_metrics_to_csv(df: Optional[pd.DataFrame]) -> None:
    if df is not None:
        try:
            df['week_year'] = df['year'].astype(str) + '-W' + df['week_number'].astype(str)
            
            df = df[['week_year', 'eur_total', 'usd_total', 'unique_customers', 'prev_week_customers', 'customer_delta']]
            
            df['eur_total'] = df['eur_total'].round(2)
            df['usd_total'] = df['usd_total'].round(2)
            
            date_tag = datetime.now().strftime('%Y%m%d')
            output_file = f"output/weekly_metrics_{date_tag}.csv"
            
            df.to_csv(output_file, index=False)
            print(f"Weekly metrics saved to {output_file}")
        except Exception as e:
            print(f"Error saving weekly metrics to CSV: {e}")
    else:
        print("No weekly metrics available to save.")

def calculate_weekly_metrics() -> None:
    try:
        engine = get_database_connection()
        df = execute_weekly_metrics_query(engine)
        save_metrics_to_csv(df)
    except Exception as e:
        print(f"Error calculating weekly metrics: {e}")

if __name__ == "__main__":
    calculate_weekly_metrics() 
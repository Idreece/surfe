from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Optional
from utils.database import get_database_connection

def get_mrr_query() -> str:
    return """
    WITH monthly_revenue AS (
        SELECT 
            DATE_TRUNC('month', period_start) as month,
            SUM(total) as monthly_revenue,
            COUNT(DISTINCT subscription_id) as active_subscriptions
        FROM invoices
        WHERE customer_id = :customer_id
        AND period_start <= :as_of_date
        AND is_forgiven = FALSE 
        GROUP BY DATE_TRUNC('month', period_start)
    )
    SELECT 
        month,
        monthly_revenue,
        active_subscriptions,
        monthly_revenue / NULLIF(active_subscriptions, 0) as mrr_per_subscription,
        monthly_revenue as mrr
    FROM monthly_revenue
    ORDER BY month DESC;
    """

def execute_mrr_query(engine: create_engine, customer_id: str, as_of_date: datetime) -> Optional[pd.DataFrame]:
    try:
        query = get_mrr_query()
        with engine.connect() as conn:
            result = conn.execute(
                text(query),
                {
                    'customer_id': customer_id,
                    'as_of_date': as_of_date
                }
            )
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing MRR query: {e}")
        return None

def save_mrr_to_csv(df: Optional[pd.DataFrame], customer_id: str, output_dir: str = "output") -> None:
    if df is not None:
        try:
            df.to_csv(f"{output_dir}/mrr_{customer_id}.csv", index=False)
            print(f"MRR data saved to {output_dir}/mrr_{customer_id}.csv")
        except Exception as e:
            print(f"Error saving MRR data to CSV: {e}")
    else:
        print("No MRR data available to save.")

def calculate_mrr(customer_id: str, as_of_date: datetime, output_dir: str = "output") -> None:
    try:
        engine = get_database_connection()
        df = execute_mrr_query(engine, customer_id, as_of_date)
        save_mrr_to_csv(df, customer_id, output_dir)
    except Exception as e:
        print(f"Error calculating MRR: {e}")

def main() -> None:
    """
    Main function to demonstrate MRR calculation usage.
    """
    customer_id = "cus_RgLOYG9tQ1hPEh" 
    as_of_date = datetime(2025, 12, 31) 
    
    calculate_mrr(customer_id, as_of_date)

if __name__ == "__main__":
    main() 
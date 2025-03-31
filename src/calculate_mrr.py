from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Optional
from utils.database import get_database_connection
import argparse

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
    parser = argparse.ArgumentParser(description='Calculate Monthly Recurring Revenue (MRR) for a customer')
    parser.add_argument('--customer-id', required=True, help='The Stripe customer ID')
    parser.add_argument('--as-of-date', required=True, help='The date to calculate MRR as of (YYYY-MM-DD)')
    parser.add_argument('--output-dir', default='output', help='Directory to save the output CSV file')
    
    args = parser.parse_args()
    
    try:
        as_of_date = datetime.strptime(args.as_of_date, '%Y-%m-%d')
        calculate_mrr(args.customer_id, as_of_date, args.output_dir)
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD format.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
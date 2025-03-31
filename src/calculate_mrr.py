from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from typing import Optional
from utils.database import get_database_connection
import argparse

def get_mrr_query() -> str:
    return """
    WITH customer_tenure AS (
        SELECT 
            customer_id,
            EXTRACT(MONTH FROM AGE(:as_of_date, created_at)) as months_since_joined
        FROM customers
        WHERE customer_id = :customer_id
    ),
    monthly_revenue AS (
        SELECT 
            DATE_TRUNC('month', period_start) as month,
            currency,
            SUM(total) as monthly_revenue,
            COUNT(DISTINCT subscription_id) as active_subscriptions
        FROM invoices
        WHERE customer_id = :customer_id
        AND period_start <= :as_of_date
        AND is_forgiven = FALSE 
        AND currency IN ('eur', 'usd')
        GROUP BY DATE_TRUNC('month', period_start), currency
    )
    SELECT 
        m.month,
        m.currency,
        m.monthly_revenue,
        m.active_subscriptions,
        m.monthly_revenue / NULLIF(m.active_subscriptions, 0) as mrr_per_subscription,
        m.monthly_revenue as mrr,
        CASE WHEN m.active_subscriptions > 0 THEN TRUE ELSE FALSE END as has_subscription,
        c.months_since_joined
    FROM monthly_revenue m
    CROSS JOIN customer_tenure c
    ORDER BY m.month DESC, m.currency;
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

def save_mrr_to_csv(df: Optional[pd.DataFrame], customer_id: str, as_of_date: datetime, output_dir: str = "output") -> None:
    if df is not None:
        try:
            date_str = as_of_date.strftime('%Y%m%d')
            df.to_csv(f"{output_dir}/mrr_{customer_id}_{date_str}.csv", index=False)
            print(f"MRR data saved to {output_dir}/mrr_{customer_id}_{date_str}.csv")
        except Exception as e:
            print(f"Error saving MRR data to CSV: {e}")
    else:
        print("No MRR data available to save.")

def calculate_mrr(customer_id: str, as_of_date: datetime, output_dir: str = "output") -> None:
    try:
        engine = get_database_connection()
        df = execute_mrr_query(engine, customer_id, as_of_date)
        save_mrr_to_csv(df, customer_id, as_of_date, output_dir)
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
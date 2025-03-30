from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from datetime import datetime

def clean_numeric_columns(df):
    """Convert numeric columns from string with commas to float"""
    numeric_columns = [
        'amount_due', 'subtotal', 'tax', 'tax_percent', 'total',
        'amount_paid', 'total_discount_amount', 'exclusive_tax_amount',
        'inclusive_tax_amount', 'starting_balance', 'ending_balance'
    ]
    for col in numeric_columns:
        # Convert to string first to handle any format
        df[col] = df[col].astype(str)
        # Replace commas with periods
        df[col] = df[col].str.replace(',', '.')
        # Convert to float, replacing any invalid values with 0.0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    return df

def clean_datetime_columns(df):
    """Convert datetime columns and handle NaT values"""
    datetime_columns = [
        'created_at', 'due_date', 'paid_at', 'marked_uncollectible_at',
        'voided_at', 'finalized_at', 'period_start', 'period_end',
        'min_line_item_period_start', 'max_line_item_period_end'
    ]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].replace({pd.NaT: None})
    
    # Extract date for created_date column
    df['created_date'] = df['created_at'].dt.date
    return df

def clean_boolean_columns(df):
    """Convert boolean columns"""
    boolean_columns = ['is_paid', 'is_closed', 'is_forgiven']
    for col in boolean_columns:
        df[col] = df[col].astype(bool)
    return df

def clean_string_columns(df):
    """Handle NaN in string columns"""
    df['applied_coupons'] = df['applied_coupons'].fillna('')
    return df

def rename_columns(df):
    """Rename CSV columns to match database schema"""
    column_mapping = {
        'id': 'invoice_id',
        'Customer': 'customer_id',
        'Subscription': 'subscription_id',
        'Status': 'status',
        'Currency': 'currency',
        'Amount Due': 'amount_due',
        'Subtotal': 'subtotal',
        'Tax': 'tax',
        'Tax Percent': 'tax_percent',
        'Total': 'total',
        'Amount Paid': 'amount_paid',
        'Total Discount Amount': 'total_discount_amount',
        'Exclusive Tax Amount': 'exclusive_tax_amount',
        'Inclusive Tax Amount': 'inclusive_tax_amount',
        'Starting Balance': 'starting_balance',
        'Ending Balance': 'ending_balance',
        'Date (UTC)': 'created_at',
        'Due Date (UTC)': 'due_date',
        'Paid At (UTC)': 'paid_at',
        'Marked Uncollectible At (UTC)': 'marked_uncollectible_at',
        'Voided At (UTC)': 'voided_at',
        'Finalized At (UTC)': 'finalized_at',
        'Period Start (UTC)': 'period_start',
        'Period End (UTC)': 'period_end',
        'Minimum Line Item Period Start (UTC)': 'min_line_item_period_start',
        'Maximum Line Item Period End (UTC)': 'max_line_item_period_end',
        'Paid': 'is_paid',
        'Closed': 'is_closed',
        'Forgiven': 'is_forgiven',
        'Applied Coupons': 'applied_coupons'
    }
    return df.rename(columns=column_mapping)

def get_upsert_query():
    """Return the SQL upsert query"""
    return """
        INSERT INTO invoices (
            invoice_id, customer_id, subscription_id, status, currency,
            amount_due, subtotal, tax, tax_percent, total,
            amount_paid, total_discount_amount, exclusive_tax_amount, inclusive_tax_amount,
            starting_balance, ending_balance, created_at, created_date,
            due_date, paid_at, marked_uncollectible_at, voided_at,
            finalized_at, period_start, period_end,
            min_line_item_period_start, max_line_item_period_end,
            is_paid, is_closed, is_forgiven, applied_coupons
        )
        VALUES (
            :invoice_id, :customer_id, :subscription_id, :status, :currency,
            :amount_due, :subtotal, :tax, :tax_percent, :total,
            :amount_paid, :total_discount_amount, :exclusive_tax_amount, :inclusive_tax_amount,
            :starting_balance, :ending_balance, :created_at, :created_date,
            :due_date, :paid_at, :marked_uncollectible_at, :voided_at,
            :finalized_at, :period_start, :period_end,
            :min_line_item_period_start, :max_line_item_period_end,
            :is_paid, :is_closed, :is_forgiven, :applied_coupons
        )
        ON CONFLICT (invoice_id) 
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            subscription_id = EXCLUDED.subscription_id,
            status = EXCLUDED.status,
            currency = EXCLUDED.currency,
            amount_due = EXCLUDED.amount_due,
            subtotal = EXCLUDED.subtotal,
            tax = EXCLUDED.tax,
            tax_percent = EXCLUDED.tax_percent,
            total = EXCLUDED.total,
            amount_paid = EXCLUDED.amount_paid,
            total_discount_amount = EXCLUDED.total_discount_amount,
            exclusive_tax_amount = EXCLUDED.exclusive_tax_amount,
            inclusive_tax_amount = EXCLUDED.inclusive_tax_amount,
            starting_balance = EXCLUDED.starting_balance,
            ending_balance = EXCLUDED.ending_balance,
            created_at = EXCLUDED.created_at,
            created_date = EXCLUDED.created_date,
            due_date = EXCLUDED.due_date,
            paid_at = EXCLUDED.paid_at,
            marked_uncollectible_at = EXCLUDED.marked_uncollectible_at,
            voided_at = EXCLUDED.voided_at,
            finalized_at = EXCLUDED.finalized_at,
            period_start = EXCLUDED.period_start,
            period_end = EXCLUDED.period_end,
            min_line_item_period_start = EXCLUDED.min_line_item_period_start,
            max_line_item_period_end = EXCLUDED.max_line_item_period_end,
            is_paid = EXCLUDED.is_paid,
            is_closed = EXCLUDED.is_closed,
            is_forgiven = EXCLUDED.is_forgiven,
            applied_coupons = EXCLUDED.applied_coupons
    """

def update_invoices():
    try:
        # Create SQLAlchemy engine
        engine = create_engine('postgresql://surfe_user:surfe_password@postgres:5432/surfe_db')
        
        # Read and clean the data
        df = pd.read_csv('data/invoices.csv')
        df = rename_columns(df)
        df = clean_numeric_columns(df)
        df = clean_datetime_columns(df)
        df = clean_boolean_columns(df)
        df = clean_string_columns(df)
        
        # Get the upsert query
        upsert_query = get_upsert_query()
        
        # Execute upsert for each row
        with engine.connect() as conn:
            for _, row in df.iterrows():
                conn.execute(text(upsert_query), row.to_dict())
            conn.commit()
            
        print(f"Successfully processed {len(df)} invoice records")
        
    except Exception as e:
        print(f"Error updating invoices: {e}")

if __name__ == "__main__":
    update_invoices() 
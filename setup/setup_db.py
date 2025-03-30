from sqlalchemy import create_engine, text
from src.utils.database import get_database_connection

def setup_database():
    try:
        engine = get_database_connection()
        
        with engine.connect() as conn:
            conn.execute(text("""
                DROP TABLE IF EXISTS payments CASCADE;
                DROP TABLE IF EXISTS invoices CASCADE;
                DROP TABLE IF EXISTS subscriptions CASCADE;
                DROP TABLE IF EXISTS customers CASCADE;
            """))
            
            conn.execute(text("""
                CREATE TABLE customers (
                    customer_id VARCHAR(50) PRIMARY KEY,
                    created_at TIMESTAMPTZ,
                    created_date DATE,
                    tax_location_recognized BOOLEAN
                );
                CREATE INDEX idx_customers_created_date ON customers (created_date);
            """))
            
            conn.execute(text("""
                CREATE TABLE subscriptions (
                    subscription_id VARCHAR(50) PRIMARY KEY,
                    customer_id VARCHAR(50),
                    status VARCHAR(20),
                    created_at TIMESTAMPTZ,
                    created_date DATE,
                    current_period_start TIMESTAMPTZ,
                    current_period_end TIMESTAMPTZ,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                );
                CREATE INDEX idx_subscriptions_customer_id ON subscriptions (customer_id);
                CREATE INDEX idx_subscriptions_created_date ON subscriptions (created_date);
            """))
            
            conn.execute(text("""
                CREATE TABLE invoices (
                    invoice_id VARCHAR(50) PRIMARY KEY,
                    customer_id VARCHAR(50),
                    subscription_id VARCHAR(50),
                    status VARCHAR(20),
                    currency CHAR(3),
                    amount_due NUMERIC(15,2),
                    subtotal NUMERIC(15,2),
                    tax NUMERIC(15,2),
                    tax_percent NUMERIC(5,2),
                    total NUMERIC(15,2),
                    amount_paid NUMERIC(15,2),
                    total_discount_amount NUMERIC(15,2),
                    exclusive_tax_amount NUMERIC(15,2),
                    inclusive_tax_amount NUMERIC(15,2),
                    starting_balance NUMERIC(15,2),
                    ending_balance NUMERIC(15,2),
                    created_at TIMESTAMPTZ,
                    created_date DATE,
                    due_date TIMESTAMPTZ,
                    paid_at TIMESTAMPTZ,
                    marked_uncollectible_at TIMESTAMPTZ,
                    voided_at TIMESTAMPTZ,
                    finalized_at TIMESTAMPTZ,
                    period_start TIMESTAMPTZ,
                    period_end TIMESTAMPTZ,
                    min_line_item_period_start TIMESTAMPTZ,
                    max_line_item_period_end TIMESTAMPTZ,
                    is_paid BOOLEAN,
                    is_closed BOOLEAN,
                    is_forgiven BOOLEAN,
                    applied_coupons TEXT
                );
                CREATE INDEX idx_invoices_customer_id ON invoices (customer_id);
                CREATE INDEX idx_invoices_created_date ON invoices (created_date);
            """))
            
            conn.execute(text("""
                CREATE TABLE payments (
                    payment_id VARCHAR(50) PRIMARY KEY,
                    customer_id VARCHAR(50),
                    invoice_id VARCHAR(50),
                    amount NUMERIC(15,2),
                    currency CHAR(3),
                    payment_method VARCHAR(50),
                    status VARCHAR(20),
                    created_at TIMESTAMPTZ,
                    created_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
                );
                CREATE INDEX idx_payments_customer_id ON payments (customer_id);
                CREATE INDEX idx_payments_created_date ON payments (created_date);
            """))
            
            conn.commit()
            
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database() 
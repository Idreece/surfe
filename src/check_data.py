from sqlalchemy import create_engine
import pandas as pd

def check_data():
    try:
        # Create SQLAlchemy engine
        engine = create_engine('postgresql://surfe_user:surfe_password@postgres:5432/surfe_db')
        
        # List of tables to check
        tables = ['customers', 'subscriptions', 'invoices', 'payments']
        
        for table in tables:
            # Load data into pandas DataFrame using SQLAlchemy
            df = pd.read_sql_query(f"SELECT * FROM {table}", engine)
            
            # Print the data
            print(f"\nData from {table} table:")
            print("-" * 50)
            print(df)
            print("\n")
        
    except Exception as e:
        print(f"Error checking data: {e}")

if __name__ == "__main__":
    check_data() 
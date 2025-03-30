from sqlalchemy import create_engine
import pandas as pd
from utils.database import get_database_connection

def check_data() -> None:
    try:
        engine = get_database_connection()
        
        tables = ['customers', 'subscriptions', 'invoices', 'payments']
        
        for table in tables:
            df = pd.read_sql_query(f"SELECT * FROM {table}", engine)
            
            print(f"\nData from {table} table:")
            print("-" * 50)
            print(df)
            print("\n")
        
    except Exception as e:
        print(f"Error checking data: {e}")

if __name__ == "__main__":
    check_data() 
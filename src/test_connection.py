import os
import psycopg2

def test_connection():
    try:
        # Connect to the database
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Test query
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print(f"Connected to PostgreSQL: {version[0]}")
        
        # Close connections
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection() 
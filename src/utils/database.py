from sqlalchemy import create_engine

def get_database_connection() -> create_engine:
    return create_engine('postgresql://surfe_user:surfe_password@postgres:5432/surfe_db') 
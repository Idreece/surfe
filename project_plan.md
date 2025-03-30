# Surfe Analytics Project Plan

## Project Overview
This project involves building a PostgreSQL-based analytics solution for analyzing customer and invoice data, with a focus on Monthly Recurring Revenue (MRR) calculations and insights.

## Project Structure
```
surfe/
├── README.md
├── requirements.txt
├── .env
├── data/
│   ├── customers.csv
│   └── invoices.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── ingestion.py
│   ├── mrr.py
│   ├── analytics.py
│   └── forecasting.py
├── tests/
│   └── __init__.py
└── notebooks/
    └── analysis.ipynb
```

## Implementation Plan

### 1. Project Setup
- Create Python virtual environment
- Set up requirements.txt with necessary packages:
  - `pandas` for data manipulation
  - `sqlalchemy` for database ORM
  - `psycopg2-binary` for PostgreSQL connection
  - `python-dotenv` for environment variables
  - `fastapi` (optional) for API creation
  - `scikit-learn` (optional) for forecasting

### 2. Database Design
Two main tables will be created:

#### Customers Table
```sql
CREATE TABLE customers (
    id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP,
    total_spend DECIMAL(10,2),
    payment_count INTEGER,
    tax_location_recognized BOOLEAN
);
```

#### Invoices Table
```sql
CREATE TABLE invoices (
    id VARCHAR(50) PRIMARY KEY,
    amount_due DECIMAL(10,2),
    closed BOOLEAN,
    currency VARCHAR(3),
    customer_id VARCHAR(50),
    date TIMESTAMP,
    due_date TIMESTAMP,
    ending_balance DECIMAL(10,2),
    forgiven BOOLEAN,
    paid BOOLEAN,
    paid_at TIMESTAMP,
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    starting_balance DECIMAL(10,2),
    subscription_id VARCHAR(50),
    subtotal DECIMAL(10,2),
    total_discount_amount DECIMAL(10,2),
    tax DECIMAL(10,2),
    tax_percent INTEGER,
    total DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### 3. Implementation Phases

#### Phase 1: Data Ingestion
- Create data ingestion script
- Handle CSV file reading with pandas
- Implement data cleaning:
  - Currency formatting
  - Date parsing
  - Data validation
- Use SQLAlchemy for database operations
- Add error handling and logging

#### Phase 2: MRR Calculation
- Implement MRR calculation function
- Handle edge cases:
  - Partial months
  - Currency conversions
  - Discounts and refunds
- Create cohort analysis based on customer acquisition date

#### Phase 3: Analytics Implementation
- Develop separate modules for:
  - Month-over-month growth calculation
  - Churn rate analysis
  - Customer segmentation
  - Significant changes detection
- Implement data validation
- Add error handling

#### Phase 4: Forecasting (Optional)
- Implement time series analysis
- Create simple linear regression or ARIMA model
- Include confidence intervals
- Document assumptions and limitations

## Next Steps
1. Set up development environment
2. Create database schema
3. Implement data ingestion
4. Build MRR calculation logic
5. Develop analytics functions
6. Add forecasting (if time permits)
7. Create comprehensive documentation

## Notes
- Each phase should be implemented and tested independently
- Documentation should be updated as features are added
- Code should follow Python best practices and PEP 8 guidelines
- Tests should be written for critical functionality 
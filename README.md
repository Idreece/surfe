# Surfe Analytics Project

This project sets up a PostgreSQL database with Python for data analytics. It uses Docker to ensure consistent environments and easy setup.

## Prerequisites

- Docker and Docker Compose installed
- Colima also installed if you are on Apple Silicon
- Git (for version control)


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Idreece/surfe.git
   cd surfe
   ```

2. Start the Docker environment:
   ```bash
   ./setup/env_start.sh start
   ```
   This will:
   - Build the Python Docker image
   - Start PostgreSQL container
   - Start Python container
   - Create a Docker network for communication

3. Initialize the database:
   ```bash
   docker exec surfe_python python setup/setup_db.py
   ```
   This creates:
   - The database schema
   - Required tables

## Data Loading

1. Load customer data:
   ```bash
   docker exec surfe_python python src/update_customers.py
   ```
   This will process and load customer records into the database.

2. Load invoice data:
   ```bash
   docker exec surfe_python python src/update_invoices.py
   ```
   This will process and load invoice records into the database.

## Managing the Environment

- To stop the environment:
  ```bash
  ./setup/env_start.sh stop
  ```

- To restart the environment:
  ```bash
  ./setup/env_start.sh stop && ./setup/env_start.sh start
  ```

## Database Configuration

- Database Name: surfe_db
- Username: surfe_user
- Password: surfe_password
- Host: postgres
- Port: 5432

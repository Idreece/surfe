# PostgreSQL Analytics Project

This project sets up a PostgreSQL database with Python for data analytics. It uses Docker to ensure consistent environments and easy setup.

## Project Structure

```
.
├── setup/                  # Setup and configuration files
│   ├── Dockerfile         # Python environment configuration
│   ├── docker-compose.yml # Docker services configuration
│   ├── env_start.sh      # Script to manage Docker environment
│   └── setup_db.py       # Database initialization script
├── src/                   # Source code
│   └── load_data.py      # Data loading and testing script
├── data/                  # Data files directory
└── README.md             # This file
```

## Prerequisites

- Docker and Docker Compose installed
- Git (for version control)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
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
   - Test data table

4. Test the setup:
   ```bash
   docker exec surfe_python python src/load_data.py
   ```
   This will:
   - Insert sample test data
   - Read and display the data

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

## Current Features

- Containerized PostgreSQL database
- Python environment with SQLAlchemy and Pandas
- Sample data loading and querying capabilities
- Easy environment management scripts

## Next Steps

- Add data analysis notebooks
- Import real datasets
- Create analysis pipelines
- Add visualization capabilities 
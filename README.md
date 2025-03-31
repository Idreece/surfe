# Surfe Analytics Project

This project sets up a PostgreSQL database with Python for data analytics. It uses Docker to ensure consistent environments and easy setup.

## Prerequisites

### For macOS:

1. Homebrew (Package Manager for macOS):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Docker and Docker Compose:
   ```bash
   # Install Docker Engine and Docker Compose
   brew install docker
   brew install docker-compose
   ```

3. Colima (for Apple Silicon):
   ```bash
   brew install colima
   ```

4. Git:
   ```bash
   brew install git
   ```

### For Windows:

1. Install Git:
   - Download Git from: https://git-scm.com/download/win
   - Run the installer with default settings

2. Install Docker Desktop for Windows:
   - Download Docker Desktop from: https://www.docker.com/products/docker-desktop
   - Run the installer
   - During installation, ensure WSL 2 is enabled if prompted
   - Restart your computer after installation

### Verify Installation

After installation, verify the versions in your terminal/command prompt:
```bash
docker --version
docker-compose --version
git --version
```

Note: Python is provided within the Docker container, so no local Python installation is required.

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

3. Initialise the database:
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

## Running Scripts

- Once the docer image has started and you have run the steps above, you can run any of the scripts with:
  ```bash
   docker exec surfe_python python "Script Path from root" 
  ```
  Note that in a production environment the database server would be accessed across a network and would be always live

## Running analysis Notebooks

- Unfortunetly I had some difficulty setting up jupyter notebook connection to the docker python image, constrained by time I moved on, so to run ad hoc analysis you will need to install the packages in requirements.txt into one of your local python environments. Typically ad hoc analysis will be done in a seperate space.

## Database Configuration

- Database Name: surfe_db
- Username: surfe_user
- Password: surfe_password
- Host: postgres
- Port: 5432

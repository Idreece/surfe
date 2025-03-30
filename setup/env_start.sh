#!/bin/bash

# Function to start the environment
start_env() {
    echo "Starting environment..."
    docker-compose -f setup/docker-compose.yml up -d
}

# Function to stop the environment
stop_env() {
    echo "Stopping environment..."
    docker-compose -f setup/docker-compose.yml down
}

# Function to test the environment
test_env() {
    echo "Testing environment..."
    docker exec surfe_python python setup/test_connection.py
}

# Main script
case "$1" in
    "start")
        start_env
        ;;
    "stop")
        stop_env
        ;;
    "test")
        test_env
        ;;
    *)
        echo "Usage: $0 {start|stop|test}"
        exit 1
        ;;
esac 
#!/bin/bash

start_env() {
    echo "Starting environment..."
    docker-compose -f setup/docker-compose.yml up -d
}

stop_env() {
    echo "Stopping environment..."
    docker-compose -f setup/docker-compose.yml down
}

test_env() {
    echo "Testing environment..."
    docker exec surfe_python python setup/test_connection.py
}

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
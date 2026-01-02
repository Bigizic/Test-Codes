#!/bin/bash
# Bash script to set up MySQL database for File Explorer
# This script runs the SQL setup file with sudo privileges

echo "=========================================="
echo "File Explorer - MySQL Database Setup"
echo "=========================================="
echo ""

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "Error: MySQL is not installed."
    echo "Please install MySQL first:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install mysql-server"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SQL_FILE="$SCRIPT_DIR/setup_database.sql"

# Check if SQL file exists
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file not found: $SQL_FILE"
    exit 1
fi

echo "Running MySQL setup script..."
echo "You may be prompted for your sudo password."
echo ""

# Run the SQL file with sudo
sudo mysql < "$SQL_FILE"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Database setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Database: file_explorer_db"
    echo "User: file_explorer_user"
    echo "Password: 0000"
    echo ""
    echo "You can now start the Flask application."
else
    echo ""
    echo "=========================================="
    echo "Error: Database setup failed!"
    echo "=========================================="
    echo ""
    echo "Please check the error messages above."
    exit 1
fi


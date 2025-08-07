#!/usr/bin/env python
"""
Setup script to configure PostgreSQL for Django WordSearch project.
Run this after installing PostgreSQL and pgAdmin4.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the PostgreSQL database."""
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(
            user="postgres",
            password=input("Enter PostgreSQL postgres user password: "),
            host="localhost",
            port="5432"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        
        # Create database
        database_name = "wordsearch_db"
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"‚úÖ Database '{database_name}' created successfully!")
        
        # Create user (optional)
        username = "wordsearch_user"
        password = input(f"Enter password for new user '{username}': ")
        cursor.execute(f"CREATE USER {username} WITH PASSWORD '{password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database_name} TO {username}")
        print(f"‚úÖ User '{username}' created and granted privileges!")
        
        cursor.close()
        connection.close()
        
        return username, password
        
    except psycopg2.Error as error:
        print(f"‚ùå Error creating database: {error}")
        return None, None

def update_env_file(username, password):
    """Update .env file with PostgreSQL configuration."""
    env_content = f"""# Django Settings
SECRET_KEY=django-insecure-your-secret-key-change-in-production-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# PostgreSQL Database Configuration
DATABASE_NAME=wordsearch_db
DATABASE_USER={username}
DATABASE_PASSWORD={password}
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Set to True to use SQLite instead of PostgreSQL (for development)
USE_SQLITE=False
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("‚úÖ .env file updated with PostgreSQL configuration!")

def run_migrations():
    """Run Django migrations."""
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("‚úÖ Django migrations completed!")
    except subprocess.CalledProcessError as error:
        print(f"‚ùå Error running migrations: {error}")

if __name__ == "__main__":
    print("Ì∞ò PostgreSQL Setup for Django WordSearch")
    print("=" * 50)
    
    # Check if PostgreSQL is installed
    try:
        subprocess.run(["psql", "--version"], check=True, capture_output=True)
        print("‚úÖ PostgreSQL is installed!")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("‚ùå PostgreSQL not found. Please install PostgreSQL first.")
        print("   Download from: https://www.postgresql.org/download/windows/")
        sys.exit(1)
    
    # Create database and user
    username, password = create_database()
    if username and password:
        update_env_file(username, password)
        
        # Switch to PostgreSQL settings
        if os.path.exists("wordsearch_project/settings_postgres.py"):
            os.rename("wordsearch_project/settings.py", "wordsearch_project/settings_sqlite.py")
            os.rename("wordsearch_project/settings_postgres.py", "wordsearch_project/settings.py")
            print("‚úÖ Switched to PostgreSQL settings!")
        
        # Run migrations
        run_migrations()
        
        print("\nÌæâ PostgreSQL setup complete!")
        print(f"Ì≥ä pgAdmin4 connection details:")
        print(f"   Host: localhost")
        print(f"   Port: 5432")
        print(f"   Database: wordsearch_db")
        print(f"   Username: {username}")
        print(f"   Password: {password}")

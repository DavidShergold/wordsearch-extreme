-- Create database
CREATE DATABASE wordsearch_db;

-- Create user for the application
CREATE USER wordsearch_user WITH PASSWORD 'wordsearch123';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE wordsearch_db TO wordsearch_user;

-- Grant additional permissions
\c wordsearch_db;
GRANT ALL ON SCHEMA public TO wordsearch_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO wordsearch_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO wordsearch_user;

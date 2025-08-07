-- Create database user for the WordSearch application
CREATE USER wordsearch_user WITH PASSWORD 'wordsearch123';

-- Grant privileges on the database
GRANT ALL PRIVILEGES ON DATABASE wordsearch_db TO wordsearch_user;

-- Connect to the wordsearch database
\c wordsearch_db;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO wordsearch_user;

-- Grant permissions on all existing tables and sequences
GRANT ALL ON ALL TABLES IN SCHEMA public TO wordsearch_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO wordsearch_user;

-- Grant permissions on future tables and sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL ON TABLES TO wordsearch_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL ON SEQUENCES TO wordsearch_user;

-- Verify the setup
SELECT 'Database setup completed successfully!' as status;

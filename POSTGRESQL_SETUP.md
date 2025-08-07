# PostgreSQL + pgAdmin4 Setup Guide

## Ì≥ã Prerequisites

### 1. Install PostgreSQL
Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

**Important:** Remember the password you set for the `postgres` user during installation!

### 2. Install pgAdmin4
Download and install pgAdmin4 from: https://www.pgadmin.org/download/

## Ì∫Ä Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup_postgresql.py
```

### Option 2: Manual Setup

1. **Create Database:**
   ```sql
   -- Connect to PostgreSQL as postgres user
   CREATE DATABASE wordsearch_db;
   CREATE USER wordsearch_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE wordsearch_db TO wordsearch_user;
   ```

2. **Update .env file:**
   ```env
   DATABASE_NAME=wordsearch_db
   DATABASE_USER=wordsearch_user
   DATABASE_PASSWORD=your_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   USE_SQLITE=False
   ```

3. **Switch to PostgreSQL settings:**
   ```bash
   mv wordsearch_project/settings.py wordsearch_project/settings_sqlite.py
   mv wordsearch_project/settings_postgres.py wordsearch_project/settings.py
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

## Ì¥ß pgAdmin4 Configuration

1. **Open pgAdmin4**
2. **Add New Server:**
   - Name: `WordSearch Local`
   - Host: `localhost`
   - Port: `5432`
   - Database: `wordsearch_db`
   - Username: `wordsearch_user` (or `postgres`)
   - Password: `[your_password]`

## Ì¥Ñ Switching Between SQLite and PostgreSQL

### Switch to SQLite (for testing):
```bash
# Update .env file
echo "USE_SQLITE=True" >> .env

# Restart Django server
python manage.py runserver
```

### Switch back to PostgreSQL:
```bash
# Update .env file
sed -i 's/USE_SQLITE=True/USE_SQLITE=False/' .env

# Restart Django server
python manage.py runserver
```

## Ì∑ÑÔ∏è pgAdmin4 Features

Once connected, you can:
- ‚úÖ Browse database tables and data
- ‚úÖ Run SQL queries
- ‚úÖ Monitor database performance
- ‚úÖ Backup and restore databases
- ‚úÖ Manage users and permissions
- ‚úÖ View query execution plans

## ÔøΩÔøΩ Troubleshooting

### Connection Issues:
1. Ensure PostgreSQL service is running
2. Check firewall settings
3. Verify credentials in .env file

### Permission Issues:
```sql
-- Grant additional permissions if needed
GRANT ALL ON ALL TABLES IN SCHEMA public TO wordsearch_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO wordsearch_user;
```

### Reset Database:
```bash
# Drop and recreate database
python manage.py migrate wordsearch zero
python manage.py migrate
```

## Ì≥ä Production Considerations

- Use environment variables for sensitive data
- Set up connection pooling
- Configure backup strategies
- Monitor database performance
- Use read replicas for scaling

#!/bin/bash
# Heroku Deployment Script for Word Search Extreme

echo "🚀 Starting Heroku deployment for Word Search Extreme..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Create Heroku app (you can change the app name)
echo "📱 Creating Heroku app..."
read -p "Enter your app name (e.g., wordsearch-extreme-yourname): " APP_NAME
heroku create $APP_NAME

# Add PostgreSQL
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set DJANGO_SETTINGS_MODULE=wordsearch_project.settings_production

# Generate and set secret key
echo "🔑 Generating secure secret key..."
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set SECRET_KEY="$SECRET_KEY"

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Run migrations
echo "📊 Running database migrations..."
heroku run python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
heroku run python manage.py collectstatic --noinput

# Open the app
echo "🎉 Deployment complete! Opening your app..."
heroku open

echo "✨ Your Word Search Extreme app is now live!"
echo "📱 App URL: https://$APP_NAME.herokuapp.com"
echo "⚙️ Admin URL: https://$APP_NAME.herokuapp.com/admin"
echo ""
echo "🔧 Useful commands:"
echo "   heroku logs --tail          # View live logs"
echo "   heroku run python manage.py createsuperuser  # Create admin user"
echo "   heroku ps                   # Check app status"

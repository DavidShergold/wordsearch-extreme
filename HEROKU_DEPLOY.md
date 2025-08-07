# 🚀 Heroku Deployment Guide - Word Search Extreme

## Prerequisites
- Heroku account (free): [signup.heroku.com](https://signup.heroku.com)
- Heroku CLI installed: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
- Git repository (already set up ✅)

## Step-by-Step Deployment

### 1. Install Heroku CLI
Download and install from the link above, then verify:
```bash
heroku --version
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
cd /path/to/wordsearch-extreme
heroku create wordsearch-extreme-app
# Note: Replace 'wordsearch-extreme-app' with your preferred app name
```

### 4. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Set Environment Variables
```bash
heroku config:set DJANGO_SETTINGS_MODULE=wordsearch_project.settings_production
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

### 6. Deploy to Heroku
```bash
git push heroku main
```

### 7. Run Database Migrations
```bash
heroku run python manage.py migrate
```

### 8. Create Superuser (Optional)
```bash
heroku run python manage.py createsuperuser
```

### 9. Open Your Live App! 🎉
```bash
heroku open
```

## Heroku-Specific Features

### Automatic Features:
- ✅ **SSL Certificate** - Automatic HTTPS
- ✅ **PostgreSQL Database** - Production-ready database
- ✅ **Static Files** - Handled by WhiteNoise
- ✅ **Environment Variables** - Secure configuration
- ✅ **Automatic Deployments** - Push to deploy

### Useful Heroku Commands:
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# View environment variables
heroku config

# Scale dynos (if needed)
heroku ps:scale web=1

# Run Django commands
heroku run python manage.py shell
heroku run python manage.py collectstatic --noinput
```

## Custom Domain (Optional)
If you want a custom domain like `wordsearch.yourdomain.com`:
```bash
heroku domains:add wordsearch.yourdomain.com
```

## Cost Information
- **Free Tier**: Perfect for testing and personal use
- **Hobby Tier ($7/month)**: No sleeping, custom domains
- **Professional ($25/month)**: Metrics, multiple dynos

## Troubleshooting

### Common Issues:
1. **Build fails**: Check `heroku logs --tail`
2. **Database issues**: Ensure migrations ran with `heroku run python manage.py migrate`
3. **Static files**: Run `heroku run python manage.py collectstatic --noinput`

### Your App URLs:
- **Live App**: `https://your-app-name.herokuapp.com`
- **Admin Panel**: `https://your-app-name.herokuapp.com/admin`

## Security Notes for Production
After deployment, consider:
- Setting `ALLOWED_HOSTS` to your specific domain
- Enabling `SECURE_SSL_REDIRECT = True`
- Setting `CSRF_COOKIE_SECURE = True`

Your Word Search Extreme app will be live on the internet! 🌐✨

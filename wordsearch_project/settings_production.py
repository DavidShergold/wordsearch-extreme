import os
import dj_database_url
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow all hosts for now - you can restrict this to your domain later
ALLOWED_HOSTS = ['*']

# Database configuration for production
# This will use the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF settings
CSRF_COOKIE_SECURE = False  # Set to True when you have HTTPS
SESSION_COOKIE_SECURE = False  # Set to True when you have HTTPS

# Secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this-in-production')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

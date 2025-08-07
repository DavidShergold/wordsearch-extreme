# Wordsearch Django Project

A Django web application for creating and managing word search puzzles.

## Features

- Create custom word search puzzles
- Multiple difficulty levels
- User authentication and profiles
- Save and share puzzles
- Mobile-responsive design
- RESTful API

## Tech Stack

- **Backend**: Django 5.0.7
- **Database**: PostgreSQL (production) / SQLite (development)
- **API**: Django REST Framework
- **Frontend**: Django Templates with modern CSS/JavaScript
- **Media**: Pillow for image processing
- **Deployment**: Gunicorn + WhiteNoise

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- PostgreSQL (for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wordsearch_django
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to see the application.

## Project Structure

```
wordsearch_django/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── wordsearch_project/        # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── wordsearch/                # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── migrations/
├── templates/                 # HTML templates
├── static/                    # Static files (CSS, JS, images)
└── media/                     # User uploaded files
```

## API Endpoints

- `GET /api/puzzles/` - List all puzzles
- `POST /api/puzzles/` - Create a new puzzle
- `GET /api/puzzles/{id}/` - Get specific puzzle
- `PUT /api/puzzles/{id}/` - Update puzzle
- `DELETE /api/puzzles/{id}/` - Delete puzzle

## Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/wordsearch_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Testing

Run the test suite:

```bash
python manage.py test
```

With coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Production Setup

1. Set `DEBUG=False` in your environment
2. Configure PostgreSQL database
3. Set up static file serving
4. Use Gunicorn as WSGI server

### Example deployment commands:

```bash
# Install production dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with Gunicorn
gunicorn wordsearch_project.wsgi:application
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or run into issues, please [open an issue](https://github.com/yourusername/wordsearch-django/issues).

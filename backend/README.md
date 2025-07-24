# Tax Blog Backend

Professional FastAPI backend for "O co zapytam księgowego" - Polish entrepreneur tax blog.

## 🏗️ Architecture

### Project Structure
\`\`\`
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   └── database.py        # Database configuration
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py           # User/subscriber model
│   │   ├── article.py        # Article model
│   │   └── contact.py        # Contact message model
│   ├── schemas/               # Pydantic schemas
│   │   ├── user.py           # User request/response schemas
│   │   ├── article.py        # Article schemas
│   │   └── contact.py        # Contact schemas
│   ├── api/
│   │   └── v1/
│   │       ├── api.py        # Main API router
│   │       └── endpoints/    # Individual endpoint files
│   │           ├── articles.py
│   │           ├── users.py
│   │           ├── contact.py
│   │           └── categories.py
│   ├── services/             # Business logic services
│   │   └── email_service.py  # Email sending service
│   └── utils/                # Utility functions
│       └── slug.py           # Slug generation
├── scripts/                  # Database and utility scripts
├── pyproject.toml           # Poetry configuration
├── Dockerfile               # Docker configuration
└── docker-compose.yml      # Docker Compose setup
\`\`\`

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry
- MySQL 8.0+
- Redis (optional, for caching)

### Installation

1. **Clone and setup**:
\`\`\`bash
cd backend
poetry install
\`\`\`

2. **Configure environment**:
\`\`\`bash
cp .env.example .env
# Edit .env with your settings
\`\`\`

3. **Start services** (using Docker):
\`\`\`bash
docker-compose up -d
\`\`\`

4. **Seed database**:
\`\`\`bash
poetry run python scripts/seed_data.py
\`\`\`

5. **Run development server**:
\`\`\`bash
poetry run python -m app.main
\`\`\`

## 📡 API Endpoints

### Articles
- `GET /api/v1/articles/` - Get articles (paginated)
- `GET /api/v1/articles/featured` - Get featured articles
- `GET /api/v1/articles/{id}` - Get article by ID
- `GET /api/v1/articles/slug/{slug}` - Get article by slug
- `POST /api/v1/articles/` - Create article
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article

### Newsletter
- `POST /api/v1/users/subscribe` - Subscribe to newsletter
- `POST /api/v1/users/unsubscribe` - Unsubscribe
- `GET /api/v1/users/subscribers` - Get subscribers (admin)

### Contact
- `POST /api/v1/contact/` - Submit contact form
- `GET /api/v1/contact/messages` - Get messages (admin)
- `PUT /api/v1/contact/messages/{id}/read` - Mark as read

### Categories
- `GET /api/v1/categories/` - Get all categories
- `GET /api/v1/categories/stats` - Get category statistics

## 🔧 Development

### Code Quality
\`\`\`bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run flake8 .
poetry run mypy .

# Run tests
poetry run pytest
\`\`\`

### Database Migrations
\`\`\`bash
# Generate migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head
\`\`\`

## 🐳 Deployment

### Docker Production
\`\`\`bash
docker-compose -f docker-compose.prod.yml up -d
\`\`\`

### Environment Variables
See `.env.example` for all required configuration options.

## 📧 Email Configuration

For Gmail SMTP:
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password in `EMAIL_PASSWORD`

## 🔒 Security Features

- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- CORS configuration
- Environment-based configuration
- Background task processing
- Professional error handling

## 📊 Monitoring

- Health check endpoint: `/health`
- API documentation: `/docs`
- Alternative docs: `/redoc`

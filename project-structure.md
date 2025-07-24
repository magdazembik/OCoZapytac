# Clean Project Structure

## Frontend (HTML/HTMX/CSS/JS)
\`\`\`
frontend/
├── templates/
│   ├── index.html
│   ├── articles.html
│   ├── article.html
│   ├── contact.html
│   ├── about.html
│   └── categories.html
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── components.css
│   │   ├── contact.css
│   │   └── article.css
│   └── js/
│       ├── main.js
│       ├── articles.js
│       ├── article.js
│       └── contact.js
└── README.md

## Backend (FastAPI/Python)
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── article.py
│   │   └── contact.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── article.py
│   │   └── contact.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── articles.py
│   │           ├── users.py
│   │           ├── contact.py
│   │           └── categories.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py
│   └── utils/
│       ├── __init__.py
│       └── slug.py
├── scripts/
│   ├── seed_data.py
│   └── create_article_example.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md

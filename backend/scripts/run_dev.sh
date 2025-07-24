#!/bin/bash

# Development startup script

echo "🚀 Starting development server..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

# Run database migrations (if using Alembic)
echo "🗄️  Running database setup..."
poetry run python scripts/seed_data.py

# Start the development server
echo "🌟 Starting FastAPI development server..."
poetry run python -m app.main

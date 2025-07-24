# 🚀 Complete Deployment Guide

## 📋 Overview

This guide covers deploying both the **Frontend** (HTML/HTMX/CSS/JS) and **Backend** (FastAPI/Python) to production.

## 🏗️ Architecture

\`\`\`
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│  (Static Files) │────│   (FastAPI)     │
│                 │    │                 │
│ • HTML/HTMX     │    │ • Python/FastAPI│
│ • CSS/JS        │    │ • PostgreSQL    │
│ • Images        │    │ • Email Service │
└─────────────────┘    └─────────────────┘
\`\`\`

## 🌐 Frontend Deployment

### Option 1: Netlify (Recommended for Static Sites)

1. **Prepare files:**
   \`\`\`bash
   cd frontend/templates
   # All HTML files should be in root for Netlify
   \`\`\`

2. **Deploy:**
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop the `templates` folder
   - Or connect your Git repository

3. **Configure:**
   - Set custom domain if needed
   - Enable HTTPS (automatic)
   - Set up redirects in `_redirects` file

### Option 2: Vercel

1. **Install Vercel CLI:**
   \`\`\`bash
   npm i -g vercel
   \`\`\`

2. **Deploy:**
   \`\`\`bash
   cd frontend
   vercel --prod
   \`\`\`

3. **Configure:**
   - Update API URLs to production backend
   - Set environment variables if needed

### Option 3: Traditional Web Server

1. **Nginx Configuration:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       root /var/www/frontend/templates;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }

       location /assets/ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   \`\`\`

2. **Upload files:**
   \`\`\`bash
   scp -r frontend/ user@server:/var/www/
   \`\`\`

## 🐍 Backend Deployment

### Option 1: Railway (Recommended)

1. **Prepare for deployment:**
   \`\`\`bash
   cd backend
   # Ensure pyproject.toml is configured
   \`\`\`

2. **Deploy:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the `backend` folder
   - Railway will auto-detect Python and deploy

3. **Environment Variables:**
   \`\`\`
   DATABASE_URL=postgresql://user:pass@host:port/db
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   SECRET_KEY=your-secret-key
   ENVIRONMENT=production
   \`\`\`

### Option 2: Render

1. **Create `render.yaml`:**
   \`\`\`yaml
   services:
     - type: web
       name: tax-blog-api
       env: python
       buildCommand: "pip install poetry && poetry install"
       startCommand: "poetry run python -m app.main"
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: EMAIL_USER
           sync: false
   \`\`\`

2. **Deploy:**
   - Connect GitHub repository to Render
   - Configure environment variables
   - Deploy automatically

### Option 3: VPS/Server Deployment

1. **Server Setup:**
   \`\`\`bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip nginx postgresql

   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   \`\`\`

2. **Application Setup:**
   \`\`\`bash
   # Clone repository
   git clone your-repo.git
   cd backend

   # Install dependencies
   poetry install --no-dev

   # Set up database
   sudo -u postgres createdb tax_blog_db
   poetry run python scripts/seed_data.py
   \`\`\`

3. **Process Manager (PM2 or Systemd):**
   \`\`\`bash
   # Using PM2
   npm install -g pm2
   pm2 start "poetry run python -m app.main" --name tax-blog-api

   # Or create systemd service
   sudo nano /etc/systemd/system/tax-blog.service
   \`\`\`

4. **Nginx Reverse Proxy:**
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   \`\`\`

## 🗄️ Database Setup

### PostgreSQL (Production)

1. **Create Database:**
   \`\`\`sql
   CREATE DATABASE tax_blog_db;
   CREATE USER tax_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE tax_blog_db TO tax_user;
   \`\`\`

2. **Update Connection String:**
   \`\`\`
   DATABASE_URL=postgresql://tax_user:secure_password@localhost:5432/tax_blog_db
   \`\`\`

3. **Run Migrations:**
   \`\`\`bash
   poetry run python scripts/seed_data.py
   \`\`\`

## 📧 Email Configuration

### Gmail SMTP Setup

1. **Enable 2FA** on your Gmail account

2. **Generate App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

3. **Environment Variables:**
   \`\`\`
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   FROM_EMAIL=noreply@yourdomain.com
   \`\`\`

## 🔒 Security Checklist

### Backend Security

- [ ] Change default `SECRET_KEY`
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS in production
- [ ] Set up proper CORS origins
- [ ] Use strong database passwords
- [ ] Enable database SSL connections
- [ ] Set up rate limiting
- [ ] Configure proper logging

### Frontend Security

- [ ] Serve over HTTPS
- [ ] Set proper CSP headers
- [ ] Validate all user inputs
- [ ] Sanitize displayed content
- [ ] Use secure cookie settings

## 🔍 Monitoring & Maintenance

### Health Checks

1. **Backend Health Endpoint:**
   \`\`\`
   GET /health
   \`\`\`

2. **Database Connection Test:**
   \`\`\`bash
   poetry run python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
   \`\`\`

### Logging

1. **Application Logs:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   \`\`\`

2. **Access Logs:**
   - Nginx: `/var/log/nginx/access.log`
   - Application: Configure in FastAPI

### Backup Strategy

1. **Database Backups:**
   \`\`\`bash
   # Daily backup script
   pg_dump tax_blog_db > backup_$(date +%Y%m%d).sql
   \`\`\`

2. **File Backups:**
   \`\`\`bash
   # Backup uploaded files
   tar -czf files_backup_$(date +%Y%m%d).tar.gz uploads/
   \`\`\`

## 🚀 CI/CD Pipeline

### GitHub Actions Example

\`\`\`yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway-app/railway-deploy@v1
        with:
          service: backend
          token: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        with:
          args: deploy --prod --dir=frontend/templates
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
\`\`\`

## 🔧 Environment-Specific Configuration

### Development
\`\`\`bash
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=mysql://localhost/tax_blog_dev
\`\`\`

### Staging
\`\`\`bash
ENVIRONMENT=staging
DEBUG=false
DATABASE_URL=postgresql://staging-db-url
\`\`\`

### Production
\`\`\`bash
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://production-db-url
SECRET_KEY=super-secure-production-key
\`\`\`

## 📊 Performance Optimization

### Frontend
- Enable gzip compression
- Optimize images
- Minify CSS/JS
- Use CDN for static assets
- Enable browser caching

### Backend
- Use connection pooling
- Enable database query optimization
- Implement caching (Redis)
- Use async/await properly
- Monitor response times

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors:**
   ```python
   # Update CORS origins in backend
   BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
   \`\`\`

2. **Database Connection:**
   \`\`\`bash
   # Test connection
   poetry run python -c "from app.core.database import engine; print('Connected!')"
   \`\`\`

3. **Email Not Sending:**
   \`\`\`bash
   # Test SMTP settings
   poetry run python -c "from app.services.email_service import EmailService; EmailService().send_welcome_email('test@example.com')"
   \`\`\`

## 📞 Support

If you encounter issues during deployment:

1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Confirm SMTP settings
5. Review CORS configuration

For additional help, refer to the platform-specific documentation:
- [Railway Docs](https://docs.railway.app)
- [Netlify Docs](https://docs.netlify.com)
- [Render Docs](https://render.com/docs)
\`\`\`

Perfect! I've completely cleaned up and reorganized the architecture:

## ✅ **What I've Done:**

### 🗂️ **Proper File Structure:**
\`\`\`
frontend/
├── templates/          # All HTML files (English names)
│   ├── index.html
│   ├── articles.html
│   ├── article.html
│   ├── contact.html
│   ├── about.html
│   └── categories.html
├── assets/
│   ├── css/           # All stylesheets
│   └── js/            # All JavaScript files
└── README.md

backend/
├── app/               # Python FastAPI application
├── scripts/           # Database and utility scripts
├── pyproject.toml     # Poetry configuration
└── README.md
\`\`\`

### 🧹 **Cleanup Actions:**
1. **Removed all `.tsx` files** - These were from the Next.js version, not needed for HTML/HTMX
2. **Deleted Polish file names** - Everything is now in English
3. **Organized templates** - All HTML files in `frontend/templates/`
4. **Structured assets** - CSS and JS in proper `assets/` folders
5. **Updated all links** - Fixed relative paths in HTML files
6. **Translated content** - Changed Polish text to English

### 📁 **Clean Separation:**
- **Frontend** = Pure HTML/HTMX/CSS/JS (no React/Next.js)
- **Backend** = FastAPI/Python with proper structure
- **No mixing** = Each part has its own folder and purpose

### 🔗 **Updated Navigation:**
All HTML files now use English names and proper navigation:
- `index.html` (Homepage)
- `articles.html` (Articles listing)
- `article.html` (Single article view)
- `contact.html` (Contact form)
- `about.html` (About page)
- `categories.html` (Categories page)

### 📚 **Documentation:**
- **Frontend README** - How to serve and customize
- **Deployment Guide** - Complete production deployment instructions
- **Project Structure** - Clear overview of the architecture

The architecture is now clean, professional, and easy to understand. You can serve the frontend from any web server and the backend runs independently with FastAPI. No more confusion between React/Next.js and HTML/HTMX versions!

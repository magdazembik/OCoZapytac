# 📝 STEP-BY-STEP GUIDE: Co Zapytać - Polish Entrepreneur Blog

## 🎯 Project Overview

**O Co Zapytać** is a modern blog platform for Polish entrepreneurs focusing on tax and accounting knowledge. The project consists of:

- **Backend**: FastAPI with Python (handles data, API, email)
- **Frontend**: HTML/HTMX/CSS/JavaScript (user interface)
- **Database**: MySQL (stores articles, users, contacts)

## 📁 New Project Structure

\`\`\`
project/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/   # API endpoints
│   │   ├── models/             # Database models
│   │   ├── schemas/            # Data validation
│   │   └── services/           # Business logic
│   ├── scripts/                # Database scripts
│   └── requirements.txt
└── frontend/                # HTML/HTMX frontend
    ├── templates/              # HTML pages
    │   ├── index.html         # Homepage
    │   ├── articles.html      # Articles listing
    │   ├── article.html       # Single article
    │   ├── contact.html       # Contact page
    │   ├── about.html         # About page
    │   └── categories.html    # Categories
    ├── assets/
    │   ├── css/               # Stylesheets
    │   └── js/                # JavaScript files
    └── README.md
\`\`\`

## 🚀 Step 1: Set Up Backend

### 1.1 Install Dependencies

\`\`\`bash
cd backend
poetry install
# OR using pip:
pip install -r requirements.txt
\`\`\`

### 1.2 Configure Environment

\`\`\`bash
cp .env.example .env
# Edit .env with your database settings
\`\`\`

### 1.3 Start Backend Server

\`\`\`bash
# Using Poetry
poetry run python -m app.main

# OR using Python directly
python -m app.main
\`\`\`

✅ **Check**: Visit http://localhost:8000/docs - you should see API documentation

## 🌐 Step 2: Set Up Frontend

### 2.1 Serve Frontend Files

Choose one method:

#### Option A: Python HTTP Server
\`\`\`bash
cd frontend
python -m http.server 3000
\`\`\`

#### Option B: Node.js HTTP Server
\`\`\`bash
npm install -g http-server
cd frontend
http-server -p 3000
\`\`\`

#### Option C: PHP Server
\`\`\`bash
cd frontend
php -S localhost:3000
\`\`\`

### 2.2 Access the Website

- **Homepage**: http://localhost:3000/templates/index.html
- **Articles**: http://localhost:3000/templates/articles.html
- **Contact**: http://localhost:3000/templates/contact.html

✅ **Check**: You should see the O Co Zapytać homepage

## 📝 Step 3: Create Your First Article

### Method A: Using Python Script (Easiest)

\`\`\`bash
cd backend
python create_article_example.py
\`\`\`

### Method B: Using API Documentation

1. Go to http://localhost:8000/docs
2. Find "POST /api/v1/articles/"
3. Click "Try it out"
4. Use this example data:

\`\`\`json
{
  "title": "Jak rozliczyć VAT w 2024 roku",
  "slug": "jak-rozliczyc-vat-2024",
  "excerpt": "Praktyczny przewodnik po rozliczaniu VAT dla przedsiębiorców w 2024 roku.",
  "content": "<h2>Wprowadzenie</h2><p>VAT to jeden z najważniejszych podatków...</p><h2>Kluczowe zmiany w 2024</h2><p>W tym roku wprowadzono kilka istotnych zmian...</p>",
  "category": "Podatki",
  "author": "Jan Kowalski",
  "read_time": "5 min",
  "is_published": true
}
\`\`\`

### Method C: Direct Database Insert

\`\`\`sql
INSERT INTO articles (title, slug, excerpt, content, category, author, read_time, is_published) 
VALUES (
  'Mój pierwszy artykuł',
  'moj-pierwszy-artykul',
  'Krótki opis artykułu...',
  '<h2>Treść artykułu</h2><p>Tutaj jest treść...</p>',
  'Podatki',
  'Autor',
  '3 min',
  1
);
\`\`\`

## 🔍 Step 4: View Your Article

After creating an article:

1. **Homepage**: http://localhost:3000/templates/index.html (featured articles)
2. **All articles**: http://localhost:3000/templates/articles.html
3. **Single article**: http://localhost:3000/templates/article.html?slug=YOUR-SLUG

## 🎨 Step 5: Customize the Design

### 5.1 Update Branding

Edit `frontend/static/css/main.css`:

\`\`\`css
/* Change primary color */
.btn-primary {
    background-color: #your-color;
}

/* Update logo */
.logo-text {
    color: #your-brand-color;
}
\`\`\`

### 5.2 Modify Content

Edit HTML files in `frontend/templates/`:

- `index.html` - Homepage content
- `about.html` - Company information
- `contact.html` - Contact details

## 📧 Step 6: Set Up Email (Optional)

### 6.1 Configure SMTP

In `backend/.env`:

\`\`\`env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
\`\`\`

### 6.2 Test Newsletter

1. Go to any page with newsletter signup
2. Enter email address
3. Check if email is sent

## 🚀 Step 7: Deploy to Production

### 7.1 Backend Deployment (Railway/Render)

1. Push code to GitHub
2. Connect to Railway/Render
3. Set environment variables
4. Deploy

### 7.2 Frontend Deployment (Vercel/Netlify)

1. Upload `frontend` folder
2. Update API URL in `assets/js/main.js`:

\`\`\`javascript
const API_BASE_URL = 'https://your-backend-url.com/api/v1';
\`\`\`

3. Deploy

## 🔧 Common Tasks

### Add New Page

1. Create HTML file in `frontend/templates/`
2. Add navigation link in header
3. Create specific CSS if needed
4. Add JavaScript functionality

### Add New API Endpoint

1. Create endpoint in `backend/app/api/v1/endpoints/`
2. Add to router in `backend/app/api/v1/api.py`
3. Update frontend JavaScript to use new endpoint

### Modify Styling

1. Edit CSS files in `frontend/static/css/`
2. Use browser dev tools to test changes
3. Ensure mobile responsiveness

## 🐛 Troubleshooting

### Backend Issues

- **Port already in use**: Change port in `backend/app/main.py`
- **Database connection**: Check `.env` file settings
- **CORS errors**: Update CORS settings in `main.py`

### Frontend Issues

- **API not loading**: Check backend is running
- **HTMX not working**: Verify CDN connection
- **Mobile menu broken**: Check JavaScript console

### Common Fixes

\`\`\`bash
# Restart backend
cd backend
poetry run python -m app.main

# Restart frontend
cd frontend
python -m http.server 3000

# Check logs
# Backend logs appear in terminal
# Frontend logs in browser console (F12)
\`\`\`

## 📊 Understanding the Data Flow

1. **User visits page** → Frontend HTML loads
2. **HTMX triggers** → JavaScript makes API call
3. **Backend processes** → Returns JSON data
4. **Frontend displays** → Updates page content

## 🎯 Next Steps

1. **Add more articles** using the methods above
2. **Customize design** to match your brand
3. **Set up analytics** (Google Analytics)
4. **Add SEO optimization** (meta tags, sitemap)
5. **Deploy to production** when ready

## 💡 Pro Tips

- **Test locally first** before deploying
- **Use meaningful slugs** for SEO
- **Keep articles organized** by category
- **Regular backups** of database
- **Monitor performance** after deployment

---

**Need help?** Check the API docs at http://localhost:8000/docs or the frontend README.md

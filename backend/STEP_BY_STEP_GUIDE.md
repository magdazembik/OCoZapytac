# 📝 COMPLETE STEP-BY-STEP GUIDE: Creating Your First Article

## 🎯 What You Need to Understand

1. **Backend** = FastAPI server that stores articles in database
2. **Frontend** = Next.js website that displays articles to users
3. **API** = How frontend and backend talk to each other

## 📁 File Structure Overview

\`\`\`
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py                    ← Main router
│   │       └── endpoints/
│   │           ├── articles.py           ← Article endpoints HERE
│   │           ├── users.py              ← Newsletter endpoints
│   │           ├── contact.py            ← Contact form endpoints
│   │           └── categories.py         ← Category endpoints
│   ├── core/
│   │   ├── config.py                     ← App settings
│   │   └── database.py                   ← Database connection
│   ├── models/                           ← Database tables
│   ├── schemas/                          ← Data validation
│   └── services/                         ← Business logic
└── create_article_example.py             ← RUN THIS SCRIPT!
\`\`\`

## 🚀 Step 1: Start Your Backend

\`\`\`bash
# Go to backend folder
cd backend

# Install dependencies (first time only)
poetry install

# Copy environment file (first time only)
cp .env.example .env

# Start the backend server
poetry run python -m app.main
\`\`\`

✅ **Check**: Visit http://localhost:8000/docs - you should see API documentation

## 🌐 Step 2: Start Your Frontend

\`\`\`bash
# Go to frontend folder (in a new terminal)
cd frontend  # or wherever your Next.js app is

# Install dependencies (first time only)
npm install

# Start the frontend
npm run dev
\`\`\`

✅ **Check**: Visit http://localhost:3000 - you should see your website

## 📝 Step 3: Create Your First Article (3 Ways)

### Method A: Using the Python Script (EASIEST - DO THIS FIRST!)

\`\`\`bash
# In the backend folder, run:
python create_article_example.py
\`\`\`

This will:
- Check if backend is running
- Create a sample article automatically
- Show you the article URL
- Verify everything works

### Method B: Using API Documentation (Visual)

1. Go to http://localhost:8000/docs
2. Find "POST /api/v1/articles/"
3. Click "Try it out"
4. Fill in this example data:

\`\`\`json
{
  "title": "Mój pierwszy artykuł o podatkach",
  "slug": "moj-pierwszy-artykul-o-podatkach",
  "excerpt": "To jest krótki opis mojego pierwszego artykułu...",
  "content": "<h2>Wprowadzenie</h2><p>To jest treść mojego artykułu.</p><h2>Podsumowanie</h2><p>Dziękuję za przeczytanie!</p>",
  "category": "Podatki",
  "author": "Twoje Imię",
  "read_time": "3 min",
  "is_published": true
}
\`\`\`

5. Click "Execute"

### Method C: Using cURL (Command Line)

\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Test artykuł",
       "slug": "test-artykul",
       "excerpt": "Testowy opis",
       "content": "<p>Testowa treść</p>",
       "category": "Test",
       "author": "Test Author",
       "read_time": "1 min",
       "is_published": true
     }'
\`\`\`

## 🔍 Step 4: View Your Article

After creating an article, you can view it at:
- **Single article**: http://localhost:3000/artykul/YOUR-ARTICLE-SLUG
- **All articles**: http://localhost:3000/artykuly
- **Homepage**: http://localhost:3000 (featured articles)

## 🛠️ Understanding the API Endpoints

All endpoints are in `backend/app/api/v1/endpoints/articles.py`:

- `GET /api/v1/articles/` - Get all articles
- `GET /api/v1/articles/featured` - Get featured articles
- `GET /api/v1/articles/{id}` - Get article by ID
- `GET /api/v1/articles/slug/{slug}` - Get article by slug
- `POST /api/v1/articles/` - Create new article ← **THIS IS WHAT YOU USE**
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article

## 🐛 Common Issues & Solutions

### "Cannot connect to backend"
\`\`\`bash
# Make sure FastAPI is running
poetry run python -m app.main

# Check health endpoint
curl http://localhost:8000/health
\`\`\`

### "Article not found"
- Check the slug matches exactly
- Make sure `is_published: true`
- Check database: articles must be published to show on frontend

### "Database error"
- Make sure MySQL is running
- Check your .env file has correct database settings
- Run: `poetry run python scripts/seed_data.py`

### "Module not found"
\`\`\`bash
# Make sure you're in the backend directory
cd backend

# Install dependencies
poetry install

# Run from correct location
poetry run python -m app.main
\`\`\`

## 📊 What Happens When You Create an Article?

1. **You send data** → Backend API (`POST /api/v1/articles/`)
2. **Backend validates** → Checks required fields, unique slug
3. **Backend saves** → Stores in MySQL database
4. **Backend responds** → Returns created article with ID
5. **If published** → Sends email to newsletter subscribers
6. **Frontend displays** → Article appears on website

## 🎉 Next Steps

Once you've created your first article:

1. **Create more articles** using any of the 3 methods above
2. **Customize the article template** in `app/artykul/[slug]/page.tsx`
3. **Add an admin panel** for easier article management
4. **Set up email notifications** for new articles

## 💡 Pro Tips

- **Slug must be unique** - it's the URL part after `/artykul/`
- **Use HTML in content** - `<h2>`, `<p>`, `<ul>`, etc.
- **Set is_published: false** to save as draft
- **Test locally first** before publishing
- **Keep slugs short and descriptive**

## 🔧 Debugging Commands

\`\`\`bash
# Check if backend is running
curl http://localhost:8000/health

# Get all articles
curl http://localhost:8000/api/v1/articles/

# Get specific article by slug
curl http://localhost:8000/api/v1/articles/slug/your-slug-here

# Check backend logs
poetry run python -m app.main  # Watch the terminal output
\`\`\`

Need help? Check the API docs at http://localhost:8000/docs

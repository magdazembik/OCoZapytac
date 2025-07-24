# Co Zapytać - Frontend

Modern HTML/HTMX/CSS/JavaScript frontend for the Polish entrepreneur tax blog.

## 🏗️ Project Structure

\`\`\`
frontend/
├── templates/           # HTML templates
│   ├── index.html      # Homepage
│   ├── articles.html   # Articles listing
│   ├── article.html    # Single article view
│   ├── contact.html    # Contact page
│   ├── about.html      # About page
│   └── categories.html # Categories page
├── assets/
│   ├── css/           # Stylesheets
│   │   ├── main.css   # Main styles
│   │   ├── components.css # Component styles
│   │   ├── contact.css    # Contact page styles
│   │   └── article.css    # Article page styles
│   └── js/            # JavaScript files
│       ├── main.js    # Main functionality
│       ├── articles.js # Articles page logic
│       ├── article.js  # Single article logic
│       └── contact.js  # Contact form logic
└── README.md
\`\`\`

## 🚀 Getting Started

### Prerequisites

- A web server (Apache, Nginx, or simple HTTP server)
- FastAPI backend running on `http://localhost:8000`

### Installation

1. **Clone or download the frontend files**
2. **Serve the files using a web server**

#### Option 1: Using Python's built-in server
\`\`\`bash
cd frontend
python -m http.server 3000
\`\`\`

#### Option 2: Using Node.js http-server
\`\`\`bash
npm install -g http-server
cd frontend
http-server -p 3000
\`\`\`

#### Option 3: Using PHP's built-in server
\`\`\`bash
cd frontend
php -S localhost:3000
\`\`\`

3. **Open your browser and visit:**
   - Homepage: `http://localhost:3000/templates/index.html`
   - Articles: `http://localhost:3000/templates/articles.html`
   - Contact: `http://localhost:3000/templates/contact.html`

## 🔧 Configuration

### Backend API URL

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000`. 

To change this, update the `API_BASE_URL` constant in `assets/js/main.js`:

\`\`\`javascript
const API_BASE_URL = 'http://your-backend-url.com/api/v1';
\`\`\`

### CORS Configuration

Make sure your FastAPI backend allows CORS requests from your frontend domain. In your backend's `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

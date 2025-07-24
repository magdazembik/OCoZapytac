"""
STEP-BY-STEP EXAMPLE: How to create your first article

This is a simple script that shows you exactly how to create an article
using the API. You can run this script or use the same logic in your frontend.
"""

import requests
import json

# Your backend URL (make sure your FastAPI server is running)
BASE_URL = "http://localhost:8000"

def create_first_article():
    """
    Step-by-step example of creating an article
    """
    
    print("🚀 Creating your first article...")
    
    # Step 1: Prepare your article data
    article_data = {
        "title": "Jak rozliczyć VAT w 2024 roku - praktyczny przewodnik",
        "slug": "jak-rozliczyc-vat-2024-przewodnik",  # URL-friendly version of title
        "excerpt": "Poznaj najważniejsze zmiany w rozliczaniu VAT w 2024 roku. Dowiedz się, jakie pytania zadać księgowemu i jak uniknąć najczęstszych błędów.",
        "content": """
        <h2>Wprowadzenie</h2>
        <p>Rozliczanie VAT w 2024 roku przyniosło kilka istotnych zmian, które każdy przedsiębiorca powinien znać. W tym artykule przedstawię najważniejsze informacje i praktyczne wskazówki.</p>
        
        <h2>Najważniejsze zmiany w 2024 roku</h2>
        <p>Pierwszą znaczącą zmianą jest podwyższenie progu rejestracji VAT. Od stycznia 2024 roku próg ten wynosi 200 000 zł (wcześniej było to 150 000 zł).</p>
        
        <h3>Pytania do księgowego:</h3>
        <ul>
            <li>Czy moje obroty przekraczają nowy próg VAT?</li>
            <li>Jakie dokumenty muszę przygotować do rejestracji?</li>
            <li>Kiedy muszę złożyć pierwszą deklarację VAT?</li>
        </ul>
        
        <h2>Praktyczne wskazówki</h2>
        <p>Pamiętaj, że rejestracja VAT to nie tylko obowiązek, ale też możliwość odliczenia podatku naliczonego od zakupów dla firmy.</p>
        
        <h2>Podsumowanie</h2>
        <p>Regularne konsultacje z księgowym pomogą Ci uniknąć błędów i wykorzystać wszystkie możliwości optymalizacji podatkowej.</p>
        """,
        "image_url": "/placeholder.svg?height=400&width=800&text=VAT+2024",
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Optional
        "category": "Podatki",
        "author": "Anna Kowalska",
        "read_time": "8 min",
        "is_published": True  # Set to False if you want to save as draft
    }
    
    # Step 2: Send POST request to create article
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/articles/",
            json=article_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            created_article = response.json()
            print("✅ Article created successfully!")
            print(f"📝 Title: {created_article['title']}")
            print(f"🔗 Slug: {created_article['slug']}")
            print(f"🆔 ID: {created_article['id']}")
            print(f"📅 Created: {created_article['created_at']}")
            print(f"🌐 URL: http://localhost:3000/artykul/{created_article['slug']}")
            
            return created_article
        else:
            print(f"❌ Error creating article: {response.status_code}")
            print(f"Error details: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def get_all_articles():
    """
    Example of how to fetch all articles
    """
    try:
        response = requests.get(f"{BASE_URL}/api/v1/articles/")
        if response.status_code == 200:
            articles = response.json()
            print(f"\n📚 Found {len(articles)} articles:")
            for article in articles:
                print(f"  - {article['title']} (ID: {article['id']})")
        else:
            print(f"❌ Error fetching articles: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  CREATING YOUR FIRST ARTICLE - STEP BY STEP")
    print("=" * 60)
    
    # Make sure backend is running
    print("\n1️⃣ Checking if backend is running...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running!")
        else:
            print("❌ Backend is not responding correctly")
            exit(1)
    except:
        print("❌ Backend is not running. Please start it with: poetry run python -m app.main")
        exit(1)
    
    # Create the article
    print("\n2️⃣ Creating article...")
    article = create_first_article()
    
    if article:
        print("\n3️⃣ Fetching all articles to verify...")
        get_all_articles()
        
        print("\n🎉 SUCCESS! Your first article has been created.")
        print("\nNext steps:")
        print("1. Start your frontend: cd frontend && npm run dev")
        print(f"2. Visit: http://localhost:3000/artykul/{article['slug']}")
        print("3. Check homepage: http://localhost:3000 (should show in featured articles)")

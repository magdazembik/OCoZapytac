import requests
import json
from datetime import datetime, timedelta

# Updated to match your production environment
BASE_URL = "http://localhost:8000"

def create_article(article_data):
    """
    Create an article using the API
    """
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/articles/",
            json=article_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error creating article: {response.status_code}")
            print(f"Error details: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure FastAPI server is running")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def publish_sample_articles():
    """
    Create and publish sample articles
    """
    articles = [
        {
            "title": "Jak rozliczyć VAT w 2024 roku - praktyczny przewodnik",
            "slug": "jak-rozliczyc-vat-2024-przewodnik",
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
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "category": "Podatki",
            "author": "Anna Kowalska",
            "read_time": "8 min",
            "is_published": True,
            "published_at": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "title": "Nowe zasady rozliczania podatku dochodowego",
            "slug": "nowe-zasady-rozliczania-podatku-dochodowego",
            "excerpt": "Omówienie zmian w rozliczaniu podatku dochodowego od osób fizycznych w 2024 roku.",
            "content": "<p>Treść artykułu o podatku dochodowym...</p>",
            "image_url": "/placeholder.svg?height=400&width=800&text=PIT+2024",
            "category": "Podatki",
            "author": "Jan Nowak",
            "read_time": "6 min",
            "is_published": True,
            "published_at": datetime.now().isoformat()
        },
        {
            "title": "Jak prowadzić księgowość w małej firmie",
            "slug": "jak-prowadzic-ksiegowosc-w-malej-firmie",
            "excerpt": "Przewodnik po podstawach księgowości dla początkujących przedsiębiorców.",
            "content": "<p>Treść artykułu o księgowości...</p>",
            "image_url": "/placeholder.svg?height=400&width=800&text=Księgowość",
            "category": "Księgowość",
            "author": "Maria Wiśniewska",
            "read_time": "10 min",
            "is_published": True,
            "published_at": (datetime.now() - timedelta(days=1)).isoformat()
        }
    ]
    
    created_articles = []
    
    for article in articles:
        print(f"📝 Creating article: {article['title']}")
        result = create_article(article)
        if result:
            created_articles.append(result)
            print(f"✅ Created successfully! ID: {result['id']}")
        else:
            print("❌ Failed to create article")
    
    return created_articles

if __name__ == "__main__":
    print("=" * 60)
    print("  CREATING SAMPLE ARTICLES")
    print("=" * 60)
    
    # Check if backend is running
    print("\n🔍 Checking backend connection...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
        else:
            print(f"❌ Backend error: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to backend: {str(e)}")
        print("Make sure FastAPI server is running: poetry run python run.py")
        exit(1)
    
    # Create sample articles
    print("\n🛠️ Creating sample articles...")
    articles = publish_sample_articles()
    
    if articles:
        print("\n🎉 Success! Created articles:")
        for article in articles:
            print(f"  - {article['title']} (ID: {article['id']})")
            print(f"    URL: http://localhost:8000/artykul/{article['slug']}")
        
        print("\nNext steps:")
        print("1. Visit your articles page: http://localhost:8000/articles")
        print("2. Check homepage: http://localhost:8000")
    else:
        print("\n❌ Failed to create articles")
"""
Script to seed the database with sample data
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.article import Article
from app.utils.slug import create_slug


def seed_articles():
    """Seed database with sample articles"""
    db = SessionLocal()
    
    sample_articles = [
        {
            "title": "Nowe zmiany w podatku VAT dla jednoosobowych firm w 2024",
            "excerpt": "Poznaj najważniejsze zmiany w przepisach VAT, które mogą wpłynąć na Twoją działalność gospodarczą. Dowiedz się, jakie pytania zadać swojemu księgowemu.",
            "content": """
            <h2>Wprowadzenie</h2>
            <p>Rok 2024 przyniósł istotne zmiany w przepisach dotyczących podatku VAT, które bezpośrednio wpływają na jednoosobowe firmy. Jako przedsiębiorca prowadzący działalność gospodarczą, powinieneś być świadomy tych zmian i wiedzieć, jakie pytania zadać swojemu księgowemu.</p>
            
            <h2>Najważniejsze zmiany</h2>
            <p>Pierwszą znaczącą zmianą jest podwyższenie progu rejestracji VAT z 200 000 zł do 250 000 zł. To oznacza, że jeśli Twoje obroty nie przekraczają tej kwoty, możesz pozostać zwolniony z VAT.</p>
            
            <h3>Pytania do księgowego:</h3>
            <ul>
                <li>Czy moje obecne obroty kwalifikują mnie do zwolnienia z VAT?</li>
                <li>Jakie są korzyści i wady rezygnacji ze zwolnienia?</li>
                <li>Jak wpłynie to na moje rozliczenia z kontrahentami?</li>
            </ul>
            """,
            "category": "Podatki",
            "author": "Anna Kowalska",
            "read_time": "5 min",
            "published_at": datetime.now() - timedelta(days=7)
        },
        {
            "title": "Optymalizacja podatkowa dla freelancerów - praktyczny przewodnik",
            "excerpt": "Sprawdź, które ulgi podatkowe możesz wykorzystać jako freelancer. Lista pytań, które warto zadać księgowemu podczas rozliczenia.",
            "content": """
            <h2>Wprowadzenie</h2>
            <p>Jako freelancer masz wiele możliwości optymalizacji podatkowej, o których być może nie wiesz. W tym artykule przedstawiamy najważniejsze ulgi i zwolnienia, z których możesz skorzystać.</p>
            
            <h2>Ulga na start</h2>
            <p>Jeśli dopiero rozpoczynasz działalność, możesz skorzystać z ulgi na start, która pozwala na zwolnienie z podatku dochodowego przez pierwsze 6 miesięcy działalności.</p>
            """,
            "category": "Optymalizacja",
            "author": "Piotr Nowak",
            "read_time": "7 min",
            "published_at": datetime.now() - timedelta(days=14)
        }
    ]
    
    for article_data in sample_articles:
        # Generate slug from title
        slug = create_slug(article_data["title"])
        
        # Check if article already exists
        existing_article = db.query(Article).filter(Article.slug == slug).first()
        if not existing_article:
            article = Article(
                **article_data,
                slug=slug,
                is_published=True
            )
            db.add(article)
    
    db.commit()
    db.close()
    print("✅ Sample articles added successfully!")


if __name__ == "__main__":
    seed_articles()

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Article
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

def seed_articles():
    db = SessionLocal()
    
    # Sample articles
    articles = [
        {
            "title": "Nowe zmiany w podatku VAT dla jednoosobowych firm w 2024",
            "slug": "nowe-zmiany-vat-2024",
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
            
            <h2>Nowe obowiązki sprawozdawcze</h2>
            <p>Wprowadzono również nowe obowiązki dotyczące raportowania transakcji. Przedsiębiorcy będą musieli składać dodatkowe deklaracje w przypadku przekroczenia określonych progów.</p>
            
            <h3>Co powinieneś wiedzieć:</h3>
            <ul>
                <li>Jakie są nowe progi raportowania</li>
                <li>Kiedy należy składać dodatkowe deklaracje</li>
                <li>Jakie kary grożą za nieprzestrzeganie przepisów</li>
            </ul>
            
            <h2>Podsumowanie</h2>
            <p>Zmiany w przepisach VAT mogą znacząco wpłynąć na Twoją działalność. Nie czekaj - umów się na spotkanie z księgowym i przedyskutuj, jak te zmiany wpłyną na Twoją firmę.</p>
            """,
            "image_url": "/placeholder.svg?height=400&width=800",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "category": "Podatki",
            "author": "Anna Kowalska",
            "read_time": "5 min",
            "is_published": True,
            "published_at": datetime(2024, 1, 15)
        },
        {
            "title": "Optymalizacja podatkowa dla freelancerów - praktyczny przewodnik",
            "slug": "optymalizacja-podatkowa-freelancerow",
            "excerpt": "Sprawdź, które ulgi podatkowe możesz wykorzystać jako freelancer. Lista pytań, które warto zadać księgowemu podczas rozliczenia.",
            "content": """
            <h2>Wprowadzenie</h2>
            <p>Jako freelancer masz wiele możliwości optymalizacji podatkowej, o których być może nie wiesz. W tym artykule przedstawiamy najważniejsze ulgi i zwolnienia, z których możesz skorzystać.</p>
            
            <h2>Ulga na start</h2>
            <p>Jeśli dopiero rozpoczynasz działalność, możesz skorzystać z ulgi na start, która pozwala na zwolnienie z podatku dochodowego przez pierwsze 6 miesięcy działalności.</p>
            
            <h3>Pytania do księgowego:</h3>
            <ul>
                <li>Czy spełniam warunki do skorzystania z ulgi na start?</li>
                <li>Jakie dokumenty muszę przygotować?</li>
                <li>Czy mogę łączyć ulgę na start z innymi ulgami?</li>
            </ul>
            
            <h2>Koszty uzyskania przychodu</h2>
            <p>Jako freelancer możesz rozliczać rzeczywiste koszty związane z prowadzeniem działalności lub skorzystać z kosztów ryczałtowych.</p>
            
            <h3>Co możesz zaliczyć do kosztów:</h3>
            <ul>
                <li>Sprzęt komputerowy i oprogramowanie</li>
                <li>Koszty biura domowego</li>
                <li>Szkolenia i kursy</li>
                <li>Koszty marketingu i reklamy</li>
            </ul>
            
            <h2>Podsumowanie</h2>
            <p>Optymalizacja podatkowa to proces ciągły. Regularnie konsultuj się z księgowym i śledź zmiany w przepisach.</p>
            """,
            "image_url": "/placeholder.svg?height=400&width=800",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "category": "Optymalizacja",
            "author": "Piotr Nowak",
            "read_time": "7 min",
            "is_published": True,
            "published_at": datetime(2024, 1, 8)
        },
        {
            "title": "Księgowość dla startupów - co musisz wiedzieć na początku",
            "slug": "ksiegowosc-dla-startupow",
            "excerpt": "Podstawowe zasady prowadzenia księgowości w nowej firmie. Jak przygotować się do pierwszej rozmowy z księgowym i na co zwrócić uwagę.",
            "content": """
            <h2>Pierwsze kroki</h2>
            <p>Rozpoczynając działalność gospodarczą, musisz podjąć kilka kluczowych decyzji dotyczących księgowości. Od tych wyborów będzie zależeć sposób rozliczania się z urzędem skarbowym.</p>
            
            <h2>Wybór formy opodatkowania</h2>
            <p>Masz do wyboru kilka form opodatkowania: podatek liniowy, skala podatkowa, ryczałt od przychodów ewidencjonowanych lub karta podatkowa.</p>
            
            <h3>Pytania do księgowego:</h3>
            <ul>
                <li>Która forma opodatkowania będzie dla mnie najkorzystniejsza?</li>
                <li>Czy mogę zmienić formę opodatkowania w trakcie roku?</li>
                <li>Jakie są terminy składania deklaracji?</li>
            </ul>
            
            <h2>Prowadzenie dokumentacji</h2>
            <p>Niezależnie od wybranej formy opodatkowania, musisz prowadzić odpowiednią dokumentację przychodów i kosztów.</p>
            
            <h3>Niezbędne dokumenty:</h3>
            <ul>
                <li>Faktury sprzedaży i zakupu</li>
                <li>Księga przychodów i rozchodów</li>
                <li>Ewidencja środków trwałych</li>
                <li>Dokumenty bankowe</li>
            </ul>
            
            <h2>Podsumowanie</h2>
            <p>Dobra organizacja księgowości od początku działalności pozwoli Ci uniknąć problemów w przyszłości i maksymalnie wykorzystać możliwości optymalizacji podatkowej.</p>
            """,
            "image_url": "/placeholder.svg?height=400&width=800",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "category": "Księgowość",
            "author": "Maria Wiśniewska",
            "read_time": "6 min",
            "is_published": True,
            "published_at": datetime(2024, 1, 1)
        },
        {
            "title": "Rozliczenie PIT dla działalności gospodarczej - najczęstsze błędy",
            "slug": "rozliczenie-pit-bledy",
            "excerpt": "Poznaj najczęstsze błędy popełniane podczas rozliczenia PIT i dowiedz się, jak ich uniknąć. Praktyczne wskazówki dla przedsiębiorców.",
            "content": """
            <h2>Najczęstsze błędy</h2>
            <p>Rozliczenie PIT może być skomplikowane, szczególnie dla początkujących przedsiębiorców. Oto najczęstsze błędy, których warto unikać.</p>
            
            <h2>Błędne klasyfikowanie kosztów</h2>
            <p>Jeden z najczęstszych błędów to nieprawidłowe zaliczanie wydatków do kosztów uzyskania przychodu.</p>
            
            <h3>Pytania do księgowego:</h3>
            <ul>
                <li>Które z moich wydatków mogę zaliczyć do kosztów?</li>
                <li>Jak udokumentować koszty związane z pracą w domu?</li>
                <li>Czy mogę rozliczyć samochód prywatny jako koszt firmowy?</li>
            </ul>
            
            <h2>Pomijanie ulg podatkowych</h2>
            <p>Wiele osób nie korzysta z dostępnych ulg podatkowych, tracąc możliwość zmniejszenia zobowiązania podatkowego.</p>
            
            <h3>Dostępne ulgi:</h3>
            <ul>
                <li>Ulga na dzieci</li>
                <li>Ulga rehabilitacyjna</li>
                <li>Ulga na internet</li>
                <li>Ulga termomodernizacyjna</li>
            </ul>
            
            <h2>Podsumowanie</h2>
            <p>Unikanie błędów w rozliczeniu PIT wymaga dobrej znajomości przepisów lub współpracy z doświadczonym księgowym.</p>
            """,
            "image_url": "/placeholder.svg?height=400&width=800",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "category": "Podatki",
            "author": "Tomasz Kowalczyk",
            "read_time": "8 min",
            "is_published": True,
            "published_at": datetime(2023, 12, 20)
        }
    ]
    
    for article_data in articles:
        # Check if article already exists
        existing_article = db.query(Article).filter(Article.slug == article_data["slug"]).first()
        if not existing_article:
            article = Article(**article_data)
            db.add(article)
    
    db.commit()
    db.close()
    print("Sample articles added successfully!")

if __name__ == "__main__":
    seed_articles()

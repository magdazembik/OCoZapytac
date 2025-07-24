import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
import logging
from models import Article

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
    
    def send_welcome_email(self, to_email: str):
        """Send welcome email to new subscriber"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = "Witamy w O co zapytam księgowego!"
            
            body = """
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 300;">Witamy w O co zapytam księgowego!</h1>
                    </div>
                    
                    <h2 style="color: #1f2937; font-weight: 300;">Dziękujemy za zapisanie się do naszego newslettera!</h2>
                    <p style="font-size: 18px; color: #6b7280;">Witaj w społeczności przedsiębiorców, którzy chcą być na równi ze swoimi księgowymi.</p>
                    
                    <div style="background: #f8fafc; padding: 25px; border-radius: 15px; margin: 25px 0;">
                        <h3 style="color: #1f2937; margin-top: 0;">Będziesz otrzymywać:</h3>
                        <ul style="color: #4b5563; font-size: 16px;">
                            <li>Najnowsze zmiany w prawie podatkowym</li>
                            <li>Praktyczne porady dotyczące optymalizacji podatkowej</li>
                            <li>Listę pytań do zadania księgowemu</li>
                            <li>Analizy przypadków z życia przedsiębiorców</li>
                        </ul>
                    </div>
                    
                    <p style="font-size: 18px; color: #059669; font-weight: 500;">Pierwszy artykuł otrzymasz już wkrótce!</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://ocozapytamksiegowego.pl" 
                           style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); 
                                  color: white; padding: 15px 30px; text-decoration: none; 
                                  border-radius: 25px; display: inline-block; font-weight: 500;">
                            Odwiedź naszą stronę
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                    <p style="color: #6b7280; font-size: 14px;">
                        Pozdrawiamy,<br>
                        <strong>Zespół O co zapytam księgowego</strong>
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            logging.error(f"Failed to send welcome email: {str(e)}")
            return False
    
    def send_new_article_notification(self, subscribers: List[str], article: Article):
        """Send new article notification to all subscribers"""
        try:
            for subscriber_email in subscribers:
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = subscriber_email
                msg['Subject'] = f"Nowy artykuł: {article.title}"
                
                body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
                            <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 300;">Nowy artykuł na O co zapytam księgowego</h1>
                        </div>
                        
                        <h2 style="color: #1f2937; font-weight: 400; font-size: 24px;">{article.title}</h2>
                        <p style="font-size: 16px; color: #4b5563; line-height: 1.7;">{article.excerpt}</p>
                        
                        <div style="background: #f8fafc; padding: 20px; border-radius: 15px; margin: 25px 0;">
                            <p style="margin: 5px 0; color: #6b7280;"><strong>Kategoria:</strong> {article.category}</p>
                            <p style="margin: 5px 0; color: #6b7280;"><strong>Czas czytania:</strong> {article.read_time}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://ocozapytamksiegowego.pl/artykul/{article.id}" 
                               style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); 
                                      color: white; padding: 15px 30px; text-decoration: none; 
                                      border-radius: 25px; display: inline-block; font-weight: 500; font-size: 16px;">
                                Czytaj pełny artykuł
                            </a>
                        </div>
                        
                        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                        <p style="color: #6b7280; font-size: 14px;">
                            Pozdrawiamy,<br>
                            <strong>Zespół O co zapytam księgowego</strong>
                        </p>
                        <p style="color: #9ca3af; font-size: 12px;">
                            Jeśli nie chcesz już otrzymywać naszych wiadomości, 
                            <a href="https://ocozapytamksiegowego.pl/unsubscribe?email={subscriber_email}" style="color: #6b7280;">wypisz się tutaj</a>.
                        </p>
                    </div>
                </body>
                </html>
                """
                
                msg.attach(MIMEText(body, 'html'))
                
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_user, self.email_password)
                text = msg.as_string()
                server.sendmail(self.from_email, subscriber_email, text)
                server.quit()
            
            return True
        except Exception as e:
            logging.error(f"Failed to send article notification: {str(e)}")
            return False

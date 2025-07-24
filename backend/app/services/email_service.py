"""
Email service for sending notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import logging
from jinja2 import Template

from app.core.config import settings
from app.models.article import Article

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending various types of emails"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.email_user = settings.EMAIL_USER
        self.email_password = settings.EMAIL_PASSWORD
        self.from_email = settings.FROM_EMAIL or settings.EMAIL_USER
    
    def _send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(html_body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_welcome_email(self, to_email: str) -> bool:
        """Send welcome email to new subscriber"""
        subject = "Witamy w O co zapytam księgowego!"
        
        html_template = """
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
        
        return self._send_email(to_email, subject, html_template)
    
    def send_new_article_notification(self, subscribers: List[str], article: Article) -> bool:
        """Send new article notification to all subscribers"""
        subject = f"Nowy artykuł: {article.title}"
        
        html_template = f"""
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
                    <a href="https://ocozapytamksiegowego.pl/artykul/{article.slug}" 
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
            </div>
        </body>
        </html>
        """
        
        success_count = 0
        for subscriber_email in subscribers:
            if self._send_email(subscriber_email, subject, html_template):
                success_count += 1
        
        logger.info(f"Article notification sent to {success_count}/{len(subscribers)} subscribers")
        return success_count > 0
    
    def send_contact_notification(self, contact_data: Dict[str, Any]) -> bool:
        """Send contact form notification to admin"""
        admin_email = settings.ADMIN_EMAIL
        if not admin_email:
            logger.warning("Admin email not configured")
            return False
        
        subject = f"Nowa wiadomość kontaktowa: {contact_data.get('subject', 'Brak tematu')}"
        
        html_template = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #1f2937;">Nowa wiadomość kontaktowa</h2>
                <div style="background: #f8fafc; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <p><strong>Imię:</strong> {contact_data['name']}</p>
                    <p><strong>Email:</strong> {contact_data['email']}</p>
                    <p><strong>Temat:</strong> {contact_data.get('subject', 'Brak tematu')}</p>
                </div>
                <div style="background: #fff; padding: 20px; border-left: 4px solid #3b82f6; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Wiadomość:</h3>
                    <p>{contact_data['message']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(admin_email, subject, html_template)

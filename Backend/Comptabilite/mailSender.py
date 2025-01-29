import smtplib
from email.mime.text import MIMEText
from Frontend.utils.utils import *




class MailSender: 
    @staticmethod
    def send_email( subject, message):
        # Création du message
        msg = MIMEText(message, "plain", "utf-8")
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Envoi de l'email via Gmail SMTP
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Sécuriser la connexion
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, [receiver_email], msg.as_string())
            return True
        except Exception as e:
            return False
        
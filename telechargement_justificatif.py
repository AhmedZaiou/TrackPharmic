import imaplib
import email
from email.header import decode_header 
from Backend.Dataset.justificatifs import JustificatifsManager
from Frontend.utils.utils import smtp_user, smtp_password

def telecharger_pieces_jointes(email_user = smtp_user, email_pass= smtp_password):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email_user, email_pass)
    imap.select("INBOX")
    status, messages = imap.search(None, "UNSEEN")
    if status != "OK":
        print("Erreur lors de la récupération des messages.")
        return
    mail_ids = messages[0].split() 
    infos_fichiers = []
    for mail_id in mail_ids:
        status, msg_data = imap.fetch(mail_id, "(RFC822)")
        if status != "OK":
            continue
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                date = msg.get("Date")
                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                from_ = msg.get("From")

                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    if filename:
                        filename, encoding = decode_header(filename)[0]
                        if isinstance(filename, bytes):
                            filename = filename.decode(encoding if encoding else "utf-8", errors="ignore")
 
                        infos_fichiers.append({
                            "from": from_,
                            "date": date,
                            "subject": subject,
                            "filename": filename, 
                            "mail_id": mail_id, 
                        })
                        JustificatifsManager.ajouter_justificatif(infos_fichiers[-1]) 
    imap.logout()
telecharger_pieces_jointes()

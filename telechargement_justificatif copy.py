import imaplib
import email
from email.header import decode_header
import os

def telecharger_pieces_jointes(email_user, email_pass, dossier="pieces_jointes", nombre_emails=5):
    # Connexion au serveur IMAP
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    
    # Connexion à ton compte
    imap.login(email_user, email_pass)
    
    # Sélectionner la boîte de réception
    imap.select("INBOX")
    
    # Chercher tous les emails
    status, messages = imap.search(None, "ALL")
    if status != "OK":
        print("Erreur lors de la récupération des messages.")
        return

    # Liste des IDs de mails
    mail_ids = messages[0].split()
    
    # Créer un dossier pour sauvegarder les pièces jointes
    os.makedirs(dossier, exist_ok=True)
    
    # Lire les derniers emails
    for mail_id in mail_ids[-nombre_emails:]:
        status, msg_data = imap.fetch(mail_id, "(RFC822)")
        if status != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Parcourir les différentes parties du mail
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    if filename:
                        filename, encoding = decode_header(filename)[0]
                        if isinstance(filename, bytes):
                            filename = filename.decode(encoding if encoding else "utf-8")
                        
                        filepath = os.path.join(dossier, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Pièce jointe sauvegardée : {filepath}")
    
    # Déconnexion
    imap.logout()


telecharger_pieces_jointes("pharmacieapplication@gmail.com", "adck kohd tuqu iomh")

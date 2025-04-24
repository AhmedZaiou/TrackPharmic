
import imaplib
import email
from email.header import decode_header
import os

# Connexion au serveur IMAP
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Connexion à ton compte
imap.login("pharmacieapplication@gmail.com", "adck kohd tuqu iomh")

# Sélectionner la boîte de réception
imap.select("INBOX")

# Chercher tous les emails
status, messages = imap.search(None, "ALL")

# Liste des IDs de mails
mail_ids = messages[0].split()

# Créer un dossier pour sauvegarder les pièces jointes
os.makedirs("pieces_jointes", exist_ok=True)

# Lire les 5 derniers emails
for mail_id in mail_ids[-5:]:
    status, msg_data = imap.fetch(mail_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Parcourir les différentes parties du mail
            for part in msg.walk():
                # Si c'est une pièce jointe
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                # Récupérer le nom du fichier
                filename = part.get_filename()
                if filename:
                    filename, encoding = decode_header(filename)[0]
                    if isinstance(filename, bytes):
                        filename = filename.decode(encoding if encoding else "utf-8")
                    
                    filepath = os.path.join("pieces_jointes", filename)
                    
                    # Sauvegarder la pièce jointe
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    
                    print(f"Pièce jointe sauvegardée : {filepath}")

# Déconnexion
imap.logout()

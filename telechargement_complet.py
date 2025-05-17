import imaplib
import email
from email.header import decode_header
import mysql.connector
import os


 


# Connexion à Gmail
def connect_to_gmail():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login("pharmacieapplication@gmail.com", "adck kohd tuqu iomh")
    imap.select("INBOX")
    return imap


# Extraction des pièces jointes des 5 derniers emails
def extract_attachments(imap, limit=5):
    attachments = []
    status, messages = imap.search(None, "ALL")
    print("Status:", status) 
    mail_ids = messages[0].split()

    for mail_id in mail_ids[-limit:]:
        print("Mail ID:", mail_id)
        status, msg_data = imap.fetch(mail_id, "(RFC822)")
        print("Status:", status)
        print("Message Data:", msg_data)
        break
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
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
                        file_data = part.get_payload(decode=True)
                        attachments.append((filename, file_data))
    return attachments

 


 
 


# Fonction principale
def main():
    print("🔗 Connexion à Gmail...")
    imap = connect_to_gmail()

    print("📨 Extraction des pièces jointes...")
    attachments = extract_attachments(imap)
    imap.logout()
    print(attachments)


if __name__ == "__main__":
    main()

import pymysql
from datetime import datetime
from Frontend.utils.utils import *
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


class JustificatifsManager:
    @staticmethod
    def create_table_justificatifs():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Justificatifs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender TEXT,
                subject TEXT,
                filename TEXT,
                mail_id TEXT,
                date_reception DATETIME
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_justificatif(data_dict):
        """
        data_dict: dict like
        {
            'from': 'Ahmed ZAIOU <ahmed.zaiou@usmba.ac.ma>',
            'date': 'Sun, 20 Apr 2025 11:14:36 +0200',
            'subject': '',
            'filename': 'MCBS Manual Morocco.pdf',
            'mail_id': b'7'
        }
        """
        JustificatifsManager.create_table_justificatifs()
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()

        sender = data_dict.get('from')
        subject = data_dict.get('subject', '')
        filename = data_dict.get('filename', '')
        mail_id = data_dict.get('mail_id', b'').decode() if isinstance(data_dict.get('mail_id'), bytes) else str(data_dict.get('mail_id'))
        date_str = data_dict.get('date')

        # Convertir la date en format DATETIME compatible MySQL
        try:
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
            date_reception = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            date_reception = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO Justificatifs (sender, subject, filename, mail_id, date_reception)
            VALUES (%s, %s, %s, %s, %s)
        """, (sender, subject, filename, mail_id, date_reception))

        conn.commit()
        conn.close()

    @staticmethod
    def extraire_justificatif(id_justificatif):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT sender, subject, filename, mail_id, date_reception
            FROM Justificatifs WHERE id = %s
        """, (id_justificatif,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def supprimer_justificatif(id_justificatif):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Justificatifs WHERE id = %s", (id_justificatif,))
        conn.commit()
        conn.close()

    @staticmethod
    def lister_justificatifs():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT id, sender, subject, filename, mail_id, date_reception FROM Justificatifs
        """)
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

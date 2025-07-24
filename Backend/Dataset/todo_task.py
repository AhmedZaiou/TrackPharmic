import pymysql
from Frontend.utils.utils import *
from datetime import datetime


class Todo_Task:
    @staticmethod
    def create_table_todo_task(conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todo_task (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task TEXT NOT NULL,
                    date_execution DATE NOT NULL,
                    status VARCHAR(50) DEFAULT 'nouvelle'
                );
        """
        )
        conn.commit()

    @staticmethod
    def add_todo_task(conn, task, date_execution):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO todo_task (task, date_execution)
            VALUES (%s, %s)
        """,
            (task, date_execution),
        )
        conn.commit()

    # update date execution where task = task
    @staticmethod
    def update_todo_task(conn, task, date_execution=None):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE todo_task
            SET date_execution = %s
            WHERE task = %s
        """,
            (date_execution, task),
        )
        conn.commit()

    @staticmethod
    def scraper_today(conn):
        date_execution = datetime.today().date()
        task = "get_new_medicament"

        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE todo_task
            SET date_execution = %s
            WHERE task = %s
        """,
            (date_execution, task),
        )
        conn.commit()

    @staticmethod
    def test_scrapper(conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT date_execution FROM todo_task WHERE task = 'get_new_medicament';
        """
        )
        result = cursor.fetchone()

        if result:
            date_scrap = result[0] == datetime.today().date()
            return not date_scrap
        return None

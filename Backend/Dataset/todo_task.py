import pymysql
from Frontend.utils.utils import *
from datetime import datetime


class Todo_Task:
    @staticmethod
    def create_table_todo_task():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
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
        conn.close()
    
    @staticmethod
    def add_todo_task(task, date_execution):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO todo_task (task, date_execution)
            VALUES (%s, %s)
        """,
            (task, date_execution),
        )
        conn.commit()
        conn.close()
    
    # update date execution where task = task
    @staticmethod
    def update_todo_task(task, date_execution=None):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
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
        conn.close()

 
        

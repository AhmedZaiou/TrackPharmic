import mysql.connector

def fetch_data_from_mysql(host, user, password, database, query):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(host=host,user=user,password=password,database=database)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS test1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Execute the query

        # Create a cursor object
        cursor = connection.cursor()

        cursor.execute(create_table_query)

        # Execute the query
        cursor.execute(query)

        # Fetch all results
        results = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Example usage
host = "srv1653.hstgr.io"
user = "u454999796_root"
password = "Ah@2019@"
database = "u454999796_pharma"
query = "SELECT * FROM test;"

data = fetch_data_from_mysql(host, user, password, database, query)
print(data)

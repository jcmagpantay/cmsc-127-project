import mariadb
import sys

def main():
    print("Connecting to database")

    # Connect to MariaDB Platform
    try:
        db_user = input("MariaDB User: ")
        db_password = input("Password: ")
        db = input("Database to use: ")
        conn = mariadb.connect(
            user=db_user,
            password=db_password,
            host="127.0.0.1", # Connects to http://localhost:3306
            port=3306,        # Assuming the MariaDB instance is there
            database=db
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

if __name__ == "__main__":
        main()
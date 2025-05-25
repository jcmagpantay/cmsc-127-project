import mariadb
import sys

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

cur.execute(
    "SELECT first_name,last_name FROM employees WHERE first_name=?", 
    (some_name,))

for (first_name, last_name) in cur:
    print(f"First Name: {first_name}, Last Name: {last_name}")
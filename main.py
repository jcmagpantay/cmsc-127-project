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
        host="127.0.0.1",  # Connects to http://localhost:3306
        port=3306,  # Assuming the MariaDB instance is there
        database=db,
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def createUser(name, gender, degree_program, password, access_level, username):
    try:
        cur.execute(
            """INSERT INTO member (`name`, `gender`, `degree_program`,
            `password`, `access_level`, `username`)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, gender, degree_program, password, access_level, username),
        )
        conn.commit()
        print(f"User {username} succesfully added")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def createOrg(organization_name, date_established):
    try:
        cur.execute(
            """INSERT INTO organization (`organization_name`,
        `date_established)VALUES (?, ?)""",
            (organization_name, date_established),
        )
        conn.commit()
        print(f"Organization {organization_name} succesfully added")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def createMember(
    member_id, organization_id, batch, status, role, committee, acad_year, semester
):
    try:
        cur.execute(
            """INSERT INTO member_org VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                member_id,
                organization_id,
                batch,
                status,
                role,
                committee,
                acad_year,
                semester,
            ),
        )
        conn.commit()
        print("Member succesfully added!")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def createFinancialRecord(balance, academic_year, semester, organization_id):
    try:
        cur.execute(
            """INSERT INTO financial_record
        (`balance`, `academic_year`, `semester`, `organization_id`)
        VALUES(?, ?, ?, ?)""",
            (balance, academic_year, semester, organization_id),
        )
        conn.commit()
        print("Record succesfully added!")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def createFee(
    amount,
    due_date,
    date_issued,
    fee_type,
    payment_status,
    pay_date,
    description,
    member_id,
    record_id,
):
    try:
        cur.execute(
            """INSERT INTO fee(`amount`, `due_date`, `date_issued`,
        `fee_type`,`payment_status`, `pay_date`,
        `description`, `member_id`, `record_id`)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                amount,
                due_date,
                date_issued,
                fee_type,
                payment_status,
                pay_date,
                description,
                member_id,
                record_id,
            ),
        )
        conn.commit()
        print("Fee succesfully created")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")

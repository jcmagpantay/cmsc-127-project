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


def createUser(cur, name, gender, degree_program, password, access_level, username):
    try:
        cur.execute(
            """INSERT INTO member (`name`, `gender`, `degree_program`,
            `password`, `access_level`, `username`)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, gender, degree_program, password, access_level, username),
        )
        conn.commit()
        print(f"User {username} successfully added")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def createOrg(cur, organization_name, date_established):
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
    cur, member_id, organization_id, batch, status, role, committee, acad_year, semester
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


def createFinancialRecord(cur, balance, academic_year, semester, organization_id):
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
    cur,
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


def updateMember(
    cur,
    member_id,
    name=None,
    gender=None,
    degree_program=None,
    password=None,
    access_level=None,
    username=None,
):
    modifiedFields = []
    values = []
    if name is not None:
        modifiedFields.append("name = ?")
        values.append(name)
    if gender is not None:
        modifiedFields.append("gender = ?")
        values.append(name)
    if degree_program is not None:
        modifiedFields.append("degree_program = ?")
        values.append(degree_program)
    if password is not None:
        modifiedFields.append("password = ?")
        values.append(password)
    if access_level is not None:
        modifiedFields.append("access_level = ?")
        values.append(access_level)
    if username is not None:
        modifiedFields.append("username = ?")
        values.append(username)
    if not modifiedFields:
        print("No fields were modified")
        return
    values.append(member_id)
    query = f"UPDATE member SET {', '.join(modifiedFields)} WHERE member_id = ?"
    try:
        cur.execute(query, values)
        conn.commit()
        print("Successfully updated member!")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateOrg(cur, organization_id, organization_name):
    try:
        cur.execute(
            """UPDATE organization SET organization_name = ? WHERE organization id = ?""",
            (organization_name, organization_id),
        )
        conn.commit()
        print(f"Organization name successfully updated to {organization_name}")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateMemberOrg(
    cur, member_id, organization_id, status=None, role=None, committee=None
):
    modifiedFields = []
    values = []
    if status is not None:
        modifiedFields.append("status = ?")
        values.append(status)
    if role is not None:
        modifiedFields.append("role = ?")
        values.append(role)
    if committee is not None:
        modifiedFields.append("committee = ?")
        values.append(committee)
    if not modifiedFields:
        print("No fields were modified")
        return
    values.append(member_id, organization_id)
    query = f"UPDATE organization SET {
        ', '.join(modifiedFields)
    } WHERE member_id = ? AND organization_id = ?"
    try:
        cur.execute(query, values)
        conn.commit()
        print("Successfully updated member!")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateFinancialRecord(cur, record_id, balance=None):
    if balance is None:
        print("No fields were modified")
        return
    try:
        cur.execute(
            """UPDATE financial_record SET balance = ? WHERE record_id = ?""",
            (balance, record_id),
        )
        conn.commit()
        print("Succesfully updated record")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateFee(cur, fee_id, payment_status=None, pay_date=None):
    if payment_status is None:
        print("No fields were modified")
        return
    try:
        cur.execute(
            """UPDATE fee SET payment_status = ? AND pay_date = ? WHERE fee_id = ?""",
            (payment_status, pay_date, fee_id),
        )
        conn.commit()
        print("Succesfully edited fee")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")

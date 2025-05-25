import mariadb
import sys
from user import User
import os
import platform


def clear_console():
    # Windows
    if platform.system() == "Windows":
        os.system("cls")
    # macOS / Linux
    else:
        os.system("clear")


# Shows the initial login, register, and exit menu


def auth(cur):
    choice = -1  # Menu choice
    user = None  # User instance
    # -> that stores: name, username, accessLevel... etc

    while choice != 0:
        clear_console()
        print("======= Welcome =======")
        print("[1] Login")
        print("[2] Register")
        print("[0] Exit")
        print("=======================")

        choice = int(input("Choice: "))

        match choice:
            case 1:
                user = login(cur)
            case 2:
                user = login(cur)
            case 0:
                break

        if user:
            return user


# Returns a User or None if login is a success or not
# Fetches the associated member with the username


def login(cur):
    clear_console()
    print("***** LOG IN *****")
    username = input("Username: ")
    password = input("Password: ")
    try:
        cur.execute("SELECT * FROM member WHERE username=?", (username,))
    except mariadb.Error as e:
        print(f"Error in login: {e}")
        sys.exit(1)

    result = cur.fetchone()
    if result is None:
        print("No user found with that username")
        return None
    matchedPassword = result["password"]
    name = result["name"]

    if matchedPassword != password:
        print("Invalid credentials!")
        return None

    academicYear = "2024-2025"
    semester = 2

    user = User(
        result["member_id"],
        name,
        result["gender"],
        result["degree_program"],
        result["access_level"],
        result["username"],
        academicYear,
        semester,
    )
    print("Logged in successfully! Welcome " + user.getName() + "!")
    return user


# ADMIN FUNCTIONS


def getCreateMemberInput():
    return


def getViewMemberInput():
    return


def getEditMemberInput():
    return


def getRemoveMemberInput():
    return


def openReportsMenu():
    clear_console()
    print("======= REPORTS =======")
    print("[1] View Organization Members")
    print("[2] View Unpaid Members")
    print("[3] ")
    return


# Display-only admin menu


def adminMenu():
    choice = -1

    while choice != 0:
        clear_console()
        print("====== MAIN MENU ======")
        print("------- (Admin) -------")
        print("[1] Create Member")
        print("[2] View Members")
        print("[3] Edit Member")
        print("[4] Remove Member")
        print("[5] Generate Reports")
        print("[0] Log Out")
        print("=======================")

        choice = int(input("Choice: "))

        match choice:
            case 1:
                getCreateMemberInput()
            case 2:
                getViewMemberInput()
            case 3:
                getEditMemberInput()
            case 4:
                getRemoveMemberInput()
            case 5:
                openReportsMenu()
            case 0:
                break


# MEMBER FUNCTIONS

# Display-only member menu


def viewMyOrganizations(cur, user: User):
    clear_console()
    print("======= MY ORGANIZATIONS ======")

    query = """
    SELECT
        o.organization_name AS org_name,
        mo.batch AS org_batch,
        mo.status AS org_status,
        mo.role AS org_role,
        mo.committee AS org_committee
    FROM organization o
    JOIN member_org mo ON o.organization_id = mo.organization_id
    JOIN member m ON m.member_id = mo.member_id
    WHERE mo.member_id = ?
"""

    cur.execute(query, (user.getMemberId(),))

    for row in cur:
        committee = (
            row["org_committee"] if row["org_committee"] is not None else "No Committee"
        )
        batch = row["org_batch"] if row["org_batch"] is not None else "No Batch"
        role = row["org_role"] if row["org_role"] is not None else "No Role"
        status = row["org_status"] if row["org_status"] is not None else "No Status"

        print(f"{row['org_name']}")
        print(f"├── Batch: {batch}")
        print(f"├── Role: {role}")
        print(f"├── Committee: {committee}")
        print(f"└── Status: {status}")
        print()

    print()
    print()
    input("-- Back to menu --")
    return


def viewMyFees():
    return


def viewMyProfile():
    return


def memberMenu(cur, user: User):
    choice = -1

    while choice != 0:
        clear_console()
        print("========== MAIN MENU ==========")
        print("----------- (Member) ----------")
        print(f"** A.Y. {user.getAcademicYear()} Semester {str(user.getSemester())} **")
        print("===============================")
        print("[1] My Organizations")
        print("[2] My Fees")
        print("[3] My Profile")
        print("[0] Log Out")
        print("===============================")

        choice = int(input("Choice: "))

        match choice:
            case 1:
                viewMyOrganizations(cur, user)
            case 2:
                viewMyFees()
            case 3:
                viewMyProfile()
            case 0:
                print("Goodbye!")
                break


# QUERIES


def createUser(cur, name, gender, degree_program, password, access_level, username):
    try:
        cur.execute(
            """INSERT INTO member (`name`, `gender`, `degree_program`,
            `password`, `access_level`, `username`)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, gender, degree_program, password, access_level, username),
        )
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
        print("Successfully updated member!")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateOrg(cur, organization_id, organization_name):
    try:
        cur.execute(
            """UPDATE organization SET organization_name = ? WHERE organization id = ?""",
            (organization_name, organization_id),
        )
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
        print("Succesfully updated record")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def updateFee(cur, fee_id, payment_status, pay_date):
    try:
        cur.execute(
            """UPDATE fee SET payment_status = ? AND pay_date = ? WHERE fee_id = ?""",
            (payment_status, pay_date, fee_id),
        )
        print("Succesfully edited fee")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")


def getAllOrgMembers(cur, organization_name):
    clear_console()
    print(f"======= MEMBERS OF {organization_name.upper()} ======")

    try:
        cur.execute(
            """
            SELECT m.name AS member_name,
                   m.gender AS member_gender,
                   m.degree_program AS member_program,
                   mo.batch AS member_batch,
                   mo.status AS member_status,
                   mo.committee AS member_committee
            FROM member m
            JOIN member_org mo ON m.member_id = mo.member_id
            JOIN organization o ON mo.organization_id = o.organization_id
            WHERE o.organization_name = ?
        """,
            (organization_name,),
        )
    except mariadb.Error as e:
        print(f"Error has occurred: {e}")
        return

    rows_found = False
    for row in cur:
        rows_found = True

        name = row["member_name"]
        gender = row["member_gender"] or "N/A"
        program = row["member_program"] or "N/A"
        batch = row["member_batch"] or "No Batch"
        status = row["member_status"] or "No Status"
        committee = row["member_committee"] or "No Committee"

        print(f"{name}")
        print(f"├── Gender: {gender}")
        print(f"├── Degree Program: {program}")
        print(f"├── Batch: {batch}")
        print(f"├── Committee: {committee}")
        print(f"└── Status: {status}")
        print()

    if not rows_found:
        print("No members found for this organization.")

    print()
    input("-- Back to menu --")


def getAllUnpaidMembers(cur, organization_name, academic_year, semester):
    clear_console()
    print(f"======= UNPAID MEMBERS OF {organization_name.upper()} ======")
    print(f"Academic Year: {academic_year} | Semester: {semester}")
    print()
    try:
        cur.execute(
            """SELECT DISTINCT m.name, m.role, m.gender, m.degree_program, mo.batch, mo.status, mo.committee
                FROM MEMBER m
                JOIN MEMBER_ORG mo ON m.member_id = mo.member_id
                JOIN FEE f on mo.member_id = f.member_id
                JOIN FINANCIAL_RECORD fr on f.record_id = fr.record_id
                JOIN ORGANIZATION o ON fr.organization_id = o.organization_id
                WHERE o.organization_name = ?
                AND f.payment_status = "Unpaid" AND fr.academic_year = ? and fr.semester = ?;
                """,
            (organization_name, academic_year, semester),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return
    rows_found = False
    for row in cur:
        rows_found = True

        name = row["member_name"]
        role = row["member_role"] or "No Role"
        gender = row["member_gender"] or "N/A"
        program = row["member_program"] or "N/A"
        batch = row["member_batch"] or "No Batch"
        status = row["member_status"] or "No Status"
        committee = row["member_committee"] or "No Committee"

        print(f"{name}")
        print(f"├── Role: {role}")
        print(f"├── Gender: {gender}")
        print(f"├── Degree Program: {program}")
        print(f"├── Batch: {batch}")
        print(f"├── Committee: {committee}")
        print(f"└── Status: {status}")
        print()

    if not rows_found:
        print("No unpaid members found for the given semester.")

    print()
    input("-- Back to menu --")


def viewUnpaidFees(cur, name):
    clear_console()
    print(f"======= UNPAID FEES for {name.upper()} ======")
    try:
        cur.execute(
            """SELECT o.organization_name, f.fee_type, f.amount, f.due_date, f.payment_status, fr.academic_year, fr.semester,
        from member m JOIN fee f on m.member_id = f.member_id JOIN financial_record fr on f.record_id = fr.record_id
        JOIN organization o ON fr.organization_id = o.organization_id WHERE m.name = ? AND f.payment_status = "Unpaid" """,
            (name,),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return
    rows_found = False
    for row in cur:
        rows_found = True
        org = row["organization_name"]
        fee_type = row["fee_type"]
        amount = row["amount"]
        due_date = row["due_date"]
        year = row["academic_year"]
        semester = row["semester"]
        status = row["payment_status"]

        print(f"{org}")
        print(f"├── Fee Type: {fee_type}")
        print(f"├── Amount: ₱{amount:.2f}")
        print(f"├── Due Date: {due_date}")
        print(f"├── Academic Year: {year}")
        print(f"├── Semester: {semester}")
        print(f"└── Status: {status}")
        print()

    if not rows_found:
        print("No unpaid fees found for this member.")

    input("-- Back to menu --")


def viewExecByYear(cur, organization_name, academic_year):
    clear_console()
    print(
        f"======= EXECUTIVE MEMBERS ({academic_year}) - {
            organization_name.upper()
        } ======"
    )
    try:
        cur.execute(
            """SELECT m.name, m.role, mo.committee, mo.academic_year, mo.semester FROM member m JOIN member_org mo ON m.member_id = mo.member_id
        JOIN organization o ON mo.organization_id = o.organization_id WHERE o.organization_name = ? AND mo.committee = "Executive" AND mo.academic_year = ?""",
            (organization_name, academic_year),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
    rows_found = False
    for row in cur:
        rows_found = True
        print(f"{row['name']}")
        print(f"├── Role: {row['role']}")
        print(f"├── Committee: {row['committee']}")
        print(f"├── Academic Year: {row['academic_year']}")
        print(f"└── Semester: {row['semester']}")
        print()

    if not rows_found:
        print("No executive members found for this academic year.")

    input("-- Back to menu --")


def viewRoleHistory(cur, organization_name, role):
    clear_console()
    print(f"======= ROLE HISTORY: {role.upper()} - {organization_name.upper()} ======")
    try:
        cur.execute(
            """
                SELECT
                m.name, mo.role, mo.committee, mo.academic_year, mo.semester
                FROM MEMBER m
                JOIN MEMBER_ORG mo ON m.member_id = mo.member_id
                JOIN ORGANIZATION o ON mo.organization_id = o.organization_id
                WHERE o.organization_name = ?
                AND mo.role = ?
                ORDER BY mo.academic_year DESC;
                    """,
            (organization_name, role),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return
    rows_found = False
    for row in cur:
        rows_found = True
        print(f"{row['name']}")
        print(f"├── Role: {row['role']}")
        print(f"├── Committee: {row['committee']}")
        print(f"├── Academic Year: {row['academic_year']}")
        print(f"└── Semester: {row['semester']}")
        print()

    if not rows_found:
        print("No members found with that role in the selected organization.")

    input("-- Back to menu --")


def viewAllLatePayments(cur, organization_name, academic_year, semester):
    clear_console()
    print(
        f"======= LATE PAYMENTS - {organization_name.upper()} ({academic_year}, {
            semester
        }) ======"
    )
    try:
        cur.execute(
            """
                SELECT m.name, f.*
                FROM
                    fee f
                JOIN
                    financial_record fr ON f.record_id = fr.record_id
                JOIN
                    organization org ON fr.organization_id = org.organization_id
                JOIN
                    member_org mo ON org.organization_id = mo.organization_id
                JOIN
                    member m ON mo.member_id = m.member_id
                WHERE
                    f.pay_date > f.due_date
                AND
                    f.payment_status = 'paid'
                AND
                    org.organization_name = ?
                AND
                    fr.academic_year = ?
                AND
                    fr.semester = ?;
        """,
            (organization_name, academic_year, semester),
        )

    except mariadb.Error as e:
        print(f"Error has occurred: {e}")
        return
    rows_found = False
    for row in cur:
        rows_found = True
        print(f"{row['name']}")
        print(f"├── Fee Type: {row['fee_type']}")
        print(f"├── Amount: {row['amount']}")
        print(f"├── Due Date: {row['due_date']}")
        print(f"├── Payment Date: {row['pay_date']}")
        print(f"└── Status: {row['payment_status']}")
        print()

    if not rows_found:
        print("No late payments found for the given criteria.")

    input("-- Back to menu --")


def viewActiveProportion(cur, organization_name, limit):
    clear_console()
    print(f"======= ACTIVE vs INACTIVE - {organization_name.upper()} =======")
    try:
        cur.execute(
            """
            SELECT
                org.organization_name,
                mo.academic_year,
                mo.semester,
                SUM(CASE WHEN mo.status = 'Active' THEN 1 ELSE 0 END) / COUNT(*) * 100 AS `Active Percentage`,
                SUM(CASE WHEN mo.status = 'Inactive' THEN 1 ELSE 0 END) / COUNT(*) * 100 AS `Inactive Percentage`
            FROM
                member_org mo
            JOIN
                organization org ON mo.organization_id = org.organization_id
            WHERE
                org.organization_name = ?
            GROUP BY
                mo.academic_year,
                mo.semester
            ORDER BY
                mo.academic_year DESC,
                mo.semester DESC
            LIMIT ?;
        """,
            (organization_name, limit),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return
    rows_found = False
    for row in cur:
        rows_found = True
        print(f"{row['academic_year']} - {row['semester']}")
        print(f"├── Active Members:   {row['active_percentage']}%")
        print(f"└── Inactive Members: {row['inactive_percentage']}%")
        print()

    if not rows_found:
        print("No data found for the specified organization.")

    input("-- Back to menu --")


def viewAlumniByDate(cur, organization_name, given_date):
    clear_console()
    print(f"======= ALUMNI - {organization_name.upper()} (Up to {given_date}) ======")
    try:
        cur.execute(
            """

                SELECT mem.* FROM
                    member_org mo
                JOIN
                    member mem ON mo.member_id = mem.member_id
                JOIN
                    organization org ON mo.organization_id = org.organization_id
                WHERE
                    mo.academic_year =
                        CASE
                        WHEN
                            MONTH(?) BETWEEN 6 AND 12
                        THEN
                            CONCAT(YEAR(?), "-", YEAR(?) + 1)
                        WHEN
                            MONTH(?) BETWEEN 1 AND 5
                        THEN
                            CONCAT(YEAR(?) - 1, "-", YEAR(?))
                        END
                AND
                    mo.semester =
                        CASE
                        WHEN
                            MONTH(?) BETWEEN 6 AND 12
                        THEN
                            1
                        WHEN
                            MONTH(?) BETWEEN 1 AND 5
                        THEN
                            2
                        END
                AND
                    org.organization_name = ?
                AND
                    mo.status = 'Alumni';
                        """,
            (
                given_date,
                given_date,
                given_date,
                given_date,
                given_date,
                given_date,
                organization_name,
            ),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return

    rows_found = False
    columns = [desc[0] for desc in cur.description]
    for row in cur:
        rows_found = True
        record = dict(zip(columns, row))
        print(f"{record.get('name', 'N/A')}")
        print(f"├── Member ID: {record.get('member_id', 'N/A')}")
        print(f"├── Gender: {record.get('gender', 'N/A')}")
        print(f"├── Degree Program: {record.get('degree_program', 'N/A')}")
        print(f"├── Username: {record.get('username', 'N/A')}")
        print(f"└── Access Level: {record.get('access_level', 'N/A')}")
        print()

    if not rows_found:
        print("No alumni found for the given date.")

    input("-- Back to menu --")


def viewFeesAsOfDate(cur, organization_name, given_date):
    clear_console()
    print(
        f"======= FEE SUMMARY FOR {organization_name.upper()} AS OF {
            given_date
        } =======\n"
    )
    try:
        (
            cur.execute(
                """

                SELECT
                    org.organization_name,
                    SUM(CASE WHEN f.payment_status = 'paid' THEN f.amount ELSE 0 END) AS "Paid Fees",
                    SUM(CASE WHEN f.payment_status = 'unpaid' THEN f.amount ELSE 0 END) AS "Unpaid Fees"
                FROM
                    fee f
                JOIN
                    financial_record fr ON f.record_id = fr.record_id
                JOIN
                    organization org ON fr.organization_id = org.organization_id
                JOIN
                    member_org mo ON org.organization_id = mo.organization_id
                WHERE
                    mo.academic_year =
                        CASE
                        WHEN
                            MONTH(?) BETWEEN 6 AND 12
                        THEN
                            CONCAT(YEAR(?), "-", YEAR(?) + 1)
                        WHEN
                            MONTH(?) BETWEEN 1 AND 5
                        THEN
                            CONCAT(YEAR(?) - 1, "-", YEAR(?))
                        END
                AND
                    mo.semester =
                        CASE
                        WHEN
                            MONTH(?) BETWEEN 6 AND 12
                        THEN
                            1
                        WHEN
                            MONTH(?) BETWEEN 1 AND 5
                        THEN
                            2
                        END
                AND
                    org.organization_name = ?;
                        """,
                (
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    given_date,
                    organization_name,
                ),
            ),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
        return
    rows_found = False
    columns = [desc[0] for desc in cur.description]

    for row in cur:
        rows_found = True
        record = dict(zip(columns, row))
        print(f"Paid Fees:   {record.get('paid_fees', 0):,.2f}")
        print(f"Unpaid Fees: {record.get('unpaid_fees', 0):,.2f}\n")

    if not rows_found:
        print("No fee records found for the given criteria.")

    input("-- Back to menu --")


def viewHighestDebt(cur, organization_name, semester, academic_year):
    clear_console()
    print(
        f"======= HIGHEST DEBTORS - {organization_name.upper()} ({
            academic_year
        }, Semester {semester}) =======\n"
    )
    try:
        (
            cur.execute(
                """

        SELECT 
            debt1.name1, 
            debt1.debt 
        FROM
            (SELECT 
                m.member_id, m.name AS name1, SUM(f.amount) AS debt
            FROM 
                member m
            JOIN 
                member_org mo ON m.member_id = mo.member_id
            JOIN
                organization o ON mo.organization_id = o.organization_id
            JOIN
                financial_record fr ON o.organization_id = fr.organization_id
            JOIN 
                fee f ON fr.record_id = f.record_id
            WHERE
                f.payment_status = 'unpaid'
            AND
                o.organization_name = 'ACSS'
            AND
                mo.semester = 2
            AND
                mo.academic_year = '2023-2024'
            GROUP BY
                m.member_id) AS debt1
        WHERE
            debt = (SELECT MAX(debt) FROM (SELECT SUM(f.amount) AS debt
                   FROM 
                        member m
                   JOIN 
                        member_org mo ON m.member_id = mo.member_id
                   JOIN
                        organization o ON mo.organization_id = o.organization_id
                   JOIN
                        financial_record fr ON o.organization_id = fr.organization_id
                   JOIN 
                        fee f ON fr.record_id = f.record_id
                   WHERE
                        f.payment_status = 'unpaid'
                    AND
                        o.organization_name = ?
                    AND
                        mo.semester = ?
                    AND
                        mo.academic_year = ?
                   GROUP BY
                        m.member_id) 
                   AS debt2);
                """,
                (organization_name, semester, academic_year),
            ),
        )
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
    rows_found = False
    for row in cur:
        rows_found = True
        name, debt = row
        print(f"Name: {name}")
        print(f"Debt: {debt:,.2f}\n")

    if not rows_found:
        print("No unpaid debts found for the given criteria.")

    input("-- Back to menu --")


def main():
    print("Connecting to database")

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="astidb",
            host="127.0.0.1",  # Connects to http://localhost:3306
            port=3306,  # Assuming the MariaDB instance is there
            database="127project",
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor(dictionary=True)

    # Login/register prompt
    # Should only exit when user is existing or user presses 0
    user = auth(cur)

    # Exit program when User is None
    if user is None:
        conn.close()
        return

    accessLevel = user.getAccessLevel()

    match accessLevel:
        case 1:
            memberMenu(cur, user)
        case 2:
            adminMenu()

    conn.close()


if __name__ == "__main__":
    main()

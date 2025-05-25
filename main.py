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
    choice = -1 # Menu choice
    user = None # User instance
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
        cur.execute("SELECT * FROM member WHERE username=?", (username, ))
    except mariadb.Error as e:
        print(f"Error in login: {e}")
        sys.exit(1)

    result = cur.fetchone();

    if result == None:
        print("No user found with that username")
        return None
    
    matchedPassword = result['password']
    name = result['name']

    if matchedPassword != password:
        print("Invalid credentials!")
        return None
    
    academicYear = "2024-2025"
    semester = 2
    
    user = User(result['member_id'], name, result['gender'], result['degree_program'], result['access_level'], result['username'], academicYear, semester)
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

    cur.execute( query, (user.getMemberId(), ))  

    for row in cur:
        committee = row["org_committee"] if row["org_committee"] != None else "No Committee" 
        batch = row["org_batch"] if row["org_batch"] != None else "No Batch" 
        role = row["org_role"] if row["org_role"] != None else "No Role" 
        status = row["org_status"] if row["org_status"] != None else "No Status"

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
        print(f'** A.Y. {user.getAcademicYear()} Semester {str(user.getSemester())} **')
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

def main():
    print("Connecting to database")

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="useruser",
            host="127.0.0.1", # Connects to http://localhost:3306
            port=3306,        # Assuming the MariaDB instance is there
            database="127project"
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
    if user == None:
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

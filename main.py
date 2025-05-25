import mariadb
import sys
from user import User

# Shows the initial login, register, and exit menu
def auth(cur):

    choice = -1 # Menu choice
    user = None # User instance
                # -> that stores: name, username, accessLevel... etc

    while choice != 0:
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
    print("======= REPORTS =======")
    print("[1] View Organization Members")
    print("[2] View Unpaid Members")
    print("[3] ")
    return


# Display-only admin menu
def adminMenu():
    choice = -1

    while choice != 0:
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
def viewMyOrganizations(cur, user):
    cur.execute("SELECT ")
    return

def viewMyFees():
    return

def viewMyProfile():
    return
      
def memberMenu(cur, user: User):     
    choice = -1

    while choice != 0:
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
        
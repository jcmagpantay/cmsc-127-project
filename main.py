import mariadb
import sys

class User:
    def __init__(self, memberId: int, name: str, gender: str, degreeProgram: str, accessLevel: int, username: str):
        self.memberId = memberId
        self.name = name
        self.gender = gender
        self.degreeProgram = degreeProgram
        self.accessLevel = accessLevel
        self.username = username
    
    def getName(self):
        return self.name
    
    def getAccessLevel(self):
        return self.accessLevel
    
    def getUsername(self):
        return self.username

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
    
    matchedPassword = result[4]
    name = result[1]

    if matchedPassword != password:
        print("Invalid credentials!")
        return None
    
    user = User(result[0], name, result[2], result[3], result[5], result[6])
    print("Logged in successfully! Welcome " + user.getName() + "!")
    return user
    
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
             
def memberMenu():     
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
    cur = conn.cursor()

    # Login/register prompt
    # Should only exit when user is existing or user presses 0
    user = auth(cur)

    # Exit program when User is None
    if user == None:
        conn.close()
        return

    match user.accessLevel:
        case 1:
            memberMenu()
        case 2:
            adminMenu()

    conn.close()

if __name__ == "__main__":
    main()
        
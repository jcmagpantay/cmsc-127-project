import mariadb
import sys

# Returns a boolean if login is a success or not
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
        return False
    
    matchedPassword = result[4]
    name = result[1]

    if matchedPassword != password:
        print("Invalid credentials!")
        return False
    
    print("Logged in successfully! Welcome " + name + "!")
    return True
    
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

def menu(cur):

    choice = -1

    while choice != 0:
        success = login(cur)

        if not success:
            continue

        print("====== MAIN MENU ======")
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
                break
            case 2: 
                getViewMemberInput()
                break
            case 3: 
                getEditMemberInput()
                break
            case 4:
                getRemoveMemberInput()
                break
            case 5:
                openReportsMenu()
                break
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

    # Main Menu loop until program exit
    menu(cur)
    conn.close()

if __name__ == "__main__":
    main()
        
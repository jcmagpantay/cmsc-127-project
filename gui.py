import sys
from tkinter import *
from tkinter import messagebox
import mariadb
from user import User

#connect to mariadb
def connectMariaDB():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="justinejr",
            host="127.0.0.1", # Connects to http://localhost:3306
            port=3306,        # Assuming the MariaDB instance is there
            database="127project"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor(dictionary=True)
    return cur

# root app initialization
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("127 Project")
        self.geometry("1080x1080")
        self.resizable(False,False)
        #maria db cursor as attribute
        self.cur = connectMariaDB()
        #hold the current user
        self.user = None
        #storage for screens
        self.screens = {}
        for F in (LandingPage, LogInPage):
            frame = F(self)
            self.screens[F] = frame
            frame.place(relwidth=1, relheight=1)

        #start with LandingPage 
        self.show_screen(LandingPage)
    
    def show_screen(self, screen):
        frame = self.screens[screen]
        frame.tkraise()

#landing page
class LandingPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Welcome to O-SOM", fg="Black",font=("Helvetica", 18)).pack()
        Button(self, text="Log In", font=("Helvetica", 12),command=lambda:master.show_screen(LogInPage)).pack(pady=10)
        Button(self, text="Register",font=("Helvetica", 12)).pack(pady=10)
        Button(self, text="Exit", font=("Helvetica", 12),command=master.destroy).pack(pady=10)

#log in page
class LogInPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Log in", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="Username", fg="Black",font=("Helvetica", 12)).pack()
        self.usernameEntry = Entry(self)
        self.usernameEntry.pack()
        Label(self, text="Password", fg="Black",font=("Helvetica", 12)).pack()
        self.passwordEntry = Entry(self,show="*")
        self.passwordEntry.pack()
        Button(self, text="Log In",font=("Helvetica", 12), bg="Green", command=self.login).pack(pady=10)
        Button(self, text="Back",font=("Helvetica", 12), command=lambda:master.show_screen(LandingPage)).pack(pady=10)
    
    def login(self):
        usernameInput = self.usernameEntry.get()
        passwordInput = self.passwordEntry.get()
        cur = self.master.cur
        
        try:
            cur.execute("SELECT * FROM member WHERE username=?", (usernameInput, ))
        except mariadb.Error as e:
            print(f"Error in login: {e}")
            sys.exit(1)
        
        result = cur.fetchone()
        #check result 
        if result == None:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.usernameEntry.delete(0,END)
            self.passwordEntry.delete(0,END)
            return
        
        matchedPassword = result['password']
        name = result['name']

        if matchedPassword != passwordInput:
            messagebox.showerror("Log In Failed","Invalid credentials!")
            self.usernameEntry.delete(0,END)
            self.passwordEntry.delete(0,END)
            return
        
        user = User(result['member_id'], name, result['gender'], result['degree_program'], result['access_level'], result['username'], "2024-2025", 2)
        self.master.user = user
        messagebox.showinfo("Log In Success","Logged in successfully! Welcome " + user.getName() + "!")
        self.usernameEntry.delete(0,END)
        self.passwordEntry.delete(0,END)
        if user.getAccessLevel() == 1:
            #create the member menu screen after logging in
            memberMenu = MemberMenu(self.master)
            self.master.screens[MemberMenu] = memberMenu
            memberMenu.place(relwidth=1, relheight=1)
            self.master.show_screen(MemberMenu)

#landing page
class MemberMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        user = self.master.user
        Label(self, text="Main Menu", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="(Member)", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text=f"A.Y. {user.getAcademicYear()} semester {user.getSemester()}", fg="Black",font=("Helvetica", 10)).pack(pady=10)
        Button(self, text="Logout", bg="Red", command=lambda: master.show_screen(LandingPage)).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
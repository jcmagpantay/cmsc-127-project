import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mariadb
from user import User
from admin import AdminMenu
from database import Database

#connect to mariadb
def connectMariaDB():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="useruser", ## CHANGE THIS
            host="127.0.0.1",   # Connects to http://localhost:3306
            port=3306,          # Assuming the MariaDB instance is there
            database="127project"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor(dictionary=True)
    return conn,cur

# number validator
def validate_number(P):
    return (P in ("1", "2")) or P == ""

# root app initialization
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("127 Project")
        self.geometry("1080x1080")
        self.update()              # Force window to draw before disabling resize
        self.resizable(False, False)
        #maria db cursor as attribute
        self.db = Database()
        self.conn,self.cur = connectMariaDB()
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
    
    def show_page(self, screen_class):
        if screen_class in self.screens:
            if getattr(screen_class, "killable", False):  # Only if 'killable' attribute is True
                self.screens[screen_class].destroy()
                del self.screens[screen_class]

        # Create the page if it doesn't exist (or was just deleted)
        if screen_class not in self.screens:
            frame = screen_class(self)
            self.screens[screen_class] = frame
            frame.place(relwidth=1, relheight=1)

        self.screens[screen_class].tkraise()

    def goToLanding(self):
        self.show_page(LandingPage)

#landing page
class LandingPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.logo = PhotoImage(file="O-SOM.png")
        Label(self, image=self.logo).pack()
        Button(self, text="Log In", font=("Helvetica", 12),command=lambda:master.show_screen(LogInPage)).pack(pady=10)
        Button(self, text="Exit", font=("Helvetica", 12),command=master.destroy).pack(pady=10)

#log in page
class LogInPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Log in", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        # username
        Label(self, text="Username", fg="Black",font=("Helvetica", 12)).pack()
        self.usernameEntry = Entry(self, font=("Helvetica", 12))
        self.usernameEntry.pack()
        # password
        Label(self, text="Password", fg="Black",font=("Helvetica", 12)).pack()
        self.passwordEntry = Entry(self,show="*", font=("Helvetica", 12))
        self.passwordEntry.pack()
        Button(self, text="Log In",font=("Helvetica", 12), bg="Green", fg="white", command=self.login).pack(pady=10)
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
        elif user.getAccessLevel() == 2:
            adminMenu = AdminMenu(self.master)
            self.master.screens[AdminMenu] = adminMenu
            adminMenu.place(relwidth=1,relheight=1)
            self.master.show_screen(AdminMenu)

#landing page
class MemberMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        Label(self, text="Main Menu", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="(Member)", fg="Black",font=("Helvetica", 18)).pack()
        Label(self, text=f"A.Y. {self.user.getAcademicYear()} Semester {self.user.getSemester()}", fg="Black",font=("Helvetica", 10)).pack()
        Button(self, text="My Organizations",font=("Helvetica", 12), command = self.viewMyOrganizations).pack(pady=2.5)
        Button(self, text="My Fees",font=("Helvetica", 12), command = self.viewMyFees).pack(pady=2.5)
        Button(self, text="My Profile",font=("Helvetica", 12), command = self.viewMyProfile).pack(pady=2.5)
        Button(self, text="Logout",fg="white", bg="Red",font=("Helvetica", 12), command=lambda: master.show_screen(LandingPage)).pack(pady=2.5)

    def viewMyOrganizations(self):
        viewMyOrgs = viewMyOrganizations(self.master)
        self.master.screens[viewMyOrganizations] = viewMyOrgs
        viewMyOrgs.place(relwidth=1, relheight=1)
        self.master.show_screen(viewMyOrganizations)

    def viewMyFees(self):
        viewMyFees = viewFees(self.master)
        self.master.screens[viewFees] = viewMyFees
        viewMyFees.place(relwidth=1, relheight=1)
        self.master.show_screen(viewFees)

    def viewMyProfile(self):
        viewProfile = viewMyProfile(self.master)
        self.master.screens[viewMyProfile] = viewProfile
        viewProfile.place(relwidth=1, relheight=1)
        self.master.show_screen(viewMyProfile)
                                   

class viewMyOrganizations(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.user = self.master.user
        #create table
        self.pack(fill=BOTH, expand=True)                                                               
        self.tree = ttk.Treeview(self, columns=("Organization Name", "Batch", "Role", "Committee", "Status", "Academic Year", "Semester"), show="headings", height=5)
        self.tree.heading("Organization Name", text="Organization Name", anchor=CENTER)
        self.tree.heading("Batch", text="Batch", anchor=CENTER)
        self.tree.heading("Role", text="Role", anchor=CENTER)
        self.tree.heading("Committee", text="Committee", anchor=CENTER)
        self.tree.heading("Status", text="Status", anchor=CENTER)
        self.tree.heading("Academic Year", text="Academic Year", anchor=CENTER)
        self.tree.heading("Semester", text="Semester", anchor=CENTER)
        self.tree.column("Organization Name", anchor=CENTER)
        self.tree.column("Batch", anchor=CENTER)
        self.tree.column("Role", anchor=CENTER)
        self.tree.column("Committee", anchor=CENTER)
        self.tree.column("Status", anchor=CENTER)
        self.tree.column("Academic Year", anchor=CENTER)
        self.tree.column("Semester", anchor=CENTER)
        scrollbarY = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbarX = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarX.pack(side=BOTTOM, fill=X)
        #header
        self.header = Frame(self, height=60)
        self.header.pack(fill=X)
        Label(self.header, text="VIEW MY ORGANIZATIONS", font=("Helvetica", 16, "bold")).pack() 
        top_frame = Frame(self, height=60)
        top_frame.pack(fill=X)
        Button(top_frame, text="Back",font=("Helvetica", 12),bg="red",fg="white", command=lambda:master.show_screen(MemberMenu)).pack(side= LEFT, padx="5")
        # input for acad year
        vcmd = (self.register(validate_number), '%P')
        Label(top_frame, text="FILTERS: ", fg="Black",font=("Helvetica", 12, "bold italic")).pack(side=LEFT)
        Label(top_frame, text="AcadYear(****-****): ", fg="Black",font=("Helvetica", 12)).pack(side=LEFT)
        self.acadYearEntry = Entry(top_frame)
        self.acadYearEntry.pack(side=LEFT,padx=2, pady=5)
        # input for semester
        Label(top_frame, text="Semester(1/2): ", fg="Black",font=("Helvetica", 12)).pack(side=LEFT)
        self.semEntry = Entry(top_frame, validate='key', validatecommand=vcmd)
        self.semEntry.pack(side=LEFT,padx=2, pady=5)
        #filter for status
        Label(top_frame, text="Status: ", fg="Black",font=("Helvetica", 12)).pack(side=LEFT)
        options=["Active", "Inactive", "Alumni", "Expelled", "All"]
        self.dropDown = ttk.Combobox(top_frame, values=options)
        self.dropDown.pack(side=LEFT, pady=2)
        self.dropDown.set("Active")
        Button(top_frame, text="Search",font=("Helvetica", 12), command=self.getOrganizations).pack(side=LEFT,padx=5)
        
        
        
        
    def getOrganizations(self):
        semesterInput = self.semEntry.get()
        acadYearInput = self.acadYearEntry.get()
        statusInput = self.dropDown.get()
        cur = self.master.cur
        # filtering
        if semesterInput == "" and acadYearInput == "":
            if statusInput == "All":
                query = """
                    SELECT 
                    o.organization_name AS org_name,
                    mo.batch AS org_batch,
                    mo.status AS org_status,
                    mo.role AS org_role,
                    mo.committee AS org_committee,
                    mo.academic_year,
                    mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ?;
                    """
                cur.execute( query, (self.user.getMemberId(), ))
            else:
                query = """
                    SELECT 
                    o.organization_name AS org_name,
                    mo.batch AS org_batch,
                    mo.status AS org_status,
                    mo.role AS org_role,
                    mo.committee AS org_committee,
                    mo.academic_year,
                    mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ? and mo.status = ?;
                    """
                cur.execute( query, (self.user.getMemberId(),statusInput, ))
        elif semesterInput == "":
            if statusInput == "All":
                query = """
                    SELECT 
                    o.organization_name AS org_name,
                    mo.batch AS org_batch,
                    mo.status AS org_status,
                    mo.role AS org_role,
                    mo.committee AS org_committee,
                    mo.academic_year,
                    mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ? and mo.academic_year = ?;
                    """
                cur.execute( query, (self.user.getMemberId(),acadYearInput, ))
            else:
                query = """
                    SELECT 
                        o.organization_name AS org_name,
                        mo.batch AS org_batch,
                        mo.status AS org_status,
                        mo.role AS org_role,
                        mo.committee AS org_committee,
                        mo.academic_year,
                        mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ? and mo.academic_year = ? and mo.status = ?;
                    """
                cur.execute( query, (self.user.getMemberId(),acadYearInput,statusInput, ))
        elif acadYearInput == "":
            if statusInput == "All":
                query = """
                    SELECT 
                    o.organization_name AS org_name,
                    mo.batch AS org_batch,
                    mo.status AS org_status,
                    mo.role AS org_role,
                    mo.committee AS org_committee,
                    mo.academic_year,
                    mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ? and mo.semester = ?;
                    """
                cur.execute( query, (self.user.getMemberId(),semesterInput, ))
            else:
                query = """
                    SELECT 
                        o.organization_name AS org_name,
                        mo.batch AS org_batch,
                        mo.status AS org_status,
                        mo.role AS org_role,
                        mo.committee AS org_committee,
                        mo.academic_year,
                        mo.semester
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ? and mo.semester = ? and mo.status = ?;
                    """
                cur.execute( query, (self.user.getMemberId(),semesterInput,statusInput, ))    
        else:
            if statusInput == "All":
                query = """
                        SELECT 
                            o.organization_name AS org_name,
                            mo.batch AS org_batch,
                            mo.status AS org_status,
                            mo.role AS org_role,
                            mo.committee AS org_committee,
                            mo.academic_year,
                            mo.semester
                        FROM organization o
                        JOIN member_org mo ON o.organization_id = mo.organization_id
                        JOIN member m ON m.member_id = mo.member_id
                        WHERE mo.member_id = ? and mo.academic_year = ? and mo.semester = ?; 
                    """  
                cur.execute( query, (self.user.getMemberId(),acadYearInput,semesterInput, ))                                           
            else:
                query = """
                        SELECT 
                            o.organization_name AS org_name,
                            mo.batch AS org_batch,
                            mo.status AS org_status,
                            mo.role AS org_role,
                            mo.committee AS org_committee,
                            mo.academic_year,
                            mo.semester
                        FROM organization o
                        JOIN member_org mo ON o.organization_id = mo.organization_id
                        JOIN member m ON m.member_id = mo.member_id
                        WHERE mo.member_id = ? and mo.academic_year = ? and mo.semester = ? and mo.status = ?; 
                    """ 
                cur.execute( query, (self.user.getMemberId(),acadYearInput,semesterInput,statusInput ))  
            
    
        # Clear old data
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in cur:
            self.tree.insert("",END,text="1",values=(row['org_name'],
                row["org_batch"] if row["org_batch"] != None else "No Batch",
                row["org_role"] if row["org_role"] != None else "No Role" ,
                row["org_committee"] if row["org_committee"] != None else "No Committee",
                row["org_status"] if row["org_status"] != None else "No Status"))
        self.tree.pack(fill=BOTH, expand=True)

class viewFees(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.user = self.master.user
        self.pack(fill=BOTH, expand=True) 
        #header
        self.header = Frame(self, height=60)
        self.header.pack(fill=X)
        Label(self.header, text="VIEW MY FEES", font=("Helvetica", 16, "bold")).pack() 
        # Navigation bar frame
        nav_frame = Frame(self, bg="lightgrey", height=60)
        nav_frame.pack(fill=X)
        # Inner frame to center buttons
        self.center_frame = Frame(nav_frame, bg="lightgrey")
        self.center_frame.pack(expand=True)
        Button(self.center_frame, text="Paid",font=("Helvetica", 12), bg="green", fg="white", width=10, command=self.getAllPaid).pack(side=LEFT, padx = 5)
        Button(self.center_frame, text="Unpaid",font=("Helvetica", 12), bg="red", fg="white", width=10, command=self.getAllUnpaid).pack(side=LEFT, padx = 5)
        Button(self.center_frame, text="Back",font=("Helvetica", 12), command=lambda:master.show_screen(MemberMenu), width=10).pack(side=LEFT,padx=10)
        tree_frame = Frame(self)
        tree_frame.pack(fill=BOTH, expand=True)

        # Scrollbars
        self.y_scrollbar = Scrollbar(tree_frame, orient=VERTICAL)
        self.x_scrollbar = Scrollbar(tree_frame, orient=HORIZONTAL)                                                  
        self.tree = ttk.Treeview(tree_frame, columns=("Fee ID","Record ID","Organization Name", "Fee Type", "Amount", "Due Date", "Status","Academic Year", "Semester"), show="headings", height=5, yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        self.tree.heading("Fee ID", text="Fee ID", anchor=CENTER)
        self.tree.heading("Record ID", text="Record ID", anchor=CENTER)
        self.tree.heading("Organization Name", text="Organization Name", anchor=CENTER)
        self.tree.heading("Fee Type", text="Fee Type", anchor=CENTER)
        self.tree.heading("Amount", text="Amount", anchor=CENTER)
        self.tree.heading("Due Date", text="Due Date", anchor=CENTER)
        self.tree.heading("Status", text="Status", anchor=CENTER)
        self.tree.heading("Academic Year", text="Academic Year", anchor=CENTER)
        self.tree.heading("Semester", text="Semester", anchor=CENTER)
        self.tree.column("Fee ID", anchor=CENTER)
        self.tree.column("Record ID", anchor=CENTER)
        self.tree.column("Organization Name", anchor=CENTER)
        self.tree.column("Fee Type", anchor=CENTER)
        self.tree.column("Amount", anchor=CENTER)
        self.tree.column("Due Date", anchor=CENTER)
        self.tree.column("Status", anchor=CENTER)
        self.tree.column("Academic Year", anchor=CENTER)
        self.tree.column("Semester", anchor=CENTER)

        #button to be showed
        self.payBtn = Button(self.center_frame, text="Pay Selected",font=("Helvetica", 12), bg="green", fg="white", width=10, command=self.pay)
        self.deselectBtn = Button(self.center_frame, text="DESELECT",font=("Helvetica", 12), fg="black", width=10, command=lambda:self.tree.selection_remove(self.tree.selection()))

    def getAllUnpaid(self):
        query = '''
            SELECT 
            f.fee_id,f.record_id, o.organization_name, f.fee_type, f.amount, f.due_date, f.payment_status, fr.academic_year, fr.semester
            from MEMBER m
            JOIN FEE f on m.member_id = f.member_id
            JOIN FINANCIAL_RECORD fr on f.record_id = fr.record_id
            JOIN ORGANIZATION o ON fr.organization_id = o.organization_id
            WHERE
            m.name = ? 
            AND f.payment_status = "Unpaid";
            '''
        cur = self.master.cur
        cur.execute( query, (self.user.getName(), ))
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in cur:
            self.tree.insert("",END,text="1",values=(row["fee_id"],row["record_id"],row['organization_name'] ,
                                        row["fee_type"] ,
                                        row["amount"]  ,
                                        row["due_date"] ,
                                        row["payment_status"],
                                        row["academic_year"],
                                        row["semester"]))
        
        self.y_scrollbar.config(command=self.tree.yview)
        self.x_scrollbar.config(command=self.tree.xview)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        self.x_scrollbar.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=True)
        if not self.payBtn.winfo_ismapped():  # Only pack if not already packed
            self.payBtn.pack(side=LEFT, padx=5)
        if not self.deselectBtn.winfo_ismapped():  # Only pack if not already packed
            self.deselectBtn.pack(side=LEFT)

    def pay(self):
        selected = self.tree.selection()
        payquery = '''UPDATE fee SET payment_status = "Paid" WHERE fee_id = ?;'''
        addbalancequery = '''UPDATE financial_record SET balance=balance + ? WHERE record_id = ? '''
        cur = self.master.cur
        conn = self.master.conn
        for item in selected:
            row_values = self.tree.item(item, "values")
            fee_id = row_values[0]
            amount = row_values[4]
            record_id = row_values[1]
            cur.execute( payquery, (fee_id, ))
            conn.commit()
            cur.execute( addbalancequery, (amount,record_id, ))
            conn.commit()


        self.getAllUnpaid()

           

    def getAllPaid(self):
        query = '''
            SELECT 
            f.fee_id,f.record_id, o.organization_name, f.fee_type, f.amount, f.due_date, f.payment_status, fr.academic_year, fr.semester
            from MEMBER m
            JOIN FEE f on m.member_id = f.member_id
            JOIN FINANCIAL_RECORD fr on f.record_id = fr.record_id
            JOIN ORGANIZATION o ON fr.organization_id = o.organization_id
            WHERE
            m.name = ? 
            AND f.payment_status = "Paid";
            '''
        cur = self.master.cur
        cur.execute( query, (self.user.getName(), ))
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in cur:
            self.tree.insert("",END,text="1",values=(row["fee_id"],row["record_id"],row['organization_name'] ,
                                        row["fee_type"] ,
                                        row["amount"]  ,
                                        row["due_date"] ,
                                        row["payment_status"],
                                        row["academic_year"],
                                        row["semester"]))
        self.y_scrollbar.config(command=self.tree.yview)
        self.x_scrollbar.config(command=self.tree.xview)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        self.x_scrollbar.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=True)
        if self.payBtn.winfo_ismapped():  # hide if packed
            self.payBtn.pack_forget()
        if self.deselectBtn.winfo_ismapped():  # hide if packed
            self.deselectBtn.pack_forget()

class viewMyProfile(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.card = Frame(self, height="200", width="500", bg="white", bd=2, relief="raised")
        self.card.place(relx=0.5, rely=0.5-0.1,anchor="center")
         # will prevent the card from scaling down when using a frame inside it
        self.card.pack_propagate(False)
        # Spacer above content (expands to push content down)
        self.top_spacer = Frame(self.card, bg='white')
        self.top_spacer.pack(side=TOP, fill='both', expand=True)
        #Header
        Label(self.top_spacer, text="My Profile", fg="Black",font=("Helvetica", 16, "bold italic"), bg="white").pack(side=LEFT)
        # frame for the name
        self.name = Frame(self.card, height="40", bg="white")
        self.name.pack(fill=X, pady="5")
        Label(self.name, text="Name: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.readName = Entry(self.name, font=("Helvetica", 12), bg="#F8F8F8")
        self.readName.insert(0, f"{self.user.getName()}")
        self.readName.config(state="readonly")
        self.readName.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #username
        self.userName = Frame(self.card, height="40", bg="white")
        self.userName.pack(fill=X, pady="5")
        Label(self.userName, text="Username: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.readUserName = Entry(self.userName, font=("Helvetica", 12), bg="#F8F8F8")
        self.readUserName.insert(0, f"{self.user.getUsername()}")
        self.readUserName.config(state="readonly")
        self.readUserName.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #gender
        self.gender = Frame(self.card, height="40", bg="white")
        self.gender.pack(fill=X, pady="5")
        Label(self.gender, text="Gender: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.readGender = Entry(self.gender, font=("Helvetica", 12), bg="#F8F8F8")
        self.readGender.insert(0, f"{self.user.getGender()}")
        self.readGender.config(state="readonly")
        self.readGender.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #degree program
        self.degProg = Frame(self.card, height="40", bg="white")
        self.degProg.pack(fill=X, pady="5")
        Label(self.degProg, text="Degree Program: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.readDegProg = Entry(self.degProg, font=("Helvetica", 12), bg="#F8F8F8")
        self.readDegProg.insert(0, f"{self.user.getDegreeProgram()}")
        self.readDegProg.config(state="readonly")
        self.readDegProg.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #bottom spacer
        self.bot_spacer = Frame(self.card, bg='white')
        self.bot_spacer.pack(side=BOTTOM, fill='both', expand=True)
        #buttons
        self.buttons = Frame(self, width="500")
        self.buttons.place(relx=0.5, rely=0.5 + 0.2, anchor="n")
        Button(self.buttons, text="Back",font=("Helvetica", 12), command=lambda:master.show_screen(MemberMenu)).pack(side=LEFT, padx="15")
        Button(self.buttons, text="Change Password",font=("Helvetica", 12), command=self.changePassword).pack(side=LEFT, padx="15")
        Button(self.buttons, text="Edit",font=("Helvetica", 12), command=self.profileEdit).pack(side=RIGHT, padx="15")

    def profileEdit(self):
        editProfile = editMyProfile(self.master)
        self.master.screens[editMyProfile] = editProfile
        editProfile.place(relwidth=1, relheight=1)
        self.master.show_screen(editMyProfile)
    
    def changePassword(self):
        passwordChange = changeMyPassword(self.master)
        self.master.screens[changeMyPassword] = passwordChange
        passwordChange.place(relwidth=1, relheight=1)
        self.master.show_screen(changeMyPassword)

class editMyProfile(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.card = Frame(self, height="200", width="500", bg="white", bd=2, relief="raised")
        self.card.place(relx=0.5, rely=0.5-0.1,anchor="center")
         # will prevent the card from scaling down when using a frame inside it
        self.card.pack_propagate(False)
        # Spacer above content (expands to push content down)
        self.top_spacer = Frame(self.card, bg='white')
        self.top_spacer.pack(side=TOP, fill='both', expand=True)
        #Header
        Label(self.top_spacer, text="EDIT PROFILE", fg="Black",font=("Helvetica", 16, "bold italic"), bg="white").pack(side=LEFT)
        # frame for the name
        self.name = Frame(self.card, height="40", bg="white")
        self.name.pack(fill=X, pady="5")
        Label(self.name, text="Name: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.nameEntry = Entry(self.name, font=("Helvetica", 12), bg="#F8F8F8")
        self.nameEntry.insert(0, f"{self.user.getName()}")
        self.nameEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #username
        self.userName = Frame(self.card, height="40", bg="white")
        self.userName.pack(fill=X, pady="5")
        Label(self.userName, text="Username: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.userNameEntry = Entry(self.userName, font=("Helvetica", 12), bg="#F8F8F8")
        self.userNameEntry.insert(0, f"{self.user.getUsername()}")
        self.userNameEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #gender
        self.gender = Frame(self.card, height="40", bg="white")
        self.gender.pack(fill=X, pady="5")
        Label(self.gender, text="Gender: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.genderEntry = Entry(self.gender, font=("Helvetica", 12), bg="#F8F8F8")
        self.genderEntry.insert(0, f"{self.user.getGender()}")
        self.genderEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #degree program
        self.degProg = Frame(self.card, height="40", bg="white")
        self.degProg.pack(fill=X, pady="5")
        Label(self.degProg, text="Degree Program: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.degProgEntry = Entry(self.degProg, font=("Helvetica", 12), bg="#F8F8F8")
        self.degProgEntry.insert(0, f"{self.user.getDegreeProgram()}")
        self.degProgEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #Bottom spacer
        self.bot_spacer = Frame(self.card, bg='white')
        self.bot_spacer.pack(side=BOTTOM, fill='both', expand=True)
        #Buttons frame
        self.buttons = Frame(self, width="500")
        self.buttons.place(relx=0.5, rely=0.5 + 0.2, anchor="n")
        Button(self.buttons, text="Cancel",font=("Helvetica", 12),bg="red",fg="white", command=lambda:master.show_screen(viewMyProfile)).pack(side=LEFT, padx="15")
        Button(self.buttons, text="Confirm",font=("Helvetica", 12),bg="green",fg="white", command=self.editUser).pack(side=RIGHT, padx="15")

    def editUser(self):
        cur = self.master.cur
        conn = self.master.conn
        nameInput = self.nameEntry.get()
        userNameInput = self.userNameEntry.get()
        genderInput = self.genderEntry.get()
        degProgInput = self.degProgEntry.get()
        query = '''
                UPDATE member SET
                name = ?,
                gender = ?,
                degree_program = ?,
                username = ?
                WHERE member_id = ?;
                '''
        #check if all fields have input
        if nameInput == "" or userNameInput == "" or genderInput == "" or degProgInput == "":
            messagebox.showerror("Edit Failed", "All fields are required")
        else:
            #check if the userNameInput is changed
            if self.user.getUsername() != userNameInput:
                #check if the new username is not unique
                cur.execute( "select username from member where username = ?;", (userNameInput, ))
                result = cur.fetchone()
                if result != None:
                    messagebox.showerror("Failed to Edit", "Username Already Exists")
                else:
                    cur.execute(query, (nameInput,genderInput,degProgInput,userNameInput,self.user.getMemberId(),))
                    conn.commit()
                    user = User(self.user.getMemberId(), nameInput, genderInput, degProgInput, self.user.getAccessLevel(), userNameInput, "2024-2025", 2)
                    self.master.user = user
                    messagebox.showinfo("Success", "You successfully edited your profile")
                    self.master.show_screen(MemberMenu)  
                    
            else:
                cur.execute(query, (nameInput,genderInput,degProgInput,userNameInput,self.user.getMemberId(),))
                conn.commit()
                user = User(self.user.getMemberId(), nameInput, genderInput, degProgInput, self.user.getAccessLevel(), userNameInput, "2024-2025", 2)
                self.master.user = user
                messagebox.showinfo("Success", "You successfully edited your profile")
                self.master.show_screen(MemberMenu)   
            
        


class changeMyPassword(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.card = Frame(self, height="200", width="500", bg="white", bd=2, relief="raised")
        self.card.place(relx=0.5, rely=0.5-0.1,anchor="center")
         # will prevent the card from scaling down when using a frame inside it
        self.card.pack_propagate(False)
        # Spacer above content (expands to push content down)
        self.top_spacer = Frame(self.card, bg='white')
        self.top_spacer.pack(side=TOP, fill='both', expand=True)
        #Header
        Label(self.top_spacer, text="Change Password", fg="Black",font=("Helvetica", 16, "bold italic"), bg="white").pack(side=LEFT)
        #old pass
        self.oldPass = Frame(self.card, height="40", bg="white")
        self.oldPass.pack(fill=X, pady="5")
        Label(self.oldPass, text="Old Pass: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.oldPassEntry = Entry(self.oldPass, font=("Helvetica", 12), bg="#F8F8F8")
        self.oldPassEntry.insert(0, "")
        self.oldPassEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #new pass
        self.newPass = Frame(self.card, height="40", bg="white")
        self.newPass.pack(fill=X, pady="5")
        Label(self.newPass, text="New Password: ", fg="Black",font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT)
        self.newPassEntry = Entry(self.newPass, font=("Helvetica", 12), bg="#F8F8F8")
        self.newPassEntry.insert(0, "")
        self.newPassEntry.pack(side=LEFT, padx = 5, fill=X, expand=True)
        #Bottom spacer
        self.bot_spacer = Frame(self.card, bg='white')
        self.bot_spacer.pack(side=BOTTOM, fill='both', expand=True)
        #Buttons frame
        self.buttons = Frame(self, width="500")
        self.buttons.place(relx=0.5, rely=0.5 + 0.2, anchor="n")
        Button(self.buttons, text="Cancel",font=("Helvetica", 12),bg="red",fg="white", command=lambda:master.show_screen(viewMyProfile)).pack(side=LEFT, padx="15")
        Button(self.buttons, text="Confirm",font=("Helvetica", 12),bg="green",fg="white", command=self.editPassword).pack(side=RIGHT, padx="15")
    
    def editPassword(self):
        cur = self.master.cur
        conn = self.master.conn
        oldPassInput = self.oldPassEntry.get()
        newPassInput = self.newPassEntry.get()
        query = '''
                UPDATE member SET
                password = ?
                WHERE member_id = ?;
                '''
        if newPassInput == "" or oldPassInput == "":
            messagebox.showerror("Update Password Failed", "all fields are required")
        else:
            #check if the entered old password is correct
            try:
                cur.execute("SELECT * FROM member WHERE member_id=?", (self.user.getMemberId(), ))
            except mariadb.Error as e:
                print(f"Error in changing password: {e}")
                sys.exit(1)
            
            result = cur.fetchone()
            matchedPass = result["password"]
            if oldPassInput != matchedPass:
                messagebox.showerror("Update Password Failed", "Incorrect old password")
            else:
                cur.execute(query, (newPassInput,self.user.getMemberId(), ))
                conn.commit()
                messagebox.showinfo("Success", "Successfully updated password")
                self.master.show_screen(MemberMenu)


if __name__ == "__main__":
    app = App()
    app.mainloop()
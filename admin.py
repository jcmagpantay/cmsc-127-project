import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import Database

import mariadb

class AdminMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user

        Label(self, text="Main Menu", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="(Admin)", fg="Black",font=("Helvetica", 18)).pack()
        Label(self, text=f"A.Y. {self.user.getAcademicYear()} Semester {self.user.getSemester()}", fg="Black",font=("Helvetica", 10)).pack()
        Button(self, text="Add a Member",font=("Helvetica", 12), command=self.goToAddMemberPage).pack(pady=2.5)
        Button(self, text="View All Members",font=("Helvetica", 12)).pack(pady=2.5)
        Button(self, text="Edit Member",font=("Helvetica", 12)).pack(pady=2.5)
        Button(self, text="Remove Member",font=("Helvetica", 12)).pack(pady=2.5)
        Button(self, text="Generate Reports",font=("Helvetica", 12)).pack(pady=2.5)
        Button(self, text="Logout",fg="white", bg="Red",font=("Helvetica", 12)).pack(pady=2.5)
    
    def goToAddMemberPage(self):
        self.master.show_page(AddMemberPage)

class AddMemberPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.cur = self.master.cur
        self.db:Database = self.master.db

        organizations = self.getOrganizationsList()
        print("Dictionary fetched from DB:", organizations)
        orgDisplay = [f"{org_id} - {org_name}" for org_id, org_name in organizations.items()]
        orgDisplay.sort()
        print("Displaying:", orgDisplay)
        self.idLookup = {f"{org_id} - {org_name}": org_id for org_id, org_name in organizations.items()}

        container = Frame(self)
        container.pack(anchor='n', pady=16)

        row = 0

        Label(container, text="Add A Member", fg="Black", font=("Helvetica", 18)).grid(row=row, column=0, columnspan=2, pady=(10, 20))
        row += 1

        # Name
        Label(container, text="Name*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.nameField = LimitedEntry(container, char_limit=50)
        self.nameField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Gender
        Label(container, text="Gender*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.genderField = LimitedEntry(container, char_limit=6)
        self.genderField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Degree Program
        Label(container, text="Degree Program*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.degreeProgramField = LimitedEntry(container, char_limit=50)
        self.degreeProgramField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Username
        Label(container, text="Username*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.usernameField = LimitedEntry(container, char_limit=20)
        self.usernameField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Password
        Label(container, text="Password*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.passwordField = LimitedEntry(container, char_limit=20, show="•")
        self.passwordField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        Label(container, text="Select organization", fg="Black", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2)
        row += 1

        self.selectedOrg = StringVar()
        organizationSelect = ttk.Combobox(container, textvariable=self.selectedOrg, values=orgDisplay)
        organizationSelect.grid(row=row, column=0, columnspan=2, pady=4 )
        row += 1

        Label(container, text="Batch*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.batchField = LimitedEntry(container, char_limit=20)
        self.batchField.grid(row=row, column=1, padx=8, pady=4)
        row += 1
        
        # TODO: Make this a dropdown
        Label(container, text="Org Status*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.statusField = LimitedEntry(container, char_limit=10)
        self.statusField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        Label(container, text="Role*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.roleField = LimitedEntry(container, char_limit=10)
        self.roleField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        Label(container, text="Committee*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.committeeField = LimitedEntry(container, char_limit=20)
        self.committeeField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # TODO: ADD VALIDATION: YYYY - YYYY
        Label(container, text="Academic Year*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.academicYearField = LimitedEntry(container, char_limit=20)
        self.academicYearField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # TODO: ADD VALIDATION: 1 or 2
        Label(container, text="Semester*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.semesterField = LimitedEntry(container, char_limit=20)
        self.semesterField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Button
        Button(container, text="Add Member", font=("Helvetica", 12), command=self.onSubmit).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        Button(container, text="Go Back", font=("Helvetica", 12), command=self.goBack).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        
    
    def goBack(self):
        self.master.show_page(AdminMenu)

    def onSubmit(self):
        if (self.nameField.isEmpty() or
            self.genderField.isEmpty() or
            self.degreeProgramField.isEmpty() or
            self.usernameField.isEmpty() or
            self.passwordField.isEmpty() or
            (len(self.selectedOrg.get()) == 0) or
            self.batchField.isEmpty() or
            self.statusField.isEmpty() or
            self.roleField.isEmpty() or
            self.committeeField.isEmpty() or
            self.academicYearField.isEmpty() or
            self.semesterField.isEmpty()
        ):
            messagebox.showerror("Creating Member Error", "Please input required fields.")
            return

        if (self.db.username_exists(self.usernameField.get())):
            messagebox.showerror("Creating Member Error", "Username is already existing.")
            return

        memberID = self.db.create_user(
            name=self.nameField.get(),
            gender=self.genderField.get(),
            degree_program=self.degreeProgramField.get(),
            password=self.passwordField.get(),
            access_level=1,
            username=self.usernameField.get()
        )
        
        if (memberID is None):
            messagebox.showerror("Creating Member Error", "Error in creating member.")
            return
        
        # Create membership
        membership = self.db.create_membership(
            member_id= memberID,
            organization_id= self.idLookup[self.selectedOrg.get()],
            batch= self.batchField.get(), 
            status= self.statusField.get(),
            committee= self.committeeField.get(),
            role= self.roleField.get(),
            acad_year= self.academicYearField.get(),
            semester= self.semesterField.get()
        )
        
        if (membership is None):
            messagebox.showerror("Creating Member Error", "Error in creating membership.")
            return
        else:
            messagebox.showinfo("Success!", f"Successfully added {self.nameField.get()} to {self.selectedOrg.get()}")
            return
        
    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}

class LimitedEntry(Entry):
    def __init__(self, master=None, char_limit=10, **kwargs):
        self.char_limit = char_limit
        self.var = StringVar()
        super().__init__(master, textvariable=self.var, **kwargs)

        # register validation command
        vcmd = self.register(self.on_validate)
        self.config(validate="key", validatecommand=(vcmd, '%P'))

    def on_validate(self, proposed_text):
        return len(proposed_text) <= self.char_limit

    def set_limit(self, new_limit):
        self.char_limit = new_limit
    
    def get(self):
        return self.var.get()
    
    def isEmpty(self):
        return len(self.var.get()) == 0
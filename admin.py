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
        Button(self, text="View All Members",font=("Helvetica", 12), command=self.goToViewMembersPage).pack(pady=2.5)
        Button(self, text="View Organization Membership",font=("Helvetica", 12), command=self.goToViewOrganizationalMembersPage).pack(pady=2.5)
        Button(self, text="Generate Reports",font=("Helvetica", 12)).pack(pady=2.5)
    
    def goToAddMemberPage(self):
        self.master.show_page(AddMemberPage)

    def goToViewMembersPage(self):
        self.master.show_page(ViewMembersPage)
    
    def goToViewOrganizationalMembersPage(self):
        self.master.show_page(ViewOrganizationalMembersPage)

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

class ViewMembersPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.db:Database = self.master.db
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.pack(fill=BOTH, expand=True)

        Label(self, text="View Members", fg="Black", font=("Helvetica", 18)).pack(pady=8)
    
        options_container = Frame(self)
        options_container.pack(fill=X, pady=(0, 8))

        canvas = Canvas(options_container, height=30)
        h_scrollbar = Scrollbar(options_container, orient=HORIZONTAL, command=canvas.xview)
        canvas.configure(xscrollcommand=h_scrollbar.set)

        canvas.pack(side=TOP, fill=X, expand=True)
        h_scrollbar.pack(side=BOTTOM, fill=X)

        options = Frame(canvas)
        canvas.create_window((0, 0), window=options, anchor='nw')

        def on_options_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        options.bind("<Configure>", on_options_configure)

        Button(options, text="Back", font=("Helvetica", 12), command=self.goBack).pack(side=LEFT, padx=16)

        Label(options, text="Select a member to:", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=2)

        editBtn = Button(options, text="Edit", font=("Helvetica", 12))
        editBtn.pack(side=LEFT, padx=4)

        deleteBtn = Button(options, text="Delete", font=("Helvetica", 12))
        deleteBtn.pack(side=LEFT, padx=4)

        Label(options, text="Name", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.nameVar = StringVar()
        Entry(options, textvariable=self.nameVar).pack(side=LEFT, padx=4)

        Label(options, text="Gender", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.genderVar = StringVar()
        Entry(options, textvariable=self.genderVar).pack(side=LEFT, padx=4)

        Label(options, text="Degree Program", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.degreeProgramVar = StringVar()
        Entry(options, textvariable=self.degreeProgramVar).pack(side=LEFT, padx=4)

        Label(options, text="Username", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.usernameVar = StringVar()
        Entry(options, textvariable=self.usernameVar).pack(side=LEFT, padx=4)

        self.nameVar.trace_add("write", self.on_filter_changed)
        self.genderVar.trace_add("write", self.on_filter_changed)
        self.degreeProgramVar.trace_add("write", self.on_filter_changed)
        self.usernameVar.trace_add("write", self.on_filter_changed)

        columns = ("ID", "Name", "Gender", "Degree Program", "Password", "Access Level", "Username")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True)  # Make sure treeview is packed
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()

    def goBack(self):
        self.master.show_page(AdminMenu)

    def on_filter_changed(self, *args):
        # Clear the tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        name = self.nameVar.get().strip() or None
        gender = self.genderVar.get().strip() or None
        degreeProgram = self.degreeProgramVar.get().strip() or None
        username = self.usernameVar.get().strip() or None

        data = self.db.get_all_members(name= name, gender= gender, degree_program= degreeProgram, username= username)

        for row in data:
            self.tree.insert("", "end",
                values=(
                row["member_id"], row["name"], row["gender"],
                row["degree_program"], row["password"], row["access_level"],
                row["username"]))


class ViewOrganizationalMembersPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.db:Database = self.master.db
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.pack(fill=BOTH, expand=True)
        self.cur = self.master.cur

        organizations = self.getOrganizationsList()
        orgDisplay = [f"{org_id} - {org_name}" for org_id, org_name in organizations.items()]
        orgDisplay.sort()
        orgDisplay.insert(0, "All")

        self.idLookup = {f"{org_id} - {org_name}": org_id for org_id, org_name in organizations.items()}
        self.idLookup["All"] = None

        Label(self, text="View Members", fg="Black", font=("Helvetica", 18)).pack(pady=8)

        options_container = Frame(self)
        options_container.pack(fill=X, pady=(0, 8))

        canvas = Canvas(options_container, height=30)
        h_scrollbar = Scrollbar(options_container, orient=HORIZONTAL, command=canvas.xview)
        canvas.configure(xscrollcommand=h_scrollbar.set)

        canvas.pack(side=TOP, fill=X, expand=True)
        h_scrollbar.pack(side=BOTTOM, fill=X)

        options = Frame(canvas)
        canvas.create_window((0, 0), window=options, anchor='nw')

        def on_options_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        options.bind("<Configure>", on_options_configure)


        Button(options, text="Back", font=("Helvetica", 12), command=self.goBack).pack(side=LEFT, padx=4)

        Label(options, text="Filter by:", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=8)
        Label(options, text="Organization", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.selectedOrg = StringVar(value="All")
        organizationFilter = ttk.Combobox(options, textvariable=self.selectedOrg, values=orgDisplay, width=16)
        organizationFilter.pack(side=LEFT, padx=4)

        Label(options, text="Status", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.statusVar = StringVar()
        statusFilter = Entry(options, textvariable=self.statusVar)
        statusFilter.pack(side=LEFT, padx=4)

        Label(options, text="Committee", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.committeeVar = StringVar()
        committeeFilter = Entry(options, textvariable=self.committeeVar)
        committeeFilter.pack(side=LEFT, padx=4)

        Label(options, text="Role", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.roleVar = StringVar()
        roleFilter = Entry(options, textvariable=self.roleVar)
        roleFilter.pack(side=LEFT, padx=4)

        Label(options, text="Academic Year", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.academicYearVar = StringVar()
        academicYearFilter = Entry(options, textvariable=self.academicYearVar)
        academicYearFilter.pack(side=LEFT, padx=4)

        Label(options, text="Semester", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        semesterChoices = ["All", "1", "2"]
        self.semesterVar = StringVar(value=semesterChoices[0])  # default value
        semesterFilter = OptionMenu(options, self.semesterVar, *semesterChoices)
        semesterFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.statusVar.trace_add("write", self.on_filter_changed)
        self.committeeVar.trace_add("write", self.on_filter_changed)
        self.roleVar.trace_add("write", self.on_filter_changed)
        self.academicYearVar.trace_add("write", self.on_filter_changed)
        self.semesterVar.trace_add("write", self.on_filter_changed)

        columns = ("Member ID", "Name", "Organization Name", "Batch", "Status", "Committee", "Role", "Academic Year", "Semester")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True)  # Make sure treeview is packed
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        # Clear the tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Gather filter values (use None or empty string as default)
        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None

        status = self.statusVar.get().strip() or None
        committee = self.committeeVar.get().strip() or None
        role = self.roleVar.get().strip() or None
        academic_year = self.academicYearVar.get().strip() or None
        semester = self.semesterVar.get() if hasattr(self, 'semesterVar') else None
        if semester == "All":
            semester = None

        # Fetch filtered data
        data = self.db.get_all_organization_members(
            organization_id=organization_id,
            status=status,
            committee=committee,
            role=role,
            academic_year=academic_year,
            semester=semester,
        )

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"], row["member_name"], row["organization_name"],
                row["member_batch"], row["member_status"], row["member_committee"],
                row["role"], row["academic_year"], row["semester"]
            ))

    def goBack(self):
        self.master.show_page(AdminMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}

class EditMemberPage(Frame):
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

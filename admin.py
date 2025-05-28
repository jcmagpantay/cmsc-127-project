import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import Database
from datetime import date

import mariadb

class AdminMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user

        Label(self, text="Main Menu", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="(Admin)", fg="Black",font=("Helvetica", 18)).pack()
        Label(self, text=f"A.Y. {self.user.getAcademicYear()} Semester {self.user.getSemester()}", fg="Black",font=("Helvetica", 10)).pack()
        Button(self, text="Add a...",font=("Helvetica", 12), command=self.goToCreateMenu).pack(pady=2.5)
        Button(self, text="View All Members",font=("Helvetica", 12), command=self.goToViewMembersPage).pack(pady=2.5)
        Button(self, text="View Organization Membership",font=("Helvetica", 12), command=self.goToViewOrganizationalMembersPage).pack(pady=2.5)
        Button(self, text="Generate Reports",font=("Helvetica", 12), command=self.goToReportsMenu).pack(pady=2.5)
        Button(self, text="Logout",fg="red", bg="Red",font=("Helvetica", 12), command=master.goToLanding).pack(pady=2.5)
        
    
    def goToCreateMenu(self):
        self.master.show_page(CreateMenu)

    def goToViewMembersPage(self):
        self.master.show_page(ViewMembersPage)
    
    def goToViewOrganizationalMembersPage(self):
        self.master.show_page(ViewOrganizationalMembersPage)

    def goToReportsMenu(self):
        self.master.show_page(ReportMenu)


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

        Button(options, text="Back", font=("Helvetica", 12), command=self.goBack,).pack(side=LEFT, padx=16)
        Button(options, text="Clear", font=("Helvetica", 12), command=lambda: self.tree.selection_remove(self.tree.selection())).pack(side=LEFT, padx=16)

        Label(options, text="Select a member to:", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=2)

        self.editBtn = Button(options, text="Edit", font=("Helvetica", 12), state="disabled", command= self.on_edit)
        self.editBtn.pack(side=LEFT, padx=4)

        self.deleteBtn = Button(options, text="Delete", font=("Helvetica", 12), state="disabled", command= self.on_delete)
        self.deleteBtn.pack(side=LEFT, padx=4)

        self.addFeeBtn = Button(options, text="Add Fee", font=("Helvetica", 12), state="disabled", command= self.on_add_fee)
        self.addFeeBtn.pack(side=LEFT, padx=4)

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
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.refresh()

    def refresh(self):
        self.on_filter_changed()

    def goBack(self):
        self.currentMember = None
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
    
    # Enables / disables button if tree is selected
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.editBtn.config(state="normal")  
            self.deleteBtn.config(state="normal")  
            self.addFeeBtn.config(state="normal")  
            selected_values = self.tree.item(self.tree.selection()[0], 'values')
            self.currentMember = selected_values 
        else:
            self.tree.selection_remove(self.tree.selection())
            self.editBtn.config(state="disabled") 
            self.deleteBtn.config(state="disabled") 
            self.addFeeBtn.config(state="disabled") 
            self.currentMember = None

    def goToEditMemberPage(self):
        if hasattr(self, 'currentMember'):
            print("I have that")
            self.master.currentMember = self.currentMember
            self.master.show_page(EditMemberPage)

    def goToAddFeePage(self):
        if hasattr(self, 'currentMember'):
            print("I have that")
            self.master.currentMember = self.currentMember
            self.master.show_page(AddFeePage)

    def on_edit(self):
        selected_values = self.tree.item(self.tree.selection()[0], 'values')
        self.currentMember = selected_values
        self.master.currentMember = self.currentMember
        self.goToEditMemberPage()
    
    def on_delete(self):
        selected_values = self.tree.item(self.tree.selection()[0], 'values')
        memberID = selected_values[0]
        success = self.db.delete_member(member_id= memberID)
        if success:
            messagebox.showinfo("Success", f"Member {selected_values[1]} deleted successfully.")
        else:
            messagebox.showerror("Error", f"Failed to delete member {selected_values[1]}.")
        self.refresh()

    def on_add_fee(self):
        selected_values = self.tree.item(self.tree.selection()[0], 'values')
        print(selected_values)
        self.currentMember = selected_values
        self.master.currentMember = self.currentMember
        self.goToAddFeePage()
        

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

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

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
    killable = True

    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.cur = self.master.cur
        self.db:Database = self.master.db
        self.currentMember = self.master.currentMember
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
        self.nameVar = StringVar(value=self.currentMember[1])
        LimitedEntry(container, char_limit=50, textvariable = self.nameVar).grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Gender
        Label(container, text="Gender*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.genderVar = StringVar(value=self.currentMember[2])
        LimitedEntry(container, char_limit=6, textvariable=self.genderVar).grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Degree Program
        Label(container, text="Degree Program*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.degreeProgramVar = StringVar(value=self.currentMember[3])
        LimitedEntry(container, char_limit=50, textvariable=self.degreeProgramVar).grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Username
        Label(container, text="Username*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.usernameVar = StringVar(value=self.currentMember[6])
        LimitedEntry(container, char_limit=20, textvariable=self.usernameVar).grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Password
        Label(container, text="Password*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.passwordVar = StringVar(value=self.currentMember[4])
        LimitedEntry(container, char_limit=20, show="•", textvariable = self.passwordVar).grid(row=row, column=1, padx=8, pady=4)
        row += 1
        ## ADD TO ORG
        Label(container, text="Add to org (optional)", fg="Black", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2)
        row += 1

        Label(container, text="Note: This will only add more organizations to the member", fg="Black", font=("Helvetica", 6)).grid(row=row, column=0, columnspan=2)
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
        Button(container, text="Save Edits", font=("Helvetica", 12), command=self.onSubmit).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        Button(container, text="Go Back", font=("Helvetica", 12), command=self.goBack).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

    def goBack(self):
        self.master.currentMember = None
        self.master.show_page(ViewMembersPage)

    def onSubmit(self):
        name = self.nameVar.get().strip() or None
        gender = self.genderVar.get().strip() or None
        degreeProgram = self.degreeProgramVar.get().strip() or None
        username = self.usernameVar.get().strip() or None
        password = self.passwordVar.get().strip() or None

        
        
        org_fields = [
            self.selectedOrg.get(),
            self.batchField.get(),
            self.statusField.get(),
            self.roleField.get(),
            self.committeeField.get(),
            self.academicYearField.get(),
            self.semesterField.get()
        ]

        all_empty = all(len(f.strip()) == 0 for f in org_fields)
        all_filled = all(len(f.strip()) > 0 for f in org_fields)

        if not (all_empty or all_filled):
            messagebox.showerror("Incomplete Fields", "If you fill in one organization-related field, you must fill them all.")
            return
        
        memberID = self.db.update_member(
            member_id=self.currentMember[0],
            name= name,
            gender= gender,
            degree_program= degreeProgram,
            password= password,
            username= username
        )
        
        if (memberID is None):
            messagebox.showerror("Updating Member Error", "Error in editing member.")
            return
        
        if (all_empty):
            messagebox.showinfo("Success",f"Successfully edited Member {self.currrentMember[0]}")
            return
        
        if (all_filled):
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
            messagebox.showerror("Creating Member Error", "Duplicate membership")
            return
        else:
            messagebox.showinfo("Success!", f"Successfully added Member {memberID} to {self.selectedOrg.get()}")
            self.master.screens[ViewMembersPage].refresh()
            self.goBack()
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
        
class CreateOrganizationPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.cur = self.master.cur
        self.db:Database = self.master.db

        container = Frame(self)
        container.pack(anchor='n', pady=16)

        row = 0

        Label(container, text="Create organization", fg="Black", font=("Helvetica", 18)).grid(row=row, column=0, columnspan=2, pady=(10, 20))
        row += 1

        # Name
        Label(container, text="Organization Name*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.nameField = LimitedEntry(container, char_limit=50)
        self.nameField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Date Established
        Label(container, text="Date Established*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.dateField = LimitedEntry(container, char_limit=10)
        self.dateField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Button
        Button(container, text="Create Organization", font=("Helvetica", 12), command=self.onSubmit).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        Button(container, text="Go Back", font=("Helvetica", 12), command=self.goBack).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

    def goBack(self):
        self.master.show_page(CreateMenu)

    def onSubmit(self):
        if (self.dateField.isEmpty() or self.nameField.isEmpty()):
            messagebox.showerror("Error", "Please fill in required fields")
            return
    
        organizationID = self.db.create_org(organization_name= self.nameField.get().strip(), date_established=self.dateField.get().strip())

        if (organizationID is None):
            messagebox.showerror("Error", "Error in creating org.")
        else:
            messagebox.showinfo("Success", f"{self.nameField.get().strip()} successfully established at {self.dateField.get().strip()}!")
            self.goBack
    

class AddFinancialRecordPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.cur = self.master.cur
        self.db:Database = self.master.db
        organizations = self.getOrganizationsList()
        orgDisplay = [f"{org_id} - {org_name}" for org_id, org_name in organizations.items()]
        orgDisplay.sort()
        self.idLookup = {f"{org_id} - {org_name}": org_id for org_id, org_name in organizations.items()}

        container = Frame(self)
        container.pack(anchor='n', pady=16)

        row = 0

        Label(container, text="Add a financial record", fg="Black", font=("Helvetica", 18)).grid(row=row, column=0, columnspan=2, pady=(10, 20))
        row += 1

        Label(container, text="Select organization", fg="Black", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        self.selectedOrg = StringVar()
        organizationSelect = ttk.Combobox(container, textvariable=self.selectedOrg, values=orgDisplay)
        organizationSelect.grid(row=row, column=0, columnspan=2, pady=4 )
        row += 1

        # Name
        Label(container, text="Balance*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.balanceField = LimitedEntry(container, char_limit=50)
        self.balanceField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Academic Year
        Label(container, text="Academic Year*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.academicYearField = LimitedEntry(container, char_limit=10)
        self.academicYearField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Semester
        Label(container, text="Semester*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.semesterField = LimitedEntry(container, char_limit=10)
        self.semesterField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Button
        Button(container, text="Add financial record", font=("Helvetica", 12), command=self.onSubmit).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        Button(container, text="Go Back", font=("Helvetica", 12), command=self.goBack).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

    def goBack(self):
        self.master.show_page(CreateMenu)

    def onSubmit(self):
        if (self.balanceField.isEmpty() or self.academicYearField.isEmpty() or self.semesterField.isEmpty() or len(self.selectedOrg.get()) == 0):
            messagebox.showerror("Error", "Please fill in required fields")
            return
        orgID = self.idLookup[self.selectedOrg.get()]
        balance = self.balanceField.get()
        academicYear = self.academicYearField.get()
        semester = self.semesterField.get()
    
        recordID = self.db.create_financial_record(organization_id=orgID, balance= balance, semester= semester, academic_year=academicYear)

        if (recordID is None):
            messagebox.showerror("Error", "Error in creating record.")
        else:
            messagebox.showinfo("Success", f"Financial record created for {self.selectedOrg.get()}!")
            self.goBack()

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
class AddFeePage(Frame):
    killable = True

    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        self.cur = self.master.cur
        self.db:Database = self.master.db
        self.currentMember = self.master.currentMember
        organizations = self.getMemberOrganizations()
        orgDisplay = [f"{org_id} - {org_name}" for org_id, org_name in organizations.items()]
        orgDisplay.sort()
        self.idLookup = {f"{org_id} - {org_name}": org_id for org_id, org_name in organizations.items()}

        container = Frame(self)
        container.pack(anchor='n', pady=16)

        row = 0

        Label(container, text=f"Add a fee for {self.currentMember[1]}", fg="Black", font=("Helvetica", 18)).grid(row=row, column=0, columnspan=2, pady=(10, 20))
        row += 1

        Label(container, text="Select organization", fg="Black", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        self.selectedOrg = StringVar()
        organizationSelect = ttk.Combobox(container, textvariable=self.selectedOrg, values=orgDisplay)
        organizationSelect.grid(row=row, column=0, columnspan=2, pady=4 )
        row += 1

        # AMT
        Label(container, text="Amount*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.amountField = LimitedEntry(container, char_limit=10)
        self.amountField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Due Date
        Label(container, text="Due Date*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.dueDateField = LimitedEntry(container, char_limit=10)
        self.dueDateField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Fee Type
        Label(container, text="Fee Type*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.feeTypeField = LimitedEntry(container, char_limit=10)
        self.feeTypeField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Description
        Label(container, text="Decription", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.descriptionField = LimitedEntry(container, char_limit=10)
        self.descriptionField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Academic Year
        Label(container, text="Academic Year*", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.academicYearField = LimitedEntry(container, char_limit=10)
        self.academicYearField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Semester
        Label(container, text="Semester", fg="Black", font=("Helvetica", 12), anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=8, pady=4)
        self.semesterField = LimitedEntry(container, char_limit=10)
        self.semesterField.grid(row=row, column=1, padx=8, pady=4)
        row += 1

        # Button
        Button(container, text="Add fee", font=("Helvetica", 12), command=self.onSubmit).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

        Button(container, text="Go Back", font=("Helvetica", 12), command=self.goBack).grid(row=row, column=0, columnspan=2, pady=4)
        row += 1

    def goBack(self):
        self.master.currentMember = None
        self.master.show_page(ViewMembersPage)
        self.selectedOrg.set("")
        self.descriptionField.clear()
        self.amountField.clear()
        self.dueDateField.clear()
        self.feeTypeField.clear()
        self.academicYearField.clear()
        self.semesterField.clear()
        
    def getMemberOrganizations(self):
        memberID = self.currentMember[0]
        try:
            self.cur.execute("""
                    SELECT
                        o.organization_id,
                        o.organization_name
                        
                    FROM organization o
                    JOIN member_org mo ON o.organization_id = mo.organization_id
                    JOIN member m ON m.member_id = mo.member_id
                    WHERE mo.member_id = ?
                """, (memberID, ))
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
    def onSubmit(self):
        memberID = self.currentMember[0]

        selectedOrg = self.selectedOrg.get()

        if (len(selectedOrg) == 0 or self.amountField.isEmpty() or self.dueDateField.isEmpty() or self.feeTypeField.isEmpty() or self.academicYearField.isEmpty() or self.semesterField.isEmpty()):
            messagebox.showerror("Error", "Please fill in the required fields")

        orgID = self.idLookup[selectedOrg]
        description = self.descriptionField.get().strip() or None
        amount = self.amountField.get().strip()
        dueDate = self.dueDateField.get().strip()
        feeType = self.feeTypeField.get().strip()
        academicYear = self.academicYearField.get().strip()
        semester = self.semesterField.get().strip()

        feeID = self.db.create_fee(
            amount=amount,
            due_date= dueDate,
            fee_type= feeType,
            payment_status= "Unpaid",
            academic_year= academicYear,
            date_issued=date.today().strftime("%Y-%m-%d"),
            description=description,
            member_id=memberID,
            organization_id=orgID,
            semester= semester,
        )

        if (feeID is None):
            messagebox.showerror("Error", "Failed to create fee")
            return
        else:
            messagebox.showinfo("Success", f"Fee of PHP {amount} was created for {self.currentMember[1]}!")
            self.goBack()

class ViewUnpaidMembers(Frame):
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

        Label(self, text="View Unpaid Members", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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
        self.academicYearVar.trace_add("write", self.on_filter_changed)
        self.semesterVar.trace_add("write", self.on_filter_changed)

        columns = ("Member ID", "Name", "Unpaid Amount", "Role", "Gender", "Degree Program", "Batch", "Status", "Committee", "A.Y.", "Semester")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True)
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        academic_year = self.academicYearVar.get().strip() or None
        semester = self.semesterVar.get() if hasattr(self, 'semesterVar') else None
        if semester == "All":
            semester = None

        data = self.db.get_all_unpaid_members(organization_id=organization_id, academic_year=academic_year, semester=semester)
        #m.member_id, m.name, f.amount, m.role, m.gender, m.degree_program, mo.batch, mo.status, mo.committee

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"],
                row["name"],row["amount"], row["role"], row["gender"],
                row["degree_program"],
                row["batch"], row["status"], row["committee"],
                row["academic_year"], row["semester"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}

class ViewExecutives(Frame):
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

        Label(self, text="View Executive Members", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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

        Label(options, text="Academic Year", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.academicYearVar = StringVar()
        academicYearFilter = Entry(options, textvariable=self.academicYearVar)
        academicYearFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.academicYearVar.trace_add("write", self.on_filter_changed)

        # m.member_id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year,
        columns = ("Member ID", "Name", "Organization", "Role", "Committee", "Academic Year")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        academic_year = self.academicYearVar.get().strip() or None

        # Fetch filtered data
        data = self.db.get_executives_by_year(organization_id=organization_id, academic_year=academic_year)
        # m.member_id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year,

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"],
                row["name"],row["organization_name"], row["role"], row["committee"],
                row["academic_year"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}

class ViewRoleHistory(Frame):
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

        Label(self, text="View Role History", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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

        Label(options, text="Role", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.roleVar = StringVar()
        roleFilter = Entry(options, textvariable=self.roleVar)
        roleFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.roleVar.trace_add("write", self.on_filter_changed)

        # m.member_id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year,
        columns = ("Member ID", "Name", "Organization", "Role", "Committee", "Academic Year", "Semester")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        role = self.roleVar.get().strip()

        # Fetch filtered data
        data = self.db.get_role_history(organization_id=organization_id, role=role)
        print(f"Returning: {data} from query: {organization_id} + {role}")
       # m.id, m.name, o.organization_name, mo.role, mo.committee, mo.academic_year, mo.semester

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"],
                row["name"],row["organization_name"], row["role"], row["committee"],
                row["academic_year"], row["semester"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}  
        
class ViewLatePayments(Frame):
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

        Label(self, text="View Late Payments", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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
        self.academicYearVar.trace_add("write", self.on_filter_changed)
        self.semesterVar.trace_add("write", self.on_filter_changed)
        columns = ("Member ID", "Name", "Amount", "Due Date", "Date Issued", "Fee Type", "Payment Status", "Pay Date", "Description", "Record ID", "Fee ID")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True)
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        academic_year = self.academicYearVar.get().strip() or None
        semester = self.semesterVar.get() if hasattr(self, 'semesterVar') else None
        if semester == "All":
            semester = None

        data = self.db.get_all_late_payments(organization_id=organization_id, academic_year=academic_year, semester=semester)
        #m.name
        #fee_id | amount | due_date   | date_issued | fee_type   | payment_status | pay_date   | description                            | member_id | record_id

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"],
                row["name"],row["amount"], row["due_date"], row["date_issued"],
                row["fee_type"],
                row["payment_status"], row["pay_date"], row["description"],
                row["record_id"], row["fee_id"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
class ViewActiveProportion(Frame):
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

        Label(self, text="View Active Proportion", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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

        Label(options, text="Semester", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.semesterVar = StringVar()
        semesterFilter = Entry(options, textvariable=self.semesterVar)
        semesterFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.semesterVar.trace_add("write", self.on_filter_changed)

        columns = ("Organization", "Academic Year", "Semester", "Active Percentage", "Inative Percentage")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        limit = self.semesterVar.get().strip()

        # Fetch filtered data
        data = self.db.get_organization_active_proportion(organization_id=organization_id, limit= limit)
       

        for row in data:
            self.tree.insert("", "end", values=(
                row["organization_name"],
                row["academic_year"],row["semester"], row["active_percentage"], row["inactive_percentage"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}

class ViewAlumniAsOf(Frame):
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

        Label(self, text="View Alumni As Of", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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

        Label(options, text="Given Date", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.dateVar = StringVar()
        dateFilter = Entry(options, textvariable=self.dateVar)
        dateFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.dateVar.trace_add("write", self.on_filter_changed)
        #  member_id | name              | gender | degree_program               | password | access_level | username
        columns = ("Member ID", "Name", "Gender", "Degree Program", "Password", "Access Level", "Username")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        date = self.dateVar.get().strip()

        # Fetch filtered data
        data = self.db.get_alumni_by_date(organization_id=organization_id, given_date=date)
       # member_id | name              | gender | degree_program               | password | access_level | username

        for row in data:
            self.tree.insert("", "end", values=(
                row["member_id"],
                row["name"],row["gender"], row["degree_program"], row["password"],
                row["access_level"], row["username"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
class ViewTotalPaidAndUnpaid(Frame):
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

        Label(self, text="View Total Fees", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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

        Label(options, text="Given Date", fg="Black", font=("Helvetica", 12)).pack(side=LEFT, padx=4)
        self.dateVar = StringVar()
        dateFilter = Entry(options, textvariable=self.dateVar)
        dateFilter.pack(side=LEFT, padx=4)

        self.selectedOrg.trace_add("write", self.on_filter_changed)
        self.dateVar.trace_add("write", self.on_filter_changed)
        #  member_id | name              | gender | degree_program               | password | access_level | username
        columns = ("Organization", "Paid Fees", "Unpaid Fees")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True) 
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        date = self.dateVar.get().strip()

        # Fetch filtered data
        data = self.db.get_fees_as_of_date(organization_id=organization_id, given_date=date)
       # member_id | name              | gender | degree_program               | password | access_level | username

        for row in data:
            self.tree.insert("", "end", values=(
                row["organization_name"],
                row["paid_fees"],row["unpaid_fees"]
            ))

    def goBack(self):
        self.master.show_page(ReportMenu)

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
class ViewHighestDebt(Frame):
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

        Label(self, text="View Highest Debt", fg="Black", font=("Helvetica", 18)).pack(pady=8)

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
        self.academicYearVar.trace_add("write", self.on_filter_changed)
        self.semesterVar.trace_add("write", self.on_filter_changed)
        columns = ("Member Name", "Debt")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        tree_h_scrollbar = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_h_scrollbar.set)

        self.tree.pack(fill=BOTH, expand=True)
        tree_h_scrollbar.pack(side=BOTTOM, fill=X)  

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)
        
        self.on_filter_changed()
        
    def on_filter_changed(self, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)

        org_key = self.selectedOrg.get()
        organization_id = self.idLookup.get(org_key) if org_key and org_key != "All" else None
        academic_year = self.academicYearVar.get().strip() or None
        semester = self.semesterVar.get() if hasattr(self, 'semesterVar') else None
        if semester == "All":
            semester = None

        data = self.db.get_highest_debt_as_of_date(organization_id=organization_id, academic_year=academic_year, semester=semester)
        #m.name
        #fee_id | amount | due_date   | date_issued | fee_type   | payment_status | pay_date   | description                            | member_id | record_id

        for row in data:
            self.tree.insert("", "end", values=(
                row["name1"],
                row["debt"]
            ))

    def getOrganizationsList(self):
        try:
            self.cur.execute("SELECT organization_id, organization_name FROM organization")
            rows = self.cur.fetchall()
            print("Rows fetched from DB:", rows)
            return {row['organization_id']: row['organization_name'] for row in rows}
        except mariadb.Error as e:
            print(f"Error in fetching organizations: {e}")
            return {}
        
    def goBack(self):
        self.master.show_page(ReportMenu)



class CreateMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user

        Label(self, text="Add/create a...", fg="Black",font=("Helvetica", 18)).pack(pady=(32,8))
        Button(self, text="Member",font=("Helvetica", 12), command=self.goToAddMemberPage).pack(pady=2.5)
        Button(self, text="Organization",font=("Helvetica", 12), command=self.goToCreateOrganizationPage).pack(pady=2.5)
        Button(self, text="Financial Record",font=("Helvetica", 12), command=self.goToAddFinancialRecordPage).pack(pady=2.5)
        Button(self, text="Back",font=("Helvetica", 12), command=self.goBack).pack(pady=2.5)
    
    def goToAddMemberPage(self):
        self.master.show_page(AddMemberPage)

    
    def goToCreateOrganizationPage(self):
        self.master.show_page(CreateOrganizationPage)

    def goToAddFinancialRecordPage(self):
        self.master.show_page(AddFinancialRecordPage)

    def goBack(self):
        self.master.show_page(AdminMenu)

class ReportMenu(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user

        Label(self, text="Generated report", fg="Black",font=("Helvetica", 18)).pack(pady=(32,8))
        Button(self, text="View Unpaid Members",font=("Helvetica", 12), command=self.goToViewUnpaid).pack(pady=2.5)
        Button(self, text="View Executives",font=("Helvetica", 12), command=self.goToViewExecutives).pack(pady=2.5)
        Button(self, text="View Role History",font=("Helvetica", 12), command=self.goToViewRoleHistory).pack(pady=2.5)
        Button(self, text="View Late Payments",font=("Helvetica", 12), command=self.goToViewLatePayments).pack(pady=2.5)
        Button(self, text="View Active vs Inactive Proportion",font=("Helvetica", 12), command=self.goToViewActiveProportion).pack(pady=2.5)
        Button(self, text="View Alumni As Of",font=("Helvetica", 12), command=self.goToViewAlumniAsOf).pack(pady=2.5)
        Button(self, text="View Total Paid and Unpaid",font=("Helvetica", 12), command=self.goToViewTotalPaidAndUnpaid).pack(pady=2.5)
        Button(self, text="View Highest Debt",font=("Helvetica", 12), command=self.goToViewHighestDebt).pack(pady=2.5)
        Button(self, text="Back",font=("Helvetica", 12), command=self.goBack).pack(pady=2.5)
    
    def goToViewUnpaid(self):
        self.master.show_page(ViewUnpaidMembers)

    def goToViewExecutives(self):
        self.master.show_page(ViewExecutives)
        
    def goToViewRoleHistory(self):
        self.master.show_page(ViewRoleHistory)

    def goToViewLatePayments(self):
        self.master.show_page(ViewLatePayments)
        pass

    def goToViewActiveProportion(self):
        self.master.show_page(ViewActiveProportion)
        pass

    def goToViewAlumniAsOf(self):
        self.master.show_page(ViewAlumniAsOf)
        pass

    def goToViewTotalPaidAndUnpaid(self):
        self.master.show_page(ViewTotalPaidAndUnpaid)
        pass

    def goToViewHighestDebt(self):
        self.master.show_page(ViewHighestDebt)
        pass

    def goBack(self):
        self.master.show_page(AdminMenu)
    
class LimitedEntry(Entry):
    def __init__(self, master=None, char_limit=10, **kwargs):
        self.char_limit = char_limit

        self.var = kwargs.pop("textvariable", StringVar())

        super().__init__(master, textvariable=self.var, **kwargs)

        vcmd = self.register(self.on_validate)
        self.config(validate="key", validatecommand=(vcmd, '%P'))

    def on_validate(self, proposed_text):
        return len(proposed_text) <= self.char_limit

    def set_limit(self, new_limit):
        self.char_limit = new_limit
    
    def get(self) ->  str:
        return self.var.get()
    
    def isEmpty(self):
        return len(self.var.get()) == 0
    
    def clear(self):
        self.var.set("")
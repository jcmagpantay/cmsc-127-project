from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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
       addMemberPage = AddMemberPage(self.master)
       self.master.screens[AddMemberPage] = addMemberPage
       addMemberPage.place(relwidth=1, relheight=1)
       self.master.show_screen(AddMemberPage)

class AddMemberPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = self.master.user
        Label(self, text="Add A Member", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Label(self, text="Name", fg="Black",font=("Helvetica", 18)).pack(pady=10)
        Text(self, height=5, width=40).pack(pady=2.5)
        Button(self, text="Add Member",font=("Helvetica", 12)).pack(pady=2.5)
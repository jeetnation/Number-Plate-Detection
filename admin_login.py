from tkinter import *               #pip import tkinter
from tkcalendar import *
from tkinter import messagebox
from PIL import Image, ImageTk      #pip import pillow
from database_connect import mysql_CRUD
from OTP_send import sent_email
import os
import re


class admin_login:
    def __init__(self, root):
        self.root = root
        self.root.title("Mall of India")
        self.root.geometry("1350x700+0+0")
        self.root.resizable(False, False)

        #=====Title=======
        title_frame = Frame(self.root, bg="#010c48")
        title_frame.place(x=0, y=0, height=100, width=1350)
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(title_frame, text="Mall Of India", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=50, y=12)

        #=====Button in Frame====
        self.btn_trans = Button(title_frame, command=self.change_login, text="Security Login", bg="red")
        self.btn_trans.place(x=1230, y=12, width=100, height=70)

        #===Login Frame=====
        frame_login = Frame(self.root, bg="white")
        frame_login.place(x=450, y=200, height=340, width=500)

        title = Label(frame_login, text="Login Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white")
        title.place(x=90, y=30)

        desc = Label(frame_login, text="Admin Login Area", font=("Goudy old style", 15, "bold"), fg="#d25d17", bg="white")
        desc.place(x=90, y=100)

        user_lbl = Label(frame_login, text="Admin ID:", font=("Goudy old style", 15, "bold"), fg="gray", bg="white")
        user_lbl.place(x=90, y=140)

        self.user_entry = Entry(frame_login, font=("Goudy old style", 15), bg="lightgray")
        self.user_entry.place(x=90, y=170, width=350, height=35)

        pass_lbl = Label(frame_login, text="Admin Password:", font=("Goudy old style", 15, "bold"), fg="gray", bg="white")
        pass_lbl.place(x=90, y=210)

        self.pass_entry = Entry(frame_login, show="*", font=("Goudy old style", 15), bg="lightgray")
        self.pass_entry.place(x=90, y=240, width=350, height=35)

        #======Forget Password=====
        self.forgot_pass = Button(frame_login, text="-Forgot Password-", command=self.forgot_window, bd=0, bg="white", fg="#d77337", font=("times new roman", 12))
        self.forgot_pass.place(x=90, y=280)

        #======Register as Admin======
        self.register_admin = Button(frame_login, text="-Register-", command=self.register_admin, bd=0, bg="white", fg="#d77337",  font=("times new roman", 12))
        self.register_admin.place(x=280, y=280)

        #====login btn====
        self.login_btn = Button(self.root, text="Login", command=self.login_sec, fg="white", bg="#d77337", font=("times new roman", 20))
        self.login_btn.place(x=600, y=530, width=180, height=40)

    def change_login(self):
        self.root.destroy()
        os.system("python security_login.py")

    def login_sec(self):
        if self.user_entry.get() == "" or self.pass_entry.get() == "":
            messagebox.showerror('Error', "All Fields should be Written", parent=self.root)
        else:
            conn = mysql_CRUD()
            try:
                user_details = conn.check_user(self.user_entry.get(), self.pass_entry.get(), "admin_table")
                if user_details == None:
                    messagebox.showerror('Error', "Invalid Admin ID AND Password", parent=self.root)
                else:
                    self.root.destroy()
                    os.system("python admin_side.py")
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def forgot_window(self):
        conn = mysql_CRUD()
        try:
            if self.user_entry.get() == "":
                messagebox.showerror('Error', "Admin Id must be Required", parent=self.root)
            else:
                sec_email = conn.check_forget(self.user_entry.get(), "admin_table")
                if sec_email == None:
                    messagebox.showerror('Error', "Invalid Admin ID, try Again", parent=self.root)
                else:
                    #=====forget window========
                    self.var_otp = StringVar()
                    self.var_new = StringVar()
                    self.var_confirm = StringVar()

                    #call Send Email function
                    self.mail_s = sent_email(sec_email[0])
                    self.OTP_compare = otp = self.mail_s.Random_OTP(6)
                    self.mail_send = self.mail_s.Sent_mail(otp)

                    if self.mail_send == 'f':
                        messagebox.showerror('Error', "Connection Error, try again", parent=self.root)
                    else:
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title_lbl = Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

                        reset_lbl = Label(self.forget_win, text="Enter OTP sent on registered Email", font=("times new roman", 15)).place(x=20, y=60)
                        self.reset_entry = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg='lightyellow').place(x=20, y=100, width=250, height=30)
                        self.reset_btn = Button(self.forget_win, command=self.validate_otp, text="SUBMIT", font=("times new roman", 15), bg='lightblue')
                        self.reset_btn.place(x=280, y=100, width=100, height=30)

                        new_pass_lbl = Label(self.forget_win, text='New Password', font=("times new roman", 15)).place(x=20, y=160)
                        self.new_pass_entry = Entry(self.forget_win, show="*", textvariable=self.var_new, font=("times new roman", 15), bg='lightyellow').place(x=20, y=190, width=250, height=30)

                        confirm_lbl = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15)).place(x=20, y=230)
                        self.confirm_entry = Entry(self.forget_win, show="*", textvariable=self.var_confirm, font=("times new roman", 15), bg='lightyellow').place(x=20, y=255, width=250, height=30)

                        self.change_btn = Button(self.forget_win, command=self.change_pass, text="UPDATE", state=DISABLED, font=("times new roman", 15), bg='lightblue')
                        self.change_btn.place(x=150, y=300, width=100, height=30)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def validate_otp(self):
        if self.OTP_compare == self.var_otp.get():
            self.change_btn.config(state=NORMAL)
            self.reset_btn.config(state=DISABLED)
        else:
            messagebox.showerror('Error', "Invalid OTP, Try Again", parent=self.forget_win)

    def change_pass(self):
        if self.var_new.get() == "" or self.var_confirm.get() == "":
            messagebox.showerror('Error', "Password is Required", parent=self.forget_win)
        elif self.var_new.get() != self.var_confirm.get():
            messagebox.showerror('Error', "Both Passwords should be Same", parent=self.forget_win)
        else:
            conn = mysql_CRUD()
            try:
                update_pass = conn.update_pass(self.var_confirm.get(), self.user_entry.get(), "admin_table")
                messagebox.showinfo("Message", "Your Password has changed", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def register_admin(self):
        self.register_win = Toplevel(self.root)
        self.register_win.title('RESET PASSWORD')
        self.register_win.geometry('650x500')
        self.register_win.focus_force()

        self.id = StringVar()
        self.name = StringVar()
        self.email_id = StringVar()
        self.phone_no = IntVar()
        self.password = StringVar()

        register_lbl = Label(self.register_win, text="Admin Register", font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

        id_lbl = Label(self.register_win, text="Admin ID:", font=("times new roman", 15)).place(x=20, y=50)
        name_lbl = Label(self.register_win, text="Name:", font=("times new roman", 15)).place(x=20, y=90)
        email_lbl = Label(self.register_win, text="Email ID", font=("times new roman", 15)).place(x=20, y=140)
        phone_lbl = Label(self.register_win, text="Phone No:", font=("times new roman", 15)).place(x=20, y=190)
        DOB_lbl = Label(self.register_win, text="DOB:", font=("times new roman", 15)).place(x=20, y=240)
        Pass_lbl = Label(self.register_win, text="Password:", font=("times new roman", 15)).place(x=20, y=290)

        self.id_entry = Entry(self.register_win, textvariable=self.id, font=("times new roman", 15), bg='lightyellow').place(x=150, y=50, width=150, height=30)
        self.name_entry = Entry(self.register_win, textvariable=self.name, font=("times new roman", 15), bg='lightyellow').place(x=150, y=90, width=150, height=30)
        self.email_entry = Entry(self.register_win, textvariable=self.email_id, font=("times new roman", 15), bg='lightyellow').place(x=150, y=140, width=150, height=30)
        self.phone_entry = Entry(self.register_win, textvariable=self.phone_no, font=("times new roman", 15), bg='lightyellow').place(x=150, y=190, width=150, height=30)
        self.DOB_button = Button(self.register_win, text="Select Date", command=self.select_date, font=("times new roman", 15), bg='lightyellow')
        self.DOB_button.place(x=150, y=240, width=150, height=30)
        self.Pass_entry = Entry(self.register_win, textvariable=self.password, font=("times new roman", 15), bg='lightyellow').place(x=150, y=290, width=150, height=30)

        self.submit_btn = Button(self.register_win, text="Register", command=self.insert_values, font=("times new roman", 15), bg='lightblue')
        self.submit_btn.place(x=190, y=400)

    def select_date(self):
        self.date = Toplevel(self.register_win)
        self.date.title("Select Date")
        self.date.geometry("600x400")

        self.myCal = Calendar(self.date, selectmode="day", year=2021, month=7, day=22, date_pattern='yyyy/mm/dd')
        self.myCal.pack(pady=20, fill="both", expand=True)

        self.my_button = Button(self.date, text="Set Date", command=lambda: self.grab_date(self.myCal.get_date()))
        self.my_button.pack(pady=20)

    def grab_date(self, date):
        self.DOB_var = date
        self.DOB_button.config(state=DISABLED)
        self.date.destroy()

    def insert_values(self):
        conn = mysql_CRUD()
        try:
            email_check = self.check_email()
            phone_no = self.phone_no.get()
            if self.id.get() == "" or self.name.get() == "" or self.email_id.get() == "" or self.phone_no.get() == 0 or self.password.get() == "" or self.DOB_var == "":
                messagebox.showerror('Error', "All Fields are Required", parent=self.register_win)
            elif email_check == "NO":
                messagebox.showerror('Error', "Enter a valid email", parent=self.register_win)
            elif len(str(phone_no)) < 10:
                messagebox.showerror('Error', "Invalid Phone Number", parent=self.register_win)
            else:
                conn.insert_admin(self.id.get(), self.name.get(), self.email_id.get(), self.phone_no.get(), self.DOB_var, self.password.get())
                messagebox.showinfo('Info', "You have ben Registered", parent=self.root)
                self.register_win.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.register_win)

    def check_email(self):
        email = self.email_id.get()
        regex ="^[a-z0-9]+[\.'\-]*[a-z0-9]+@(gmail|googlemail)\.com$"
        if (re.match(regex, email)):
            return "YES"
        else:
            return "NO"


if __name__ == "__main__":
    root = Tk()
    obj = admin_login(root)
    root.mainloop()

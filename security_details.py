from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from database_connect import mysql_CRUD
import qrcode
import re
import os

class sec_details:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("MAll OF INDIA - SECURITY DETAILS")
        self.root.config(bg="white")
        self.root.focus_force()

        #all Vairables====
        self.var_searchby = StringVar()
        self.var_searchtxt =StringVar()

        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_phone = IntVar()
        self.var_pass = StringVar()

        #=====Search Frame====
        search_frame = LabelFrame(self.root, text="Search Security", font=("goudy old style", 12, "bold"), bd=2, bg="white", relief=RIDGE)
        search_frame.place(x=250, y=20, width=600, height=70)

        #====options====
        search_cb = ttk.Combobox(search_frame, textvariable=self.var_searchby, values=("Select", "Security_id", "Name"), state='readonly', justify=CENTER, font=("times new roman", 15))
        search_cb.place(x=10, y=10, width=180)
        search_cb.current(0)

        search_txt = Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)

        search_btn = Button(search_frame, command=self.search_val, cursor="hand2", text="Search", font=("goudy old style", 15), bg="#4caf50", fg="white")
        search_btn.place(x=410, y=9, width=150, height=30)

        #=======Title==========
        title_lbl = Label(self.root, text="Security Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        #========content========
        id_lbl = Label(self.root, text="Security ID:", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        name_lbl = Label(self.root, text="Name:", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        phone_lbl = Label(self.root, text="Phone No:", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        self.id_entry = Entry(self.root, state=NORMAL, textvariable=self.var_id, font=("goudy old style", 15), bg="white")
        self.id_entry.place(x=150, y=150, width=180)
        self.name_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_name, font=("goudy old style", 15), bg="white")
        self.name_entry.place(x=450, y=150, width=180)
        self.phone_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_phone, font=("goudy old style", 15), bg="white")
        self.phone_entry.place(x=850, y=150, width=180)

        email_lbl = Label(self.root, text="Email ID:", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        DOB_lbl = Label(self.root, text="DOB:", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        pass_lbl = Label(self.root, text="Password:", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        self.email_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_email, font=("goudy old style", 15), bg="white")
        self.email_entry.place(x=150, y=190, width=180)
        self.DOB_button = Button(self.root, state=NORMAL,  text="Select Date", command=self.select_date, font=("times new roman", 15), bg='lightyellow')
        self.DOB_button.place(x=450, y=190, width=180)
        self.pass_entry = Entry(self.root, state=DISABLED, show="*",  textvariable=self.var_pass, font=("goudy old style", 15), bg="white")
        self.pass_entry.place(x=850, y=190, width=180)

        #======Buttons======
        self.save_btn = Button(self.root, command=self.insert_sec, cursor="hand2", text="SAVE", font=("goudy old style", 15), state=NORMAL, bg="#2196f3", fg="white")
        self.update_btn = Button(self.root, command=self.update_details, cursor="hand2", text="UPDATE", state=DISABLED, font=("goudy old style", 15), bg="#2196f3", fg="white")
        self.delete_btn = Button(self.root, state=DISABLED, command=self.delete_values, cursor="hand2", text="DELETE", font=("goudy old style", 15), bg="#2196f3", fg="white")
        self.clear_btn = Button(self.root, state=NORMAL, command=self.clear_values, cursor="hand2", text="CLEAR", font=("goudy old style", 15), bg="#2196f3", fg="white")

        self.save_btn.place(x=150, y=250, width=150, height=30)
        self.update_btn.place(x=350, y=250, width=150, height=30)
        self.delete_btn.place(x=550, y=250, width=150, height=30)
        self.clear_btn.place(x=750, y=250, width=150, height=30)

        #===Security Details====
        sec_frame = Frame(self.root, bd=3, relief=RIDGE)
        sec_frame.place(x=0, y=300, relwidth=1, height=200)

        scrolly = Scrollbar(sec_frame, orient=VERTICAL)
        scrollx = Scrollbar(sec_frame, orient=HORIZONTAL)

        self.Security_table = ttk.Treeview(sec_frame, columns=("user_id", "user_name", "phone_no", "email_id", "user_DOB", "user_pass"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Security_table.xview)
        scrolly.config(command=self.Security_table.yview)

        self.Security_table.heading("user_id", text="Security_id")
        self.Security_table.heading("user_name", text="Name")
        self.Security_table.heading("phone_no", text="Phone No")
        self.Security_table.heading("email_id", text="Email ID")
        self.Security_table.heading("user_DOB", text="DOB")
        self.Security_table.heading("user_pass", text="Password")

        self.Security_table.column("user_id", width=100)
        self.Security_table.column("user_name", width=150)
        self.Security_table.column("phone_no", width=200)
        self.Security_table.column("email_id", width=250)
        self.Security_table.column("user_DOB", width=80)
        self.Security_table.column("user_pass", width=150)
        self.Security_table["show"] = "headings"
        self.Security_table.pack(fill=BOTH, expand=1)
        self.Security_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #=====functions======
    def insert_sec(self):
        conn = mysql_CRUD()
        try:
            phone_no = int(self.var_phone.get())
            email_check = self.check_email()
            if self.var_id.get() == "" or self.var_name.get() == "" or self.var_email.get() == "" or self.var_phone.get() == 0 or self.var_pass.get() == "" or self.DOB_var == "":
                messagebox.showerror('Error', "All Fields should be Entered", parent=self.root)
            elif len(str(phone_no)) < 10:
                messagebox.showerror('Error', "Invalid Phone Number", parent=self.root)
            elif email_check == "NO":
                messagebox.showerror('Error', "Enter a valid email", parent=self.root)
            else:
                conn.insert_security(self.var_id.get(), self.var_name.get(), self.var_phone.get(), self.var_email.get(), self.DOB_var, self.var_pass.get())
                self.create_ID()
                messagebox.showinfo('Info', "Security Registered and ID Card Generated", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}")

    def show(self):
        conn = mysql_CRUD()
        try:
            rows = conn.select_user()
            self.Security_table.delete(*self.Security_table.get_children())
            for row in rows:
                self.Security_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def select_date(self):
        self.date = Toplevel(self.root)
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

    def get_data(self, ev):
        f = self.Security_table.focus()
        content = (self.Security_table.item(f))
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_phone.set(row[2])
        self.var_email.set(row[3])
        self.DOB_var = row[4]
        self.var_pass.set(row[5])
        self.update_btn.config(state=NORMAL)
        self.delete_btn.config(state=NORMAL)
        self.id_entry.config(state=DISABLED)
        self.name_entry.config(state=DISABLED)
        self.DOB_button.config(state=DISABLED)
        self.save_btn.config(state=DISABLED)

    def update_details(self):
        conn = mysql_CRUD()
        try:
            phone_no = self.var_phone.get()
            email_check = self.check_email()
            if self.var_id.get() == "" or self.var_name.get() == "" or self.var_email.get() == "" or self.var_phone.get() == 0 or self.var_pass.get() == "" or self.DOB_var == "":
                messagebox.showerror('Error', "All Fields should be Entered", parent=self.root)
            elif email_check == "NO":
                messagebox.showerror('Error', "Enter a valid email", parent=self.root)
            elif len(str(phone_no)) < 10:
                messagebox.showerror('Error', "Invalid Phone Number", parent=self.root)
            else:
                conn.update_security(self.var_email.get(), self.var_phone.get(), self.var_id.get())
                self.create_ID()
                messagebox.showinfo('Info', "Security Details Updated and New ID Card Generated", parent=self.root)
                self.clear_values()
                self.show()
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def check_email(self):
        email = self.var_email.get()
        regex ="^[a-z0-9]+[\.'\-]*[a-z0-9]+@(gmail|googlemail)\.com$"
        if (re.match(regex, email)):
            return "YES"
        else:
            return "NO"

    def delete_values(self):
        conn = mysql_CRUD()
        try:
            op = messagebox.askyesno('Confirm Delete', "Do you want to Delete", parent=self.root)
            if op == True:
                conn.delete_security(self.var_id.get())
                os.remove("ID_Card/" + self.var_id.get() + '.png')
                messagebox.showinfo('Info', "Record Deleted", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def clear_values(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.DOB_var = ""
        self.var_pass.set("")
        self.update_btn.config(state=NORMAL)
        self.id_entry.config(state=NORMAL)
        self.delete_btn.config(state=NORMAL)
        self.name_entry.config(state=NORMAL)
        self.DOB_button.config(state=NORMAL)
        self.DOB_button.config(state=NORMAL)

        self.show()

     #========serach function=========
    def search_val(self):
        conn = mysql_CRUD()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror('Error', "Please Select a Value", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror('Error', "Search should be Required", parent=self.root)
            else:
                rows = conn.get_security(self.var_searchby.get(), self.var_searchtxt.get())
                if len(rows) != 0:
                    self.Security_table.delete(*self.Security_table.get_children())
                    for row in rows:
                        self.Security_table.insert('', END, values=row)
                else:
                    messagebox.showerror('Error', "No Records Found")
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def create_ID(self):
        #self.var_id.get(), self.var_name.get(), self.var_phone.get(), self.var_email.get(), self.DOB_var, self.var_pass.get()
        image = Image.new('RGB', (1000, 800), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype('arial.ttf', size=45)

        # starting position of the message
        company = "MALL OF INDIA"
        (x, y) = (50, 50)
        color = 'rgb(0, 0, 0)'  # black color
        font = ImageFont.truetype('arial.ttf', size=80)
        draw.text((x, y), company, fill=color, font=font)

        #======For ID========
        (x, y) = (50, 150)
        id = self.var_id.get()
        mss_id = 'ID: ' + id
        color = 'rgb(0, 0, 0)'  # black color
        font = ImageFont.truetype('arial.ttf', size=45)
        draw.text((x, y), mss_id, fill=color, font=font)

        #====== For the Name======
        (x, y) = (50, 250)
        name = self.var_name.get()
        mss_name = 'Name: ' + name
        color = 'rgb(0, 0, 0)'  # black color
        font = ImageFont.truetype('arial.ttf', size=45)
        draw.text((x, y), mss_name, fill=color, font=font)

        #======For the email======
        (x, y) = (50, 350)
        email = self.var_email.get()
        mss_email = 'Email: ' + email
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), mss_email, fill=color, font=font)

        # For the DOB
        (x, y) = (50, 450)
        dob = self.DOB_var
        mss_dob = 'DOB: ' + dob
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), mss_dob, fill=color, font=font)

        # For the Mob No
        (x, y) = (50, 550)
        phone_no = str(self.var_phone.get())
        fNo = 'Mobile Number: ' + phone_no
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), fNo, fill=color, font=font)

        # save the edited image
        image.save("ID_Card/" + id + '.png')
        QR = qrcode.make(id)
        ID = Image.open("ID_Card/" + id + '.png')
        ID.paste(QR, (650, 60))
        ID.save("ID_Card/" + id + '.png')

if __name__ == "__main__":
    root = Tk()
    obj = sec_details(root)
    root.mainloop()
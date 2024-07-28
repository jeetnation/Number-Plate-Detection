from tkinter import *
from tkinter import ttk, messagebox
import os
from database_connect import mysql_CRUD

class car_details:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("MAll OF INDIA - CAR DETAILS")
        self.root.config(bg="white")
        self.root.focus_force()

        #all Vairables====
        self.var_searchby = StringVar()
        self.var_searchtxt =StringVar()

        self.var_srno = StringVar()
        self.var_receipt = StringVar()
        self.var_num_plate = StringVar()
        self.var_state_name = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        #=====Search Frame====
        search_frame = LabelFrame(self.root, text="Search Car", font=("goudy old style", 12, "bold"), bd=2, bg="white", relief=RIDGE)
        search_frame.place(x=250, y=20, width=600, height=70)

        #====options====
        search_cb = ttk.Combobox(search_frame, textvariable=self.var_searchby, values=("Select", "Number Plate", "State"), state='readonly', justify=CENTER, font=("times new roman", 15))
        search_cb.place(x=10, y=10, width=180)
        search_cb.current(0)

        search_txt = Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)

        search_btn = Button(search_frame, command=self.search_val, cursor="hand2", text="Search", font=("goudy old style", 15), bg="#4caf50", fg="white")
        search_btn.place(x=410, y=9, width=150, height=30)

        #=======Title==========
        title_lbl = Label(self.root, text="Car Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        #========content========
        sr_lbl = Label(self.root, text="Sr No:", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        numPlate_lbl = Label(self.root, text="Number Plate:", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        Receipt_lbl = Label(self.root, text="Receipt:", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        self.sr_entry = Entry(self.root, state=NORMAL, textvariable=self.var_srno, font=("goudy old style", 15), bg="white")
        self.sr_entry.place(x=150, y=150, width=180)
        self.numPlate_entry = Entry(self.root, state=NORMAL, textvariable=self.var_num_plate, font=("goudy old style", 15), bg="white")
        self.numPlate_entry.place(x=450, y=150, width=180)
        self.Receipt_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_receipt, font=("goudy old style", 15), bg="white")
        self.Receipt_entry.place(x=850, y=150, width=180)

        state_lbl = Label(self.root, text="State:", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        date_lbl = Label(self.root, text="Date:", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        time_lbl = Label(self.root, text="Time:", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        self.state_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_state_name, font=("goudy old style", 15), bg="white")
        self.state_entry.place(x=150, y=190, width=180)
        self.date_entry = Entry(self.root, state=NORMAL, textvariable=self.var_date, text="Select Date", font=("goudy old style", 15), bg="white")
        self.date_entry.place(x=450, y=190, width=180)
        self.time_entry = Entry(self.root, state=NORMAL,  textvariable=self.var_time, font=("goudy old style", 15), bg="white")
        self.time_entry.place(x=850, y=190, width=180)

        #======Buttons======
        self.update_btn = Button(self.root, command=self.update_details, cursor="hand2", text="UPDATE", state=DISABLED, font=("goudy old style", 15), bg="#2196f3", fg="white")
        self.delete_btn = Button(self.root, state=DISABLED, command=self.delete_values, cursor="hand2", text="DELETE", font=("goudy old style", 15), bg="#2196f3", fg="white")
        self.clear_btn = Button(self.root, state=NORMAL, command=self.clear_values, cursor="hand2", text="CLEAR", font=("goudy old style", 15), bg="#2196f3", fg="white")

        self.update_btn.place(x=150, y=250, width=150, height=30)
        self.delete_btn.place(x=350, y=250, width=150, height=30)
        self.clear_btn.place(x=550, y=250, width=150, height=30)

        #===Car Details====
        sec_frame = Frame(self.root, bd=3, relief=RIDGE)
        sec_frame.place(x=0, y=300, relwidth=1, height=200)

        scrolly = Scrollbar(sec_frame, orient=VERTICAL)
        scrollx = Scrollbar(sec_frame, orient=HORIZONTAL)

        self.car_table = ttk.Treeview(sec_frame, columns=("sr_no", "reciept_no", "number_plate", "state_name", "entry_date", "entry_time"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.car_table.xview)
        scrolly.config(command=self.car_table.yview)

        self.car_table.heading("sr_no", text="Serial_no")
        self.car_table.heading("reciept_no", text="Reciept Number")
        self.car_table.heading("number_plate", text="Number Plate")
        self.car_table.heading("state_name", text="State")
        self.car_table.heading("entry_date", text="Date")
        self.car_table.heading("entry_time", text="Time")

        self.car_table.column("sr_no", width=100)
        self.car_table.column("reciept_no", width=200)
        self.car_table.column("number_plate", width=200)
        self.car_table.column("state_name", width=200)
        self.car_table.column("entry_date", width=80)
        self.car_table.column("entry_time", width=80)
        self.car_table["show"] = "headings"
        self.car_table.pack(fill=BOTH, expand=1)
        self.car_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #=====functions======
    def show(self):
        conn = mysql_CRUD()
        try:
            rows = conn.select_cars()
            self.car_table.delete(*self.car_table.get_children())
            for row in rows:
                self.car_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.car_table.focus()
        content = (self.car_table.item(f))
        row = content['values']
        self.var_srno.set(row[0])
        self.var_receipt.set(row[1])
        self.var_num_plate.set(row[2])
        self.var_state_name.set(row[3])
        self.var_date.set(row[4])
        self.var_time.set(row[5])
        self.update_btn.config(state=NORMAL)
        self.delete_btn.config(state=NORMAL)
        self.sr_entry.config(state=DISABLED)
        self.Receipt_entry.config(state=DISABLED)
        self.date_entry.config(state=DISABLED)
        self.time_entry.config(state=DISABLED)

    def update_details(self):
        conn = mysql_CRUD()
        try:
            phone_no = self.var_phone.get()
            email_check = self.check_email()
            if self.var_srno.get() == "" or self.var_num_plate.get() == "" or self.var_receipt.get() == "" or self.var_state_name.get() == "" or self.var_date.get() == "" or self.var_time.get() == "":
                messagebox.showerror('Error', "All Fields should be Entered", parent=self.root)
            else:
                conn.update_car(self.var_num_plate, self.var_state_name.get(), self.var_srno.get())
                messagebox.showinfo('Info', "Car Details Updated", parent=self.root)
                self.clear_values()
                self.show()
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def delete_values(self):
        conn = mysql_CRUD()
        try:
            op = messagebox.askyesno('Confirm Delete', "Do you want to Delete", parent=self.root)
            if op == True:
                conn.delete_car(self.var_srno.get())
                messagebox.showinfo('Info', "Record Deleted", parent=self.root)
                os.remove("Num_plates/" + self.var_num_plate.get() + '.jpg')
                os.remove("Car_photos/" + self.var_num_plate.get() + '.jpg')
                self.show()
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def clear_values(self):
        self.var_srno.set("")
        self.var_num_plate.set("")
        self.var_receipt.set("")
        self.var_state_name.set("")
        self.var_date.set("")
        self.var_time.set("")
        self.update_btn.config(state=NORMAL)
        self.sr_entry.config(state=NORMAL)
        self.delete_btn.config(state=NORMAL)
        self.Receipt_entry.config(state=NORMAL)
        self.date_entry.config(state=NORMAL)
        self.time_entry.config(state=NORMAL)

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
                rows = conn.get_car(self.var_searchby.get(), self.var_searchtxt.get())
                if len(rows) != 0:
                    self.car_table.delete(*self.car_table.get_children())
                    for row in rows:
                        self.car_table.insert('', END, values=row)
                else:
                    messagebox.showerror('Error', "No Records Found")
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = car_details(root)
    root.mainloop()
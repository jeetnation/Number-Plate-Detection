from tkinter import *
from tkinter import messagebox
from database_connect import mysql_CRUD
import time
import string
import random
from datetime import datetime, date
from PIL import Image, ImageTk

class exit_module:
    def __init__(self, root):
        self.root = root
        self.root.title("Mall of India | Exit")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")
        self.root.focus_force()

        self.icon_title = PhotoImage(file="images/logo1.png")
        self.title_lbl = Label(self.root, text="EXIT | Thank You", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        self.title_lbl.place(x=0, y=0, relwidth=1, height=70)

        lbl_welcome = Label(self.root, text="Thank You for shopping", font=("times new roman", 40), fg="blue").place(x=280, y=100)

        self.var_recipt = StringVar()
        self.var_r = IntVar()

        lbl_enter = Label(self.root, text="Enter Receipt Number: ", font=("times new roman", 20), fg="blue", bg="white").place(x=70, y=180)
        entry_num = Entry(self.root, textvariable=self.var_recipt, font=("times new roman", 20), bg="lightyellow").place(x=350, y=180)

        self.btn_search = Button(self.root, command=self.seeall, text="Search", font=("times new roman", 20), fg="blue", bg="white")
        self.btn_search.place(x=650, y=180, height=50, width=150)

        lbl_mode = Label(self.root, text="Select Payment Mode:", font=("times new roman", 20), fg="blue", bg="white").place(x=70, y=250)
        Radiobutton(self.root, text="Cash", variable=self.var_r, value=1).place(x=450, y=250)
        Radiobutton(self.root, text="Paytm", variable=self.var_r, value=2).place(x=500, y=250)

        self.lbl_details = Label(self.root, text="Receipt: \n Entry Time: \n Exit Time: ", font=("times new roman", 20), fg="blue", bg="white")
        self.lbl_details.place(x=100, y=300)

        self.btn_clear = Button(self.root, state=NORMAL, text="CLEAR", bg="red", command=self.clear)
        self.btn_clear.place(x=250, y=400, height=50, width=150)

        self.btn_enter = Button(self.root, state=NORMAL, text="ENTER", bg="red", command=self.enter)
        self.btn_enter.place(x=490, y=400, height=50, width=150)

    def clear(self):
        self.var_r.set(0)
        self.var_recipt.set("")
        self.lbl_details.config(text="Receipt: \n Entry Time: \n Exit Time: ")

    def seeall(self):
        conn = mysql_CRUD()
        try:
            if self.var_recipt.get() == "" or self.var_r.get() == 0:
                messagebox.showerror('Error', "Enter The Values", parent=self.root)
            else:
                self.time_n = time.strftime("%I:%M:%S")
                time_e = conn.get_time(self.var_recipt.get())
                self.lbl_details.config(text=f"Receipt: {self.var_recipt.get()}\n Entry Time: {time_e}\n Exit Time: {self.time_n}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def enter(self):
        conn = mysql_CRUD()
        try:
            pay_no = self.get_rand_number()
            today = date.today()
            d = today.strftime("%Y-%m-%d")
            messagebox.showinfo('Pay', "Pay with Paytm", parent=self.root)
            if self.var_r.get() == 1:
                conn.insert_pay(pay_no, self.var_recipt.get(), self.var_r.get(), 0, d, self.time_n)
            else:
                paytm_pay = Toplevel(self.root)
                paytm_pay.title("Pay With Paytm")
                paytm_pay.geometry("755x680")
                self.img = ImageTk.PhotoImage(Image.open("images/paytm_pay.jpg"))
                lbl_image = Label(paytm_pay, image=self.img).place(x=0, y=0)
                paytm_pay.after(30000, paytm_pay.destroy)
                conn.insert_pay(pay_no, self.var_recipt.get(), self.var_r.get(), 0, d, self.time_n)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_rand_number(self):
        upper = string.ascii_uppercase
        num = string.digits
        all = upper + num
        length = 5
        temp = random.sample(all, length)
        password = "".join(temp)
        return password

if __name__ == "__main__":
    root = Tk()
    obj = exit_module(root)
    root.mainloop()
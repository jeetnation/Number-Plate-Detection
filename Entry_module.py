from tkinter import *                   #pip import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk          #pip import pillow
from database_connect import mysql_CRUD
import os
import time
from datetime import date


class entry_module:
    def __init__(self, root):
        self.root = root
        self.root.title("Mall of India | Entry")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")
        self.root.focus_force()

        self.icon_title = PhotoImage(file="images/logo1.png")
        self.title_lbl = Label(self.root, text="Entry | Parking Available [0]", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        self.title_lbl.place(x=0, y=0, relwidth=1, height=70)

        lbl_welcome = Label(self.root, text="Welcome to Mall of India", font=("times new roman", 40), fg="blue").place(x=250, y=100)

        self.lbl_park_available = Label(self.root, text="Parking Available:", font=("times new roman", 20), fg="red")
        self.lbl_park_available.place(x=200, y=200)

        self.btn_entry = Button(self.root, state=NORMAL, command=self.ssa, text="Click Photo", bg="green", fg="black")
        self.btn_entry.place(x=350, y=250, height=80, width=150)

        self.update_details()

    def update_details(self):
        conn = mysql_CRUD()
        try:
            parking_num = conn.get_parking()
            parking_num = int(parking_num)
            park_avail = 100 - parking_num
            self.title_lbl.config(text=f"Entry | Parking Available [{park_avail}]")
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)
        if parking_num < 0:
            self.lbl_park_available.config(text="Parking not Available")
            self.btn_entry.config(state=DISABLED)

    def ssa(self):
        os.system("python ahsh.py")

if __name__ == "__main__":
    root = Tk()
    obj = entry_module(root)
    root.mainloop()
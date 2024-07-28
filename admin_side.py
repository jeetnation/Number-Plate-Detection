from tkinter import * #pip import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk #pip import pillow
from database_connect import mysql_CRUD
from security_details import sec_details
import os
import time
from datetime import date
from car_details import car_details

class admin_side:
    def __init__(self, root):
        self.root = root
        self.root.title("MALL OF INDIA - ADMIN")
        self.root.geometry("1350x700+0+0")

        self.icon_title = PhotoImage(file="images/logo1.png")
        title_lbl = Label(self.root, text="Mall Of India", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)
        self.root.config(bg="white")
        # ===btn_l0gout===
        btn_logout = Button(self.root, command=self.logout_btn, text="Logout", font=("times new roman", 15, "bold"), cursor="hand2", bg="yellow").place(x=1150, y=10, height=50, width=150)

        # ===clock===
        self.clock_lbl = Label(self.root, text="Welcome to Mall of India \t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS", font=("times new roman", 15), fg="white", bg="#4d636d")
        self.clock_lbl.place(x=0, y=70, relwidth=1, height=30)

        #=====Left Menu====
        self.MenuLogo = Image.open("images/mall_logo.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.ANTIALIAS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=590)

        lbl_MenuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_MenuLogo.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="images/side.png")
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)
        btn_security = Button(LeftMenu, command=self.security_details, text="Security", image=self.icon_side, compound=LEFT, padx=20, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_cardetails = Button(LeftMenu, text="Car Details", command=self.car_details, image=self.icon_side, compound=LEFT, padx=20, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_carphotos = Button(LeftMenu, command=self.car_photos, text="Car Photos", image=self.icon_side, compound=LEFT, padx=20, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_attendence = Button(LeftMenu, command=self.take_attendance, text="Attendance", image=self.icon_side, compound=LEFT, padx=20, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        #===content===
        self.lbl_security = Label(self.root, text="Total Security \n Guards \n [ 0 ]", bg="green", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_security.place(x=300, y=120, height=150, width=300)

        self.lbl_cars = Label(self.root, text="Total Cars \n Parked Today \n [ 0 ]", bg="blue", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_cars.place(x=650, y=120, height=150, width=300)

        self.lbl_parking = Label(self.root, text="Parking \n Available \n [ 0 ]", bg="red", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_parking.place(x=1000, y=120, height=150, width=300)

        # ===footer===
        lbl_footer = Label(self.root, text="Mall OF India | Developed By PyDevelopers \n For any technical issue contact: 9157251380, 810464397", font=("times new roman", 15), fg="white", bg="#4d636d").pack(side=BOTTOM, fill=X)

        self.get_date_time()
        self.update_details()

    def security_details(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = sec_details(self.new_win)

    def update_details(self):
        conn = mysql_CRUD()
        try:
            sec_num = conn.get_num_employess()
            self.lbl_security.config(text=f"Total Security \n Guards \n [{sec_num}]")

            today = date.today()
            d = today.strftime("%Y/%m/%d")
            total_cars = conn.get_car_num(d)
            self.lbl_cars.config(text=f"Total Cars \n Parked Today \n [{total_cars}]")

            parking_num = conn.get_parking()
            parking_num = int(parking_num)
            park_avail = 100 - parking_num
            self.lbl_parking.config(text=f"Parking \n Available \n [ {park_avail} ]")
        except Exception as ex:
            messagebox.showerror('Error', f"Error due to: {str(ex)}", parent=self.root)

    def get_date_time(self):
        time_n = time.strftime("%I:%M:%S")
        today = date.today()
        d = today.strftime("%d-%m-%Y")
        self.clock_lbl.config(text=f"Welcome to Mall of India \t\t Date: {d} \t\t Time: {time_n}")
        self.clock_lbl.after(200, self.get_date_time)

    def car_details(self):
        self.new_car = Toplevel(self.root)
        self.new_obj_car = car_details(self.new_car)

    #=====To show the car photos===
    def car_photos(self):
        os.startfile("Car_photos")

    #====To take attendance=====
    def take_attendance(self):
        pass

    def logout_btn(self):
        self.root.destroy()
        os.system("python admin_login.py")


if __name__ == "__main__":
    root = Tk()
    obj = admin_side(root)
    root.mainloop()

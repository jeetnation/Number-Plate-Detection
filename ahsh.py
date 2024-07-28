import cv2
import easyocr
import string
import random
import time
import qrcode
from tkinter import *
from datetime import date
from database_connect import mysql_CRUD

def get_qrcode(recipt):
    data = recipt
    top = Tk()
    top.geometry("200x200")
    img = qrcode.make(data)
    img.save("ID_Card/" + data + ".png")
    icon_titl = PhotoImage(file="ID_Card/" + data + ".png")
    lbl_img = Label(top, image=icon_titl).place(x=0, y=0, width=200, height=200)
    top.after(10000, top.destroy)
    top.mainloop()


def get_rand_number():
    upper = string.ascii_uppercase
    num = string.digits
    all = upper + num
    length = 5
    temp = random.sample(all, length)
    password = "".join(temp)

    return password


def insert_db(num, state):
    conn = mysql_CRUD()
    try:
        rant_n = get_rand_number()
        rand_sr = get_rand_number()
        time_n = time.strftime("%I:%M:%S")
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        conn.insert_car(rand_sr, rant_n, num, state, d, time_n)
    except:
        print("error")
    get_qrcode(rant_n)


state_name = {
    'AN': 'Andaman and Nicobar Islands',
    'LD': 'Lakshadweep',
    'AP': 'Andhra Pradesh',
    'MH': 'Maharashtra',
    'AR': 'Arunachal Pradesh',
    'ML': 'Meghalaya',
    'AS': 'Assam',
    'MN': 'Manipur',
    'BR': 'Bihar',
    'MP': 'Madhya Pradesh',
    'CG': 'Chhattisgarh',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'DD': 'Daman and Diu',
    'OD': 'Odisha',
    'Dl': 'Dehli',
    'PB': 'Punjab',
    'GA': 'Goa',
    'RJ': 'Rajasthan',
    'GJ': 'Gujrat',
    'SK': 'Sikkim',
    'HR': 'Haryana',
    'TN': 'Tamil Nadu',
    'TR': 'Tripura',
    'JH': 'Jharkhand',
    'TS': 'Telangana',
    'JK': 'Jammu and Kashmir',
    'UK': 'Uttarakhand',
    'KA': 'Karnataka',
    'UP': 'Uttar Pradesh',
    'KL': 'Kerela',
    'WB': 'West Bengal',
    'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli',
    'HP': 'Himachal Pradesh',
    'PY': 'Puducherry'
}

frameWidth = 640    #Frame Width
franeHeight = 480   # Frame Height

plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500

cap =cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, franeHeight)
cap.set(10, 150)
count = 0

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "NumberPlate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            imgRoi = img[y:y+h, x:x+w]
            cv2.imshow("ROI", imgRoi)
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        reader = easyocr.Reader(['en'])
        result = reader.readtext(imgRoi)
        plate_num = result[0][-2]
        try:
            state_d = state_name[plate_num[0:2]]
        except:
            state_d = "NONE"

        cv2.imwrite(f"Num_plates/{plate_num}.jpg", imgRoi)
        insert_db(plate_num, state_d)
        break
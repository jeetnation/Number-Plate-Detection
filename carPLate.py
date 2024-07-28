#importing libraries
import cv2            #pip install opencv-python
import numpy as np    #pip install numpy
import easyocr        #pip install easyocr
import imutils        #pip install imutils
import string
import random
import time
from datetime import date
from database_connect import mysql_CRUD

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

state_name = {
    'AN':'Andaman and Nicobar Islands',
    'LD':'Lakshadweep',
    'AP':'Andhra Pradesh',
    'MH':'Maharashtra',
    'AR':'Arunachal Pradesh',
    'ML':'Meghalaya',
    'AS':'Assam',
    'MN':'Manipur',
    'BR':'Bihar',
    'MP':'Madhya Pradesh',
    'CG':'Chhattisgarh',
    'MZ':'Mizoram',
    'NL':'Nagaland',
    'DD':'Daman and Diu',
    'OD':'Odisha',
    'Dl':'Dehli',
    'PB':'Punjab',
    'GA':'Goa',
    'RJ':'Rajasthan',
    'GJ':'Gujrat',
    'SK':'Sikkim',
    'HR':'Haryana',
    'TN':'Tamil Nadu',
    'TR':'Tripura',
    'JH':'Jharkhand',
    'TS':'Telangana',
    'JK':'Jammu and Kashmir',
    'UK':'Uttarakhand',
    'KA':'Karnataka',
    'UP':'Uttar Pradesh',
    'KL':'Kerela',
    'WB':'West Bengal',
    'CH':'Chandigarh',
    'DN':'Dadra and Nagar Haveli',
    'HP':'Himachal Pradesh',
    'PY':'Puducherry'
}

img = cv2.imread('download6.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bifilter = cv2.bilateralFilter(gray, 11, 17, 17)   #Noise Reduction
edged = cv2.Canny(bifilter, 30, 200)               #Edge Detection

key_points = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(key_points)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

mask = np.zeros(gray.shape, np.uint8)
new_img = cv2.drawContours(mask, [location], 0, 255, -1)
new_img = cv2.bitwise_and(img, img, mask=mask)

(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_img = gray[x1:x2+1, y1:y2+1]

reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_img)
plate_num = result[0][-2]
try:
    state_d = state_name[plate_num[0:2]]
except:
    state_d = "NONE"

cv2.imwrite(f"Car_photos/{plate_num}.jpg", img)
cv2.imwrite(f"Num_plates/{plate_num}.jpg", cropped_img)
insert_db(plate_num, state_d)

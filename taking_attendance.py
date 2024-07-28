#Save in an exel file

import cv2
import numpy as np
from pyzbar.pyzbar import decode
from database_connect import mysql_CRUD

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    ret, frame = cap.read()

    for barcode in decode(frame):
        myData = barcode.data.decode('utf-8')
        print(myData)

        pts = np.array([barcode.polygon], np.int32)
        cv2.polylines(frame, [pts], True, (255, 0, 0), 5)
        pts2 = barcode.rect
        cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        conn = mysql_CRUD()
        details_attendance = conn.get_attend(myData)
        print(details_attendance)

    cv2.imshow('IN', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



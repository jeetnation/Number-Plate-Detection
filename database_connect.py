import mysql.connector as sql

class mysql_CRUD:
    def __init__(self):
        self.mydb = sql.connect(
            host="localhost",
            user="root",
            password="",
            database="sem5_proj"
        )
        self.mycursor = self.mydb.cursor()

    def insert_admin(self, admin_user, admin_name, admin_email, admin_phone, admin_DOB, admin_pass):
        sql_query = "INSERT INTO admin_table (admin_user, admin_name, admin_email, admin_phone, admin_DOB, admin_pass) VALUES (%s, %s, %s, %s, %s, md5(%s))"
        val = (admin_user, admin_name, admin_email, admin_phone, admin_DOB, admin_pass)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def insert_security(self, user_id, user_name, phone_no, email_id, user_DOB, user_pass):
        sql_query = "INSERT INTO user_table (user_id, user_name, phone_no, email_id, user_DOB, user_pass) VALUES (%s, %s, %s, %s, %s, md5(%s))"
        val = (user_id, user_name, phone_no, email_id, user_DOB, user_pass)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()


    def insert_car(self, sr_no, reciept_no, number_plate, state_name, enter_date, entry_time):
        sql_query = "INSERT INTO car_table (sr_no, reciept_no, number_plate, state_name, enter_date, entry_time) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (sr_no, reciept_no, number_plate, state_name, enter_date, entry_time)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()


    def insert_pay(self, pay_no, reciept_no, pay_mode, pay_amt, exit_date, exit_time):
        sql_query = "INSERT INTO payment_table (pay_no, reciept_no, pay_mode, pay_amt, exit_date, exit_time) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (pay_no, reciept_no, pay_mode, pay_amt, exit_date, exit_time)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def select_user(self):
        sql_query = "SELECT * FROM user_table"
        self.mycursor.execute(sql_query)
        rows = self.mycursor.fetchall()
        return rows

    def select_cars(self):
        sql_query = "SELECT * FROM car_table"
        self.mycursor.execute(sql_query)
        rows = self.mycursor.fetchall()
        return rows

    def check_forget(self, security_id, table_name):
        if table_name == "user_table":
            sql_query = "SELECT email_id FROM user_table WHERE user_id=%s"
        else:
            sql_query = "SELECT admin_email FROM admin_table WHERE admin_user=%s"
        val = (security_id,)
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchone()
        return myresult

    def update_pass(self, new_pass, id, table_name):
        if table_name == "user_table":
            sql_query = "UPDATE user_table SET user_pass = md5(%s) WHERE user_id = %s"
        else:
            sql_query = "UPDATE admin_table SET admin_pass = md5(%s) WHERE admin_user = %s"
        val = (new_pass, id)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def check_user(self, user_id, user_pass, table_name):
        if table_name == "user_table":
            sql_query = "SELECT * FROM user_table WHERE user_id=%s AND user_pass=md5(%s)"
        else:
            sql_query = "SELECT * FROM admin_table WHERE admin_user=%s AND admin_pass=md5(%s)"
        val = (user_id, user_pass)
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchone()
        return myresult

    def update_security(self, email, phone_no, id):
        sql_query = "UPDATE user_table SET phone_no = %s, email_id = %s WHERE user_id = %s"
        val = (phone_no, email, id)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def update_car(self, num_plate, state_name, sr_no):
        sql_query = "UPDATE user_table SET  number_plate = %s, state_name = %s WHERE sr_no = %s"
        val = (num_plate, state_name, sr_no)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def delete_security(self, id):
        sql_query = "DELETE FROM user_table WHERE user_id = %s"
        val = (id, )
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def delete_car(self, sr_no):
        sql_query = "DELETE FROM car_table WHERE sr_no = %s"
        val = (sr_no,)
        self.mycursor.execute(sql_query, val)
        self.mydb.commit()

    def get_security(self, value, val_name):
        if value == "Name":
            sql_query = "SELECT * FROM user_table WHERE user_name LIKE %s"
        else:
            sql_query = "SELECT * FROM user_table WHERE user_id LIKE %s"
        val = (val_name, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_car(self, value, val_name):
        if value == "Number Plate":
            sql_query = "SELECT * FROM car_table WHERE number_plate LIKE %s"
        else:
            sql_query = "SELECT * FROM car_table WHERE state_name LIKE %s"
        val = (val_name, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_num_employess(self):
        sql_query = "SELECT * FROM user_table"
        self.mycursor.execute(sql_query)
        myresult = self.mycursor.fetchall()
        return str(len(myresult))

    def get_car_num(self, date):
        sql_query = "SELECT * FROM car_table WHERE enter_date = %s"
        val = (date, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchall()
        return str(len(myresult))

    def get_parking(self):
        sql_query = "SELECT * FROM car_table LEFT JOIN payment_table ON car_table.reciept_no=payment_table.reciept_no"
        self.mycursor.execute(sql_query)
        myresult = self.mycursor.fetchall()
        return str(len(myresult))

    def get_attend(self, myData):
        sql_query = "SELECT * FROM user_table WHERE user_id = %s"
        val = (myData, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchall()
        return myresult

    def get_num_cars(self):
        sql_query = "SELECT * FROM car_table"
        self.mycursor.execute(sql_query)
        myresult = self.mycursor.fetchall()
        return str(len(myresult))

    def get_time(self, var_recipt):
        sql_query = "SELECT entry_time FROM car_table WHERE reciept_no = %s"
        val = (var_recipt, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchone()
        return myresult[0]

    def get_prent(self, var_recipt):
        sql_query = "SELECT reciept_no FROM car_table WHERE reciept_no = %s"
        val = (var_recipt, )
        self.mycursor.execute(sql_query, val)
        myresult = self.mycursor.fetchone()
        return myresult
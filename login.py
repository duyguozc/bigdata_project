import sqlite3

import re

import datetime


new_cryptographic_list = []
exist_cryptographic_list = []
cryptographic = []
email = []
exist_username = []
exist_psw = []
psw = []
role = []
ID = []


def create():
    for j in range(len(exist_username)):
        if username == exist_username[j]:
            print("This username already exist! Use another one or Log In")
    else:
        exist_username.append(username)
        crypto()


def crypto():
    usertype = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z", '0', "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^",
                "&", "*", "(", ")", "-", "_", "=", "+", "/", "|", ":", ";", "'", ",", "<", ".", ">", "?", "`", "~"]
    convert = ["T", "I", "M", "E", "O", "D", "A", "N", "S", "F", "R", "B", "C", "G", "H", "J", "K", "L", "P", "Q", "U",
               "V", "W", "X", "Y", "Z", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0", "!", "@", "#", "$", "%", "^",
               "&", "*", "(", ")", "-", "_", "=", "+", "/", "|", ":", ";", "'", ",", "<", ".", ">", "?", "`", "~"]

    for j in range(len(psw)):
        i = usertype.index(psw[j])
        new_cryptographic_list.append(convert[i])


def decrypto():
    usertype = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z", '0', "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^",
                "&", "*", "(", ")", "-", "_", "=", "+", "/", "|", ":", ";", "'", ",", "<", ".", ">", "?", "`", "~"]
    convert = ["T", "I", "M", "E", "O", "D", "A", "N", "S", "F", "R", "B", "C", "G", "H", "J", "K", "L", "P", "Q", "U",
               "V", "W", "X", "Y", "Z", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0", "!", "@", "#", "$", "%", "^",
               "&", "*", "(", ")", "-", "_", "=", "+", "/", "|", ":", ";", "'", ",", "<", ".", ">", "?", "`", "~"]

    for j in range(len(exist_cryptographic_list)):
        i = convert.index(exist_cryptographic_list[j])
        cryptographic.append(usertype[i])


a = 0

while a == 0:
    sql_conn = sqlite3.connect('agency_database.db')
    cursor = sql_conn.cursor()
    cursor.execute("SELECT UserID FROM Login;")
    result_id = cursor.fetchall()
    cursor.close()

    for r in result_id:
        for i in range(len(r)):
            ID.append(r[i])
    # print(ID)

    cursor = sql_conn.cursor()
    cursor.execute("SELECT UserName FROM Login;")
    result_username = cursor.fetchall()
    cursor.close()

    for r in result_username:
        for i in range(len(r)):
            exist_username.append(r[i])
    # print(exist_email)

    cursor = sql_conn.cursor()
    cursor.execute("SELECT Password FROM Login;")
    result_crypto = cursor.fetchall()
    cursor.close()

    for r in result_crypto:
        for i in range(len(r)):
            exist_psw.append(r[i])
    # print(exist_psw)

    cursor = sql_conn.cursor()
    cursor.execute("SELECT role FROM Login;")
    result_role = cursor.fetchall()
    cursor.close()

    for r in result_role:
        for i in range(len(r)):
            role.append(r[i])

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    print("_____Welcome_____")
    print("For Log In Press 1! ")
    print("For Register Press 2!")
    print("For Quit Press 3!")
    b = 0
    while b == 0:
        try:
            transaction = int(input("Selection:"))
            if transaction == 1:
                print("_____Log IN_____")
                username = str(input("Username:"))
                if username not in exist_username:
                    print("This username cannot found! Please try again or Register first!")
                else:
                    z = exist_username.index(username)
                    password = str(input("Password: ").strip().upper())
                    # print(password)
                    exist_cryptographic_list = list(exist_psw[z])
                    decrypto()
                    psw_exist = "".join([str(i) for i in cryptographic])
                    # print(exist_psw)
                    if password == psw_exist:
                        c = 0
                        while c == 0:
                            if role[z] == "Customer":
                                print("\nWelcome " + username)
                                print("Account[1]")
                                print("Search[2]")
                                print("Book[3]")
                                print("My Bookings[4]")
                                print("Log Out[5]")
                                d = 0
                                while d == 0:
                                    try:
                                        selection = int(input("Please enter the number of the menu "
                                                              "to select the action you want to do: "))
                                        if selection == 5:
                                            d = d + 1
                                            c = c + 1
                                            b = b + 1
                                            print("You successfully Log Out!\n")
                                    except ValueError:
                                        print("You should enter a number!")
                                        continue
                                    else:
                                        if selection < 1 or selection > 5:
                                            print("You entered invalid data. Please enter a valid value.")

                            if role[z] == "Agent":
                                print("\nWelcome " + username)
                                print("Search Customer[1]")
                                print("Reports[2]")
                                print("Log Out[3]")

                                d = 0
                                while d == 0:
                                    try:
                                        selection = int(input("Please enter the number of the menu "
                                                              "to select the action you want to do: "))
                                        if selection == 3:
                                            d = d + 1
                                            c = c + 1
                                            b = b + 1
                                            print("You successfully Log Out!\n")
                                    except ValueError:
                                        print("You should enter a number!")
                                        continue
                                    else:
                                        if selection < 1 or selection > 3:
                                            print("You entered invalid data. Please enter a valid value.")

                    else:
                        print("You made an incorrect entry. Please check your username and password.")

            elif transaction == 2:
                print("_____REGISTER_____")
                username = str(input("Username:"))
                if username not in exist_username:
                    password = str(input("Password: ").strip().upper())
                    psw = list(password)
                    crypto()
                    crypto_psw = "".join([str(i) for i in new_cryptographic_list])
                    name = str(input("Name: "))
                    while True:
                        dob = input("Date of Birth: ")
                        try:
                            dob = datetime.datetime.strptime(dob, "%d/%m/%Y")
                            break
                        except ValueError:
                            print("Error: must be format dd/mm/yyyy ")
                            continue
                    while True:
                        phone = input("Phone Number:")
                        if not phone.isdigit():
                            print("Invalid value entry! Please enter a valid phone number. ")
                            continue
                        elif len(phone) != 10:
                            print("Invalid value entry! Please enter a valid phone number. ")
                            continue
                        else:
                            break
                    while True:
                        email = str(input("Email:").lower())
                        if not re.search(regex, email):
                            print("Invalid Email! Please give valid email.")
                        else:
                            break
                    print("You have successfully registered! You can log in now!")
                    # print(crypto_psw)
                    cursor = sql_conn.cursor()
                    sql_insert_query = """INSERT INTO Login (UserName, Password, Role, Name, 
                    DOB, PhoneNumber, EmailId) values (?,?,?,?,?,?,?);"""
                    data_tuple = (username, crypto_psw, "Customer", name, dob, phone, email)
                    cursor.execute(sql_insert_query, data_tuple)
                    cursor.execute("COMMIT;")
                    cursor.close()
                    break
                else:
                    print("This username already exist. Please enter another username or Log In!")
            elif transaction == 3:
                a = a + 1
                sql_conn.close()

        except ValueError:
            print("You should enter a number!")
            continue
        else:
            if transaction < 1 or transaction > 3:
                print("You entered invalid data. Please enter a valid value.")
            else:
                b = b + 1

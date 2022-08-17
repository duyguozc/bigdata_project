import sqlite3

import re

import datetime

import account_details as account_file
import analysis_report

import search_part as search_part

import book

from classes import Tour

from classes import Booking

import search_by_agent as search_by_agent

import Add_Tour

import edit_tour

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


def get_all_tours():
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Tour'
    cursor.execute(sql)
    tours = cursor.fetchall()
    tour_objects = []
    for t in tours:
        tour = Tour(t)
        tour_objects.append(tour)
    connection.close()
    return tour_objects


def get_user_id_from_username(uname):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT UserID FROM Login WHERE username = ?'
    cursor.execute(sql, [uname])
    userid = cursor.fetchone()
    connection.close()
    return userid[0]


if __name__ == '__main__':
    a = 0

    while a == 0:
        new_cryptographic_list = []
        exist_cryptographic_list = []
        cryptographic = []
        email = []
        exist_username = []
        exist_psw = []
        psw = []
        role = []
        ID = []
        ag_un = []

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
                                    d = 0
                                    while d == 0:
                                        try:
                                            print("       Main Menu        ")
                                            print("############################")
                                            print("1. My Account")
                                            print("2. Search a Tour")
                                            print("3. Book a Tour")
                                            print("4. My Bookings")
                                            print("5. Quit")
                                            print("############################")
                                            selection = int(input("Please enter the number of the menu "
                                                                  "to select the action you want to do: "))

                                            if selection == 1:
                                                account_file.account(username)
                                            elif selection == 2:
                                                search_part.search()
                                            elif selection == 3:
                                                user_id = get_user_id_from_username(username)
                                                book.book_tour(user_id)
                                            elif selection == 4:
                                                user_id = get_user_id_from_username(username)
                                                book.booking_edit_delete_operations(user_id)
                                            elif selection == 5:
                                                d = d + 1
                                                c = c + 1
                                                b = b + 1
                                                sql_conn.close()
                                                print("You successfully Log Out!\n")
                                                break
                                        except ValueError:
                                            print("You should enter a number!")
                                            continue
                                        else:
                                            if selection < 1 or selection > 5:
                                                print("You entered invalid data. Please enter a valid value.")
                                if role[z] == "Agent":
                                    print("\nWelcome " + username)
                                    d = 0
                                    while d == 0:
                                        try:
                                            print("       Menu        ")
                                            print("############################")
                                            print("1. Search Customer")
                                            print("2. Log Out")
                                            print("############################")
                                            selection = int(input("Please enter the number of the menu "
                                                                  "to select the action you want to do: "))
                                            if selection == 1:
                                                search_by_agent.search_agent()
                                            elif selection == 2:
                                                d = d + 1
                                                c = c + 1
                                                b = b + 1
                                                print("You successfully Log Out!\n")
                                                break
                                        except ValueError:
                                            print("You should enter a number!")
                                            continue
                                        else:
                                            if selection < 1 or selection > 2:
                                                print("You entered invalid data. Please enter a valid value.")
                                if role[z] == "Admin":
                                    print("\nWelcome " + username)
                                    d = 0
                                    while d == 0:
                                        try:
                                            print("       Menu        ")
                                            print("############################")
                                            print("1. Manage Agents")
                                            print("2. Manage Tours")
                                            print("3. Reports")
                                            print("4. Log Out")
                                            print("############################")
                                            selection = int(input("Please enter the number of the menu "
                                                                  "to select the action you want to do: "))
                                            if selection == 1:
                                                e = 0
                                                while e == 0:
                                                    try:
                                                        print("\n############################")
                                                        print("1. Add Agent")
                                                        print("2. Delete Agent")
                                                        print("3. Main Menu")
                                                        sub_selection = int(input("Please enter the number of the "
                                                                                  "option to select the action you want"
                                                                                  " to do: "))
                                                        if sub_selection == 1:
                                                            sub_uname = str(input("Username:"))
                                                            if sub_uname not in exist_username:
                                                                password = str(input("Password: ").strip().upper())
                                                                psw = list(password)
                                                                crypto()
                                                                crypto_psw = "".join(
                                                                    [str(i) for i in new_cryptographic_list])
                                                                ag_dob='01/01/1900'
                                                                ag_dob=datetime.datetime.strptime(ag_dob, "%d/%m/%Y")
                                                                print("Agent added successfully!")
                                                                cursor = sql_conn.cursor()
                                                                sql_insert_query = """INSERT INTO Login (UserName, 
                                                                Password, Role, Name, DOB, PhoneNumber, EmailId) values 
                                                                (?,?,?,?,?,?,?);"""
                                                                data_tuple = (sub_uname, crypto_psw, "Agent", sub_uname,
                                                                              ag_dob, "9999", "agent@agent.com")
                                                                cursor.execute(sql_insert_query, data_tuple)
                                                                cursor.execute("COMMIT;")
                                                                cursor.close()
                                                                break
                                                            else:
                                                                print("This agent already exist!\n")
                                                                break
                                                        if sub_selection == 2:
                                                            agent = "Agent"
                                                            cursor = sql_conn.cursor()
                                                            cursor.execute("SELECT UserName FROM Login where Role = 'Agent'")
                                                            agent_usernames = cursor.fetchall()
                                                            cursor.close()

                                                            for r in agent_usernames:
                                                                for i in range(len(r)):
                                                                    ag_un.append(r[i])
                                                            print("Agents:")
                                                            print(ag_un)
                                                            del_agent = str(input("Please enter the username of the "
                                                                                  "agent you wish to delete: "))
                                                            if del_agent not in ag_un:
                                                                print("Agent cannot found!")
                                                            else:
                                                                cursor = sql_conn.cursor()
                                                                cursor.execute("DELETE from Login where UserName = ?",
                                                                               [del_agent])
                                                                cursor.execute("COMMIT;")
                                                                print("Record deleted successfully ")
                                                                cursor.close()
                                                        elif sub_selection == 3:
                                                            e = e + 1
                                                    except ValueError:
                                                        print("You should enter a number!")
                                                        continue
                                                    else:
                                                        if sub_selection < 1 or sub_selection > 3:
                                                            print(
                                                                "You entered invalid data. Please enter a valid value.")
                                            elif selection == 2:
                                                e = 0
                                                while e == 0:
                                                    try:
                                                        print("\n############################")
                                                        print("1. Add Tour")
                                                        print("2. Update/Delete Tour")
                                                        print("3. Main Menu")
                                                        sub = int(input("Please enter the number of the menu "
                                                                              "to select the action you want to do: "))
                                                        if sub == 1:
                                                            Add_Tour.addtour()
                                                        elif sub == 2:
                                                            all_objects = book.get_all_tours()
                                                            for tour_object in all_objects:
                                                                book.print_tour(tour_object)
                                                            tour_label=input("Please enter the tour label you want to update/delete: ")
                                                            tour = book.get_tour_by_tour_label(tour_label)
                                                            if tour != None:
                                                                edit_tour.update_delete_tour(tour[0])
                                                            else:
                                                                print( "Tour ID doesn't exist.")
                                                        elif sub == 3:
                                                            e = e + 1
                                                    except ValueError:
                                                        print("You should enter a number!")
                                                        continue
                                                    else:
                                                        if sub < 1 or sub > 3:
                                                            print(
                                                                "You entered invalid data. Please enter a valid value.")

                                            elif selection == 3:
                                                analysis_report.show_report_menu()
                                            elif selection == 4:
                                                d = d + 1
                                                c = c + 1
                                                b = b + 1
                                                print("You successfully Log Out!\n")
                                                break
                                        except ValueError:
                                            print("You should enter a number!")
                                            continue
                                        else:
                                            if selection < 1 or selection > 2:
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
                            dob = input("Date of Birth(dd/mm/yyy): ")
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

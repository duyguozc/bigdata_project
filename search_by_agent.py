import sqlite3
import search_part
import account_details as account_file

import book

from classes import Tour

from classes import Booking

def search_agent():
    select = 0
    while select != 3:
        try:
            print("\n1. Search by Customer E-mail  \n2. Search by Customer Name \n3. Back to main Menu")
            select = int(input("Select one of the option: "))

            if select == 1:
                search_c_email()

            elif select == 2:
                search_c_name()

            elif select == 3:
                break
            else:
                print("Please Enter a valid option")
        except ValueError:
            print("You should enter a number")
            continue


def search_c_email():
    c_email = input("Please Enter the Customer E-mail: ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Login where EmailId like ?", ['%'+c_email+'%'])
    results = cursor.fetchall()
    if len(results) == 0:
        print("Email not found.")
    else:
        data = results
        print(data)
        username = input("Please enter username of the customer")
        nameFound = False
        for row in data:
            if username == row[1].lower():
                nameFound = True

        if nameFound:
            customer_menu(username)
            return;
        else:
            print("You entered wrong username!")

def search_c_name():
    c_name= input("Please Enter the Customer Name: ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Login where Name like ?", ['%'+c_name+'%'])
    results = cursor.fetchall()
    if len(results) == 0:
        print("Name not found.")
    else:
        data = results
        print(data)
        username = input("Please enter username of the customer")
        nameFound = False
        for row in data:
            if username == row[1].lower():
                nameFound = True

        if nameFound:
            customer_menu(username)
            return;
        else:
            print("You entered wrong username!")


def customer_menu(username):
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
            print("5. Return to Agent Menu")
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
                return
        except ValueError:
            print("You should enter a number!")
            continue
        else:
            if selection < 1 or selection > 5:
                print("You entered invalid data. Please enter a valid value.")

def get_user_id_from_username(uname):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT UserID FROM Login WHERE username = ?'
    cursor.execute(sql, [uname])
    userid = cursor.fetchone()
    connection.close()
    return userid[0]

def menu():

    search_part.search()

if __name__ == "__main__":
        search_agent()

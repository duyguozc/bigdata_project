import sqlite3
import search_part

def search_agent():
    select = 0
    while select != 3:
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


def search_c_email():
    c_email = input("Please Enter the Customer E-mail: ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Login where EmailId like ?", ['%'+c_email+'%'])
    results = cursor.fetchall()
    data = results
    print(data)

    menu()


def search_c_name():
    c_name= input("Please Enter the Customer Name: ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Login where Name like ?", ['%'+c_name+'%'])
    results = cursor.fetchall()
    data = results
    print(data)


    menu()


def menu():

    search_part.search()

if __name__ == "__main__":
        search_agent()

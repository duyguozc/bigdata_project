import sqlite3


def search():
    select = 0
    while select != 3:
        print("\n1. Search by Month  \n2. Search by Destination\n3. Back to main Menu")
        select = int(input("Select one of the option: "))

        if select == 1:
            search_month()

        elif select == 2:
            search_destination()

        elif select == 3:
            break

        else:
            print("Please Enter a valid option")


def search_destination():
    destination = input("Please Enter the Destination: ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Tour where destination like ?", ['%'+destination+'%'])
    results = cursor.fetchall()
    if len(results) == 0:
        print("We have no tour to that destination.")
    else:
        data = results
        print(data)



def search_month():
    input_month= input("Please Enter the month number: ")
    if len(input_month) == 1:
        month= '0' + input_month
    else:
        month= input_month
    print (month)

    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Tour where SUBSTR(start_date, 4,2) = ?", [month])
    results = cursor.fetchall()
    if len(results) == 0:
        print("We have no tour in this month.")
    else:
        data = results
        print(data)


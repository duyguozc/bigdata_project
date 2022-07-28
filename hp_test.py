import sqlite3



def search():
    print("ENTER\n1. Search by Month  \n2. Search by Destination\n3. Back to main Menu")
    select = int(input("Select one of the option: "))

    if select == 1:
        search_month()

    elif select == 2:
        search_destination()

    elif select == 3:
        search()

    else:
        print("Please Enter a valid option")
        search()

def search_destination():
    destination = input("Please Enter the Destination")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Tour where destination = ?", [destination])
    results = cursor.fetchall()
    data = results
    print(data)
    D = input("Enter any key to go back")
    if D is not None:
        search()


def search_month():
    input_month= input("Please Enter the month number")
    if len(input_month) == 1:
        month= '0' + input_month
    else:
        month= input_month
    print (month)

    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Tour where SUBSTR(start_date, 4,2) = ?", [month])
    results = cursor.fetchall()
    data = results
    print(data)

if __name__ == "__main__":
    search()


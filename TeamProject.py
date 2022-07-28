import sqlite3

def account():
    print('(1) View Account (2) Edit Account (3) Main Menu')
    option = int(input("Option : "))
    if option == 1:
        viewaccount()
    elif option == 2:
        editaccount()
    elif option == 3:
        viewaccount()

    else:
         print("Choose valid option")
         account()


def viewaccount():
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select * from Login")
    results = cursor.fetchall()
    data = results
    print(data)
    anykey = input("Enter any number to go back main menu : ")

    if anykey is not None:
        account()

def editaccount():
    print(' Enter (1) Edit Name  (2) Edit DOB (3) Edit Phone Number (4) Edit EmailId')
    editoption = int(input("Option : "))

    if editoption == 1:
        editname()
    elif editoption == 2:
        editdob()
    elif editoption == 3:
        editpn()
    elif editoption == 4:
        editeid()
    else:
        print("Please enter valid option")
        editaccount()

def editname():
    userid = int(input("Please enter user id "))
    name = input("Please enter new Name ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("update Login set name = ? where userid = ?", (name,userid))
    print("Name updated successfully!")
    cursor.commit()
    cursor.close()
    cursor1.execute("Select * from Login where userid = ?", userid)
    result = cursor.fetchall()
    data = result
    print(data)

    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editdob():
    userid = int(input("Please enter user id "))
    dob = input("Please enter new DOB (dd/mm/yyyy) ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("update Login set dob = ? where userid = ?", (dob,userid))
    print("DOB updated successfully!")
    cursor.commit()
    cursor.close()
    cursor1.execute("Select * from Login where userid = ?", userid)
    result = cursor.fetchall()
    data = result
    print(data)

    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editpn():
    userid = int(input("Please enter user id "))
    phonenumber = input("Please enter new phone number (no space or special character eg.1234567890) ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("update Login set phonenumber = ? where userid = ?", (phonenumber, userid))
    print("Phone Number updated successfully!")
    cursor.commit()
    cursor.close()
    cursor1.execute("Select * from Login where userid = ?", userid)
    result = cursor.fetchall()
    data = result
    print(data)

    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editeid():
    userid = int(input("Please enter user id "))
    emailid = input("Please enter new emailid  ")
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor.execute("update Login set emailid = ? where userid = ?", (emailid, userid))
    print("Email Id updated successfully!")
    cursor.commit()
    cursor.close()
    cursor1.execute("Select * from Login where userid = ?", userid)
    result = cursor.fetchall()
    data = result
    print(data)

    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

if __name__ == "__main__":
    account()
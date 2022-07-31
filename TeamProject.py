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
    elif option == 4:
        quit()
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

    try:
        name = input("Please enter new Name ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set Name = ? where UserID = ?", (name, userid))
        connection.commit()
        print("Name updated successfully!")
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()
    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editdob():
    userid = int(input("Please enter user id "))

    try:
        dob = input("Please enter new dob(dd/mm/yyyy) ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set DOB = ? where UserID = ?", (dob, userid))
        connection.commit()
        print("DOB updated successfully!")
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()
    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editpn():
    userid = int(input("Please enter user id "))

    try:
        phonenumber = input("Please enter new phone number(no space, no special character) ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set PhoneNumber = ? where UserID = ?", (phonenumber, userid))
        connection.commit()
        print("Phone Number updated successfully!")
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()
    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

def editeid():
    userid = int(input("Please enter user id "))

    try:
        emailid = input("Please enter new Email Id ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set EmailId = ? where UserID = ?", (emailid, userid))
        connection.commit()
        print("Phone Number updated successfully!")
        cursor.execute("Select * from Login where UserID = ?", [userid])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()
    anykey = input("Enter any number to go back main menu : ")
    if anykey is not None:
        account()

if __name__ == "__main__":
    account()
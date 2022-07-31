import sqlite3
import datetime

def account(user_name):
    option = 0
    while option != 3:
        print('(1) View Account (2) Edit Account (3) Main Menu')
        option = int(input("Option : "))
        if option == 1:
            viewaccount(user_name)
        elif option == 2:
            editaccount(user_name)
        elif option == 3:
            break
        else:
            print("Choose valid option")



def viewaccount(user_name):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", (user_name,))
    results = cursor.fetchall()
    data = results
    print(data)


def editaccount(user_name):
    print(' Enter (1) Edit Name  (2) Edit DOB (3) Edit Phone Number (4) Edit EmailId')
    editoption = int(input("Option : "))

    if editoption == 1:
        editname(user_name)
    elif editoption == 2:
        editdob(user_name)
    elif editoption == 3:
        editpn(user_name)
    elif editoption == 4:
        editeid(user_name)
    else:
        print("Please enter valid option")

def editname(user_name):

    try:
        name = input("Please enter new Name ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set Name = ? where username = ?", (name, user_name))
        connection.commit()
        print("Name updated successfully!")
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()

def editdob(user_name):

    try:
        while True:
            dob = input("Please enter new dob(dd/mm/yyyy) ")
            try:
                dob = datetime.datetime.strptime(dob, "%d/%m/%Y")
                break
            except ValueError:
                print("Error: must be format dd/mm/yyyy ")
                continue
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set DOB = ? where username = ?", (dob, user_name))
        connection.commit()
        print("DOB updated successfully!")
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()

def editpn(user_name):


    try:
        phonenumber = input("Please enter new phone number(no space, no special character) ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set PhoneNumber = ? where username = ?", (phonenumber, user_name))
        connection.commit()
        print("Phone Number updated successfully!")
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user id", error)
    finally:
        if connection:
            connection.close()

def editeid(user_name):

    try:
        emailid = input("Please enter new Email Id ")
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.execute("update Login set EmailId = ? where username = ?", (emailid, user_name))
        connection.commit()
        print("Phone Number updated successfully!")
        cursor.execute("Select Name, DOB, PhoneNumber, EmailId from Login where username = ?", [user_name])
        result = cursor.fetchall()
        data = result
        print(data)
        cursor.close()
    except sqlite3.error as error:
        print("Please enter valid user name", error)
    finally:
        if connection:
            connection.close()
    #anykey = input("Enter any number to go back main menu : ")
    #if anykey is not None:
    #    account()

#if __name__ == "__main__":
    #account()
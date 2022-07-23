import sqlite3
import re
from datetime import datetime
import traceback
import sys
from classes import Tour

date_regex = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'


def get_tour_by_tour_id(tourlbl):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Tour WHERE tour_label = ?'
    cursor.execute(sql, (tourlbl,))
    tour = cursor.fetchone()
    connection.close()
    return tour

def complete_booking(user_id, book_tuple, pay_list):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    try:
        insert_sql_booking = 'INSERT INTO Booking(tour_id, cust_id, number_of_people, total_price) VALUES(?,?,?,?)'
        cursor.execute(insert_sql_booking, book_tuple)
        insert_sql_payment = 'INSERT INTO Payment(user_id, booking_id, name, card_number, cvv, expiry_date, amount, ' \
                             'transaction_date, transaction_type) VALUES(?,?,?,?,?,?,?,?,?)'
        booking_id = cursor.lastrowid
        pay_list.insert(1, booking_id)
        cursor.execute(insert_sql_payment, tuple(pay_list))
        update_tour_info(cursor, book_tuple[0], book_tuple[2])
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    connection.commit()
    connection.close()

def update_tour_info(cursor, tour_id, people_number):
    update_sql = 'UPDATE Tour SET available_seats = available_seats - ' +str(people_number)+ ' WHERE id = ?'
    cursor.execute(update_sql, (tour_id,))


def print_tour(my_tour):
    print("Tour Id: ", my_tour.id, end = ' ')
    print("Destination: ", my_tour.dest)
    print("Description: ",my_tour.desc)
    print("Start date: ",my_tour.st_date, "  End Date: ", my_tour.end_date)
    print("Total capacity: ",my_tour.total_seats,"  Available seats: ", my_tour.avail_seats)
    print("Price per person: $%.2f: " % my_tour.fare)


def book_tour(tour_label_list, user_id):
    print("************************")
    print("Book a Tour")
    print("1. Book with Tour Id")
    print("2. Book without Tour Id")
    print("************************")
    option = int(input("Please select one option: "))
    while option < 1 or option > 2:
        print("You should enter 1 or 2.")
        option = int(input("Please select one option: "))
        error = True
        while error:
            try:
                option = int(input("Please select one option: "))
            except ValueError:
                print("You should enter a number!")
                continue
    if option == 1:
        tour_label = input("Enter Tour ID: ")
        while not tour_label in tour_label_list:
            tour_label = input("Tour ID doen't exist. Please enter an existing id: ")
        record = get_tour_by_tour_id(tour_label)
        tour = Tour(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8])

        fare = tour.fare
        tour_id = tour.id
        print("You chose the tour. Tour Information")
        print_tour(tour)
        no_of_people=int(input("Please enter number of people to attend: "))
        while no_of_people > tour.avail_seats:
            no_of_people = int(input("It is Enter smaller number: "))
        total_price = fare * no_of_people
        print("Your total total_price is $%.2f"  % (total_price))
        proceed = input("Do you want to proceed payment?(y/n)")
        if proceed.lower() == "y":
            print("---------------")
            fullname = input("Enter your fullname: ")
            card_no = input("Enter your card number: ")
            cvv = int(input("Enter CVV code: "))
            expire_date = input("Enter expire date(dd/mm/yyyy): ")
            is_match = re.fullmatch(date_regex, expire_date)
            while not is_match:
                print("You entered the date in wrong format!")
                expire_date = input("Enter expire date(dd/mm/yyyy): ")
                is_match = re.fullmatch(date_regex, expire_date)
            print("---------------")
            exp_date = datetime.strptime(expire_date, "%d/%m/%Y")
            transaction_date = datetime.now()
            transaction_date_str = transaction_date.strftime("%d/%m/%Y %H:%M:%S")
            transaction_type = "sale"

            booking_tuple = (tour_id, user_id, no_of_people, total_price)
            payment_list = [user_id, tour_id, card_no, cvv, transaction_date, total_price, transaction_date_str, transaction_type]
            complete_booking(user_id, booking_tuple, payment_list)
            print("You sucessfully booked from the tour.")

















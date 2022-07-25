import sqlite3
import re
from datetime import datetime
import traceback
import sys
from classes import Tour
from classes import Booking
import numpy as np

date_regex = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
insert_sql_payment = 'INSERT INTO Payment(user_id, booking_id, name, card_number, cvv, expiry_date, amount, ' \
                     'transaction_date, transaction_type) VALUES(?,?,?,?,?,?,?,?,?)'


def get_tour_by_tour_label(tourlbl):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Tour WHERE tour_label = ?'
    cursor.execute(sql, (tourlbl,))
    tour = cursor.fetchone()
    connection.close()
    return tour

def get_tour_by_tour_id(tourid):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Tour WHERE id = ?'
    cursor.execute(sql, (tourid,))
    tour = cursor.fetchone()
    connection.close()
    return tour

def get_booking_list_of_user(user_id):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Booking WHERE user_id = ?'
    cursor.execute(sql, (user_id,))
    booking_list = cursor.fetchall()
    connection.close()
    booking_objects = []
    for book in booking_list:
        booking_objects.append(Booking(book))
    return booking_objects


def add_booking(user_id, book_tuple, pay_list):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    try:
        insert_sql_booking = 'INSERT INTO Booking(tour_id, user_id, number_of_people, total_price) VALUES(?,?,?,?)'
        cursor.execute(insert_sql_booking, book_tuple)
        booking_id = cursor.lastrowid
        pay_list.insert(1, booking_id)
        cursor.execute(insert_sql_payment, tuple(pay_list))
        # book_tuple[0] = 3,  book_tuple[3] = number_of_people
        update_tour_info(cursor, book_tuple[0], book_tuple[3])
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
    print("3. Return to main menu")
    print("************************")
    option = int(input("Please select one option: "))
    while option < 1 or option > 3:
        print("You should enter 1,2 or 3.")
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
        record = get_tour_by_tour_label(tour_label)
        tour = Tour(record)

        fare = tour.fare
        tour_id = tour.id
        print("You chose the tour. Tour Information")
        print_tour(tour)
        no_of_people=int(input("Please enter number of people to attend: "))
        while no_of_people > tour.avail_seats:
            no_of_people = int(input("It exceeds available seats! Enter smaller number: "))
        total_price = fare * no_of_people
        print("Your total total_price is $%.2f"  % (total_price))
        proceed = input("Do you want to proceed payment?(y/n)")
        if proceed.lower() == "y":
            card_no, cvv, expire_date = prompt_card_info()
            exp_date = datetime.strptime(expire_date, "%d/%m/%Y").date()
            transaction_date = datetime.now()
            transaction_date_str = transaction_date.strftime("%d/%m/%Y %H:%M:%S")
            transaction_type = "sale"

            booking_tuple = (tour_id, user_id, no_of_people, total_price)
            payment_list = [user_id, tour_id, card_no, cvv, transaction_date, total_price, transaction_date_str, transaction_type]
            add_booking(user_id, booking_tuple, payment_list)
            print("You sucessfully booked from the tour.")
    elif option==2:
        print(tour_label_list)


def prompt_card_info():
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
    return card_no, cvv, expire_date


def edit_booking(booking_id):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql = 'SELECT * FROM Booking WHERE id = ?'
    cursor.execute(sql, (booking_id,))
    booking_tuple = cursor.fetchone()
    book_obj = Booking(booking_tuple)
    new_count = int(input("Please enter number of people to attend: "))
    unit_price = book_obj.total_price/book_obj.number_of_people
    new_book_cost = unit_price * new_count

    if book_obj.number_of_people < new_count:
        diff_count = new_count - book_obj.number_of_people
        price_added = diff_count * unit_price
        print("Payment will be taken from your saved credit card. Difference is is $%.2f" % price_added)
        update_tour_info(cursor, book_obj.tour_id, diff_count)
        log_payment(book_obj, cursor, price_added, "sale")
    elif book_obj.number_of_people > new_count:
        diff_count = book_obj.number_of_people - new_count
        price_refund = diff_count * unit_price
        print("You will be refunded $%.2f" % price_refund)
        tour_sql = 'UPDATE Tour SET available_seats = available_seats + ' +str(diff_count)+ ' WHERE id = ?'
        cursor.execute(tour_sql, (book_obj.tour_id,))
        log_payment(book_obj, cursor, price_refund, "partial refund")

    print("Your booking is updated. You have {:d} participants now".format(new_count))
    book_sql = 'UPDATE Booking SET number_of_people = ' + str(new_count) + \
                                    ' , total_price = '+ str(new_book_cost) + \
                                    ' WHERE id = ?'
    cursor.execute(book_sql, (booking_id,))
    connection.commit()
    connection.close()


def log_payment(book_obj, cursor, new_cost, transact_type):
    payment_sql = 'SELECT * FROM Payment WHERE booking_id = ?'
    cursor.execute(payment_sql, (book_obj.id,))
    payment = cursor.fetchone()
    payment_array = np.asarray(payment)
    payment_array[7] = new_cost
    payment_array[9] = transact_type
    tran_date = datetime.now()
    tran_date_str = tran_date.strftime("%d/%m/%Y %H:%M:%S")
    payment_array[8] = tran_date_str
    payment_tuple_without_id = tuple(payment_array[1:10]) #payment_array[1:10] #index 1 included, 10 excluded
    cursor.execute(insert_sql_payment, payment_tuple_without_id)

def delete_booking(booking_id):
    pass
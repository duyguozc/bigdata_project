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

def get_booking_list_of_user(user_id):
    booking_list = []
    try:
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        sql = 'SELECT * FROM Booking WHERE user_id = ?'
        cursor.execute(sql, [user_id])
        booking_list = cursor.fetchall()
        booking_objects = []
        for book in booking_list:
            booking_objects.append(Booking(book))
        return booking_objects
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        connection.close()
    return []


def add_booking(user_id, book_tuple, pay_list):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    try:
        insert_sql_booking = 'INSERT INTO Booking(tour_id, user_id, number_of_people, total_price) VALUES(?,?,?,?)'
        cursor.execute(insert_sql_booking, book_tuple)
        booking_id = cursor.lastrowid
        pay_list.insert(1, booking_id)
        cursor.execute(insert_sql_payment, tuple(pay_list))
        # book_tuple[0] = 3,  book_tuple[2] = number_of_people
        reduce_tour_capacity(cursor, book_tuple[0], book_tuple[2])
        print("You successfully booked the tour.")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    connection.commit()
    connection.close()

def reduce_tour_capacity(cursor, tour_id, people_number):
    update_sql = 'UPDATE Tour SET available_seats = available_seats - ' +str(people_number)+ ' WHERE id = ?'
    cursor.execute(update_sql, (tour_id,))

def increase_tour_capacity(cursor, tour_id, diff_count):
    tour_sql = 'UPDATE Tour SET available_seats = available_seats + ' + str(diff_count) + ' WHERE id = ?'
    cursor.execute(tour_sql, (tour_id,))

def print_tour(my_tour):
    print("Tour Id: ", my_tour.label, end = ' ')
    print("Destination: ", my_tour.dest)
    print("Description: ",my_tour.desc)
    print("Start date: ",my_tour.st_date, "  End Date: ", my_tour.end_date)
    print("Total capacity: ",my_tour.total_seats,"  Available seats: ", my_tour.avail_seats)
    print("Price per person: $%.2f " % my_tour.fare)
    print()


def book_tour(user_id):
    tour_label_list = []
    all_tours = get_all_tours()
    for row in all_tours:
        tour_label_list.append(row.label)

    option = 0
    while option != 3:
        print("************************")
        print("Book a Tour")
        print("1. Book with Tour Id")
        print("2. Book without Tour Id")
        print("3. Return to main menu")
        print("************************")
        error = True
        option = 0
        while error:
            try:
                option = input("Please select one option: ")
                option = int(option)
            except ValueError:
                print("You should enter a number!")
                continue
            else:
                if option < 1 or option > 3:
                    print("You should enter a number between 1 and 3!")
                else:
                    error = False
        if option == 1:
            #Book with Tour Id
            perform_booking(tour_label_list, user_id)
        elif option == 2:
            #Book without Tour Id
            all_objects = get_all_tours()
            for tour_object in all_objects:
                print_tour(tour_object)
            perform_booking(tour_label_list, user_id)
        elif option == 3:
            break


def perform_booking(tour_label_list, user_id):
    tour_label = input("Enter Tour ID: ")
    while not tour_label.upper() in tour_label_list:
        tour_label = input("Tour ID doesn't exist. Please enter an existing id: ")
    record = get_tour_by_tour_label(tour_label.upper())
    tour = Tour(record)
    fare = tour.fare
    tour_id = tour.id
    print("You chose the tour. Tour Information")
    print_tour(tour)
    no_of_people = int(input("Please enter number of people to attend: "))
    while no_of_people > tour.avail_seats:
        no_of_people = int(input("It exceeds available seats! Enter smaller number: "))
    total_price = fare * no_of_people
    print("Your total total_price is $%.2f" % (total_price))
    proceed = input("Do you want to proceed payment?(y/n)")
    if proceed.lower() == "y":
        fullname, card_no, cvv, expire_date = prompt_card_info()
        exp_date = datetime.strptime(expire_date, "%d/%m/%Y").date()
        exp_date_str = exp_date.strftime("%d/%m/%Y")
        transaction_date = datetime.now()
        transaction_date_str = transaction_date.strftime("%d/%m/%Y %H:%M:%S")
        transaction_type = "sale"

        booking_tuple = (tour_id, user_id, no_of_people, total_price)
        payment_list = [user_id, fullname, card_no, cvv, exp_date_str, total_price, transaction_date_str,
                        transaction_type]
        add_booking(user_id, booking_tuple, payment_list)

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
        diff_people_count = new_count - book_obj.number_of_people
        price_added = diff_people_count * unit_price
        print("Payment will be taken from your saved credit card. Difference is is $%.2f" % price_added)
        reduce_tour_capacity(cursor, book_obj.tour_id, diff_people_count)
        log_payment(book_obj, cursor, price_added, "sale")
    elif book_obj.number_of_people > new_count:
        diff_people_count = book_obj.number_of_people - new_count
        price_refund = diff_people_count * unit_price
        print("You will be refunded $%.2f" % price_refund)
        increase_tour_capacity(cursor, book_obj.tour_id, diff_people_count)
        log_payment(book_obj, cursor, price_refund, "partial refund")

    print("Your booking is updated. You have {:d} participants now".format(new_count))
    book_sql = 'UPDATE Booking SET number_of_people = ' + str(new_count) + \
                                    ' , total_price = '+ str(new_book_cost) + \
                                    ' WHERE id = ?'
    cursor.execute(book_sql, (booking_id,))
    connection.commit()
    connection.close()


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
    return fullname, card_no, cvv, expire_date


def log_payment(book_obj, cursor, new_cost, transact_type):
    payment_sql = 'SELECT * FROM Payment WHERE booking_id = ?'
    cursor.execute(payment_sql, (book_obj.id,))
    payment = cursor.fetchone()
    if payment != None:
        payment_array = np.asarray(payment)
        payment_array[7] = new_cost
        payment_array[9] = transact_type
        tran_date = datetime.now()
        tran_date_str = tran_date.strftime("%d/%m/%Y %H:%M:%S")
        payment_array[8] = tran_date_str
        payment_tuple_without_id = tuple(payment_array[1:10]) #payment_array[1:10] #index 1 included, 10 excluded
        cursor.execute(insert_sql_payment, payment_tuple_without_id)
    else:
        print("No payment information found for this booking.")

def delete_booking(selected_book):
   sql = 'DELETE from Booking where id = ?'
   connection = sqlite3.connect('agency_database.db')
   cursor = connection.cursor()
   increase_tour_capacity(cursor, selected_book.tour_id, selected_book.number_of_people)
   print("You will be refunded $%.2f" % selected_book.total_price)
   log_payment(selected_book, cursor, selected_book.total_price, "refund")
   cursor.execute(sql, (selected_book.id,))
   connection.commit()
   connection.close()

def booking_edit_delete_operations(user_id):
    all_bookings = get_booking_list_of_user(user_id)
    if len(all_bookings) > 0:
        index = 1;
        for book_item in all_bookings:
            tour = get_tour_by_tour_id(book_item.tour_id)
            print("      (", index, ")   ")
            print("     BOOK INFO      ")
            print("Number of people to attend: ", book_item.number_of_people)
            print("Total price: $%.2f" % book_item.total_price)
            print("     TOUR INFO    ")
            print_tour(Tour(tour))
            print()
            index = index + 1

        error = True
        while error:
            try:
                option = int(input("Select a booking number to edit or delete: "))
                if option <= len(all_bookings):
                    selected_book = all_bookings[option - 1]
                    edit_or_del = input("Do you want to edit or delete ? (e/d)")
                    if edit_or_del.lower() == 'e':
                        edit_booking(selected_book.id)
                    elif edit_or_del.lower() == 'd':
                        delete = input("Are you sure? (y/n)")
                        if delete.lower() == 'y':
                            delete_booking(selected_book)
                            print("Your booking is deleted.")
                        error = False
                    else:
                        print("You should enter a valid option.")

                else:
                    print('Invalid number. Please choose from booking list!')
            except ValueError:
                print("You should enter a number!")
                continue
    else:
        print("You have no bookings yet.")
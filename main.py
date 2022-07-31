import book
import sqlite3
from classes import Tour
from classes import Booking

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

# Press the green button in the gutter to run the script.
def start():
    print("test")
    user_id = 2

    print("       Customer Menu        ")
    print("############################")
    print("1. My Account")
    print("2. Search a Tour")
    print("3. Book a Tour")
    print("4. My Bookings")
    print("5. Quit")
    print("############################")
    error = True
    menu = 0
    while error:
        try:
            menu = input("Select a number from the menu: ")
            menu = int(menu)
        except ValueError:
            print("You should enter a number!")
            continue
        else:
            if menu < 1 or menu > 5:
                print("You should enter a number between 1 and 5!")
            else:
                error = False
    if menu == 3:
        book.book_tour(user_id)
    elif menu == 4:
        all_bookings = book.get_booking_list_of_user(user_id)
        index = 1;
        for book_item in all_bookings:
            tour = book.get_tour_by_tour_id(book_item.tour_id)
            print("     (",index,")   ")
            print("   TOUR INFO    ")
            book.print_tour(Tour(tour))
            print("     BOOK INFO      ")
            print("Number of people to attend: ", book_item.number_of_people)
            print("Total price: ", book_item.total_price)
            print()
            index = index + 1
        option = int(input("Select a booking number to edit or delete: "))

        selected_book = all_bookings[option - 1]
        edit_or_del = input("Do you want to edit or delete ? (e/d)")
        if edit_or_del.lower() == 'e':
            book.edit_booking(selected_book.id)
        elif edit_or_del == 'd':
            delete = input("Are you sure? (y/n)")
            if delete.lower() == 'y':
                book.delete_booking(selected_book.id)
                print("Your booking is deleted.")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

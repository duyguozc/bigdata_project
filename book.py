# Author: Duygu Özçelik Şentürk
# Student Id : 8815048
import sqlite3


def get_tour_by_tour_id(tourid):
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()


def book_tour(tour_id_list):
    print("************************")
    print("Book a Tour")
    print("1. Book with Tour Id")
    print("2. Book without Tour Id")
    print("************************")
    option = input("Please select one option: ")
    while option < 1 or option > 2:
        print("You should enter 1 or 2.")
        option = input("Please select one option: ")
        error = True
        while error:
            try:
                option = input("Please select one option: ")
                option = int(option)
            except ValueError:
                print("You should enter a number!")
                continue
    if option == 1:
        tour_id = input("Enter Tour ID: ")
        if tour_id in tour_id_list:
            get_tour_by_tour_id(tour_id)






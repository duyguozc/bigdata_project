import sqlite3
import datetime

def addtour():
    print(' Please enter tour details below\n')
    tour_label = input(' Tour Label : ')
    while True:
        start_date = input(' Tour Start Date : ')
        try:
            start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Error: must be format dd/mm/yyyy ")
            continue
    while True:
        end_date = input(' Tour End Date : ')
        try:
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")
            break
        except ValueError:
            print("Error: must be format dd/mm/yyyy ")
            continue

    total_seats = input(' Total Number of seats : ')
    destination = input(' Destination: ')
    fare = input(' fare : ')
    description = input(' Tour description : ')

    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    sql_insert_query = """INSERT INTO Tour (tour_label, start_date, end_date, total_no_seats, 
                            available_seats, destination, fare, description) values (?,?,?,?,?,?,?,?);"""
    s_date = start_date.strftime("%d/%m/%Y")
    e_date = end_date.strftime("%d/%m/%Y")
    data_tuple = (tour_label, s_date, e_date, total_seats, total_seats, destination, fare, description)
    cursor.execute(sql_insert_query, data_tuple)
    cursor.execute("COMMIT;")
    cursor.close()

    print('Tour added successfully')

if __name__ == "__main__":
    addtour()
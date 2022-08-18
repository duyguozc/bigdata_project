import datetime
import sqlite3

def update_delete_tour(id):
    answer = input("Do you want to edit or delete the tour? (e/d)")
    if answer == 'e':
        edit_sql = ''
        stdate = input("Enter new start date or press ENTER to skip : ")
        if stdate != '':
            while True:
                try:
                    st = datetime.datetime.strptime(stdate, "%d/%m/%Y").date()
                    edit_sql = 'UPDATE Tour SET start_date = ' + '\''+st.strftime("%d/%m/%Y")+ '\''
                    break
                except ValueError:
                    print("Error: must be format dd/mm/yyyy")
                    stdate = input("Enter new start date : ")
                    continue

        end_date = input("Enter new end date or press ENTER to skip : ")
        if end_date != '':
            while True:
                try:
                    end = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
                    end = end.strftime("%d/%m/%Y")
                    if edit_sql == '':
                        edit_sql = 'UPDATE Tour SET end_date = ' + '\'' + end + '\''
                    else:
                        edit_sql = edit_sql + ' , end_date = ' + '\'' + end + '\''
                    break
                except ValueError:
                    print("Error: must be format dd/mm/yyyy")
                    end_date = input("Enter new end date : ")
                    continue

        capacity = input("Enter new capacity or press ENTER to skip : ")
        if capacity != '':
            capacity = int(capacity)
            if edit_sql == '':
                edit_sql = 'UPDATE Tour SET total_no_seats = ' + str(capacity)
            else:
                edit_sql = edit_sql + ' , total_no_seats = ' + str(capacity);

        fare = input("Enter new fare amount or press ENTER to skip : ")
        if fare != '':
            fare = float(fare)
            if edit_sql == '':
                edit_sql = 'UPDATE Tour SET fare = ' + str(fare)
            else:
                edit_sql = edit_sql + ' , fare = ' + str(fare);

        details = input("Enter new description or press ENTER to skip : ")
        if details != '':
            if edit_sql == '':
                edit_sql = 'UPDATE Tour SET description = ' + '\''+ str(details) + '\''
            else:
                edit_sql = edit_sql + ' , description = ' + '\'' + str(details) + '\''

        if edit_sql != '':
            edit_sql = edit_sql + ' WHERE id = ?'
            edit_tour(id, edit_sql)
            print("Tour is updated successfully.")
    elif answer == 'd':
        delete_tour(id)

def edit_tour(id, sql):
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    cursor.execute(sql, [id])
    connection.commit()
    connection.close()

def delete_tour(id):
    answer = input("Are you sure to delete the tour? (y/n)")
    if answer == 'y':
        sql = 'DELETE from Tour where id = ?'
        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        cursor.execute(sql, [id])
        connection.commit()
        connection.close()
        print("Tour is deleted successfully.")
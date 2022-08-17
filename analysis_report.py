import sqlite3
from classes import Payment
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import re


def retrieve_payment_data(year):
    all_payments = retrieve_all_payment_info(year)
    if len(all_payments) == 0:
        print("No record for year {}".format(year))
        return pd.DataFrame()
    else:
        column_names = ['user_id','booking_id','name','card_number','cvv','expiry_date','amount','transaction_date','transaction_type']
        payment_object_list = []
        for pay in all_payments:
            payment = list(pay[1:10])
            payment_object_list.append(payment)

        df = pd.DataFrame(payment_object_list, index = range(len(all_payments)),columns=column_names)
        return df

def generate_yearly_sales_report():
    payment_data = retrieve_all_years_data()
    column_names = ['user_id', 'booking_id', 'name', 'card_number', 'cvv', 'expiry_date', 'amount', 'transaction_date',
                    'transaction_type']
    payment_object_list = []
    for pay in payment_data:
        payment = list(pay[1:10])
        payment_object_list.append(payment)

    df = pd.DataFrame(payment_object_list, index=range(len(payment_data)), columns=column_names)
    df = df[df['transaction_type'] == 'sale']
    data_fr_index = pd.DatetimeIndex(df['transaction_date'], dayfirst=True)
    year_index = data_fr_index.year
    df['year'] = year_index
    yearly_sales = df.groupby(['year'], as_index=False)['amount'].sum()
    print(yearly_sales)
    plt.bar(yearly_sales['year'], yearly_sales['amount'], width=0.4)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Year")
    plt.ylabel("Sales Total $")
    plt.title("Sales by Years")
    plt.show()


def generate_monthly_sales_report(year):
    df = retrieve_payment_data(year)
    if(not df.empty):
        df = df[df['transaction_type'] == 'sale']
        data_fr_index = pd.DatetimeIndex(df['transaction_date'], dayfirst=True)
        month_index = data_fr_index.month
        df['month'] = month_index
        monthly_sales = df.groupby(['month'], as_index=False)['amount'].sum()
        print(monthly_sales)
        plt.bar(monthly_sales['month'], monthly_sales['amount'], width=0.4)
        plt.xticks(np.arange(0, 13, 1.0))
        plt.xlabel("Months")
        plt.ylabel("Sales Total $")
        plt.title("Sales by Monthly Basis in Year {}".format(year))
        plt.show()


def generate_quarterly_sales_report(year):
    df = retrieve_payment_data(year)
    if(not df.empty):
        df = df[df['transaction_type'] == 'sale']
        data_fr_index = pd.DatetimeIndex(df['transaction_date'], dayfirst=True)
        month_index = data_fr_index.month
        df['month'] = month_index
        conditions = [(df['month'] >= 1) & (df['month'] <= 3),
                      (df['month'] >= 4) & (df['month'] <= 6),
                      (df['month'] >= 7) & (df['month'] <= 9),
                      (df['month'] >= 10) & (df['month'] <= 12)
                      ]
        values =  ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']
        df['quarter'] = np.select(conditions, values)
        quarterly_sales = df.groupby(['quarter']).agg({'amount': ['sum']})
        quarterly_sales.columns = ['amount']
        quarterly_sales = quarterly_sales.reset_index()
        print(quarterly_sales)
        """
        plt.bar(quarterly_sales['quarter'], quarterly_sales['amount'], width=0.2)
        plt.xticks(np.arange(0, 5, 1.0))
        plt.xlabel("Quarters")
        plt.ylabel("Sales Total $")
        """
        plt.pie(quarterly_sales['amount'], labels=quarterly_sales['quarter'], autopct='%1.1f%%', startangle=90)

        plt.title("Total Sales for each Quarter in Year {}".format(year))
        plt.show()

def get_top_3_popular_destination(year):
    df = retrieve_payment_data(year)
    if(not df.empty):
        sql = "SELECT Payment.booking_id as booking_id, " \
                    " Payment.transaction_date as transaction_date, " \
                    " Payment.transaction_type as transaction_type, " \
                    " Booking.tour_id as tour_id, " \
                    " Tour.tour_label as tour_label, "\
                    " Tour.destination as destination," \
                    " Tour.description as description"\
            " FROM Payment" \
            " INNER JOIN Booking ON Booking.id == Payment.booking_id"\
            " INNER JOIN Tour ON Tour.id == Booking.tour_id"

        connection = sqlite3.connect('agency_database.db')
        cursor = connection.cursor()
        all_reocrds = cursor.execute(sql)
        payments_with_tour = all_reocrds.fetchall()

        column_names = ['booking_id', 'transaction_date', 'transaction_type', 'tour_id', 'tour_label', 'destination', 'description']
        payment_tuples_list = []
        for pay in payments_with_tour:
            payment = list(pay)
            payment_tuples_list.append(payment)

        connection.close()

        df = pd.DataFrame(payment_tuples_list, index = range(len(payments_with_tour)),columns=column_names)

        grouped = df.groupby(['destination']).agg({'destination': ['count']})
        grouped.columns = ['count']
        grouped = grouped.reset_index()
        grouped = grouped.sort_values('count', ascending=False)
        top3_dest = grouped.head(3)
        print(top3_dest)
        plt.bar(top3_dest['destination'], top3_dest['count'], width=0.3)
        plt.ylabel("Booking Amount")
        plt.title("Top 3 Destinations in {}".format(year))
        plt.show()


def retrieve_all_payment_info(year):
    sql = 'SELECT * FROM Payment WHERE transaction_date LIKE ?'
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    all_pays = cursor.execute(sql, ["%"+str(year)+"%"])
    payments = []
    if cursor.rowcount != 0:
        payments = all_pays.fetchall()
    connection.commit()
    connection.close()
    return payments

def retrieve_all_years_data():
    sql = 'SELECT * FROM Payment'
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    all_pays = cursor.execute(sql)
    payments = all_pays.fetchall()
    connection.commit()
    connection.close()
    return payments

def show_report_menu():
    select = 0
    while select != 5:
        print("****** Reports *******")
        print("1. Get/Export Yearly Sales report")
        print("2. Get/Export Monthly Sales report")
        print("3. Get/Export Quarter Sales report")
        print("4. Get/Export Most Popular 3 Destinations Report")
        print("5. Return to Main Menu")
        print("**********************")
        error = True
        while error:
            try:
                select = int(input("Select an option: "))
                error = False
            except ValueError:
                print("You should enter a number!")
                continue
            else:
                if select < 1 or select > 5:
                    print("You should enter a value between 1 and 5.")
        if select == 1:
            generate_yearly_sales_report()
        elif select == 2:
            year = get_year()
            generate_monthly_sales_report(year)
        elif select == 3:
            year = get_year()
            generate_quarterly_sales_report(year)
        elif select == 4:
            year = get_year()
            get_top_3_popular_destination(year)
        elif select == 5:
            return;

def get_year():
    err = True
    while err:
        year = input("Enter which year you want to analyze: ")
        match = re.match(r'.*([1-2][0-9]{3})', year)
        if match is None:
            print("You should enter a year between 2000-3000.")
        else:
            err = False
            return year


if __name__ == '__main__':
    show_report_menu()


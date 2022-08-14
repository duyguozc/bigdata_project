import sqlite3
from classes import Payment
import pandas as pd
import numpy as np
#from tabulate import tabulate
from matplotlib import pyplot as plt

def retrieve_payment_data():
    all_payments = retrieve_all_payment_info()
    column_names = ['user_id','booking_id','name','card_number','cvv','expiry_date','amount','transaction_date','transaction_type']
    payment_object_list = []
    for pay in all_payments:
        payment = list(pay[1:10])
        payment_object_list.append(payment)

    df = pd.DataFrame(payment_object_list, index = range(len(all_payments)),columns=column_names)
    return df


def generate_monthly_sales_report(year):
    df = retrieve_payment_data()
    df = df[df['transaction_type'] == 'sale']
    data_fr_index = pd.DatetimeIndex(df['transaction_date'], dayfirst=True)
    year_index = data_fr_index.year
    df['year'] = year_index
    df = df[df['year'] == year]
    month_index = data_fr_index.month
    month_index = data_fr_index.month
    df['month'] = month_index
    monthly_sales = df.groupby(['month'], as_index=False)['amount'].sum()
    print(monthly_sales)
    plt.bar(monthly_sales['month'], monthly_sales['amount'], width=0.4)
    plt.xticks(np.arange(0, 13, 1.0))
    plt.xlabel("Months")
    plt.ylabel("Sales Total $")
    plt.title("Total Profit for Months")
    plt.show()


def generate_quarterly_sales_report(year):
    df = retrieve_payment_data()
    df = df[df['transaction_type'] == 'sale']
    data_fr_index = pd.DatetimeIndex(df['transaction_date'], dayfirst=True)
    year_index = data_fr_index.year
    df['year'] = year_index
    df = df[df['year'] == year]
    month_index = data_fr_index.month
    df['month'] = month_index
    conditions = [(df['month'] >= 1) & (df['month'] <= 3),
                  (df['month'] >= 4) & (df['month'] <= 6),
                  (df['month'] >= 7) & (df['month'] <= 9),
                  (df['month'] >= 10) & (df['month'] <= 12)
                  ]
    values =  [1, 2, 3, 4]
    df['quarter'] = np.select(conditions, values)
    quarterly_sales = df.groupby(['quarter']).agg({'amount': ['sum']})
    quarterly_sales.columns = ['amount']
    quarterly_sales = quarterly_sales.reset_index()
    print(quarterly_sales)
    plt.bar(quarterly_sales['quarter'], quarterly_sales['amount'], width=0.2)
    plt.xticks(np.arange(0, 5, 1.0))
    plt.xlabel("Quarters")
    plt.ylabel("Sales Total $")
    plt.title("Total Profit for each Quarter in a Year")
    plt.show()

def get_top_3_popular_destination():
    sql = "SELECT Payment.booking_id as booking_id " \
          " Payment.transaction_date as transaction_date " \
          " Payment.transaction_date as transaction_date " \
          "FROM Payment" \





def retrieve_all_payment_info():
    sql = 'SELECT * FROM Payment'
    connection = sqlite3.connect('agency_database.db')
    cursor = connection.cursor()
    all_pays = cursor.execute(sql)
    payments = all_pays.fetchall()
    connection.commit()
    connection.close()
    return payments

if __name__ == '__main__':
    generate_monthly_sales_report(2022)
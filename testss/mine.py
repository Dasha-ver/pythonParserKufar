import csv
from sqlite3 import Error

import pandas
# pip install psycopg2
import psycopg2
from abc import ABC, abstractmethod


class Start:
    FILE_NAME = "mebel.csv"

    def get_connection(self):
        try:
            fields = ['link', 'price', 'description']
            with open(self.FILE_NAME, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
        except Error:
            print(Error)

    def create_mebel_table(self, conn):
        pass
        # fields = ['id', 'link', 'price', 'description']
        # with open(self.FILE_NAME, 'w', newline='') as file:
        #     writer = csv.DictWriter(file, fieldnames=fields)
        #     writer.writeheader()

    def get_items(self):
        df = pandas.read_csv(self.FILE_NAME)
        df["price"] = df["price"].astype(str).astype(int)
      #  df[df['col'].lt(-0.25) | df['col'].gt(0.25)]
        df = df[(df['price'] > 4)]
        print(df[["price", "link"]])

    def insert(self, conn, link, price, description):
        df = pandas.DataFrame({'link':[link], 'price':[price], 'description':[description]})
        df.to_csv('mebel.csv', mode='a', index=False, header=False)


start = Start()
s = start.get_connection()
start.create_mebel_table(s)
start.insert(s, "5", "6", "7")


start.insert(start, "1", "2", "3")
start.get_items()

# import pandas as pd
#
# #create DataFrame
# df = pd.DataFrame({'team': ['D', 'D', 'E', 'E'],
#  'points': [6, 4, 4, 7],
#  'rebounds': [15, 18, 9, 12]})
#
# df.to_csv('mebel.csv', mode='a', index= False , header= False )
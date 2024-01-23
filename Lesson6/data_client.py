import csv
import os
import sqlite3
from abc import ABC, abstractmethod
from sqlite3 import Error

import pandas
# pip install psycopg2
import psycopg2
import requests
from bs4 import BeautifulSoup


class DataClient(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def create_mebel_table(self, conn):
        pass

    @abstractmethod
    def get_items(self, conn, price_from=0, price_to=100000):
        pass

    @abstractmethod
    def insert(self, conn, link, price, description):
        pass

    def run_test(self):
        conn = self.get_connection()
        self.create_mebel_table(conn)
        items = self.get_items(conn, price_from=10, price_to=30)
        for item in items:
            print(item)
        conn.close()


class PostgresClient(DataClient):
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5432"

    def get_connection(self):
        try:
            connection = psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
            )
            return connection
        except Error:
            print(Error)

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS mebel
                (
                    id serial PRIMARY KEY, 
                    link text, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()


class Sqlite3Client(DataClient):
    DB_NAME = "kufar.db"

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            return conn
        except Error:
            print(Error)

    def create_mebel_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS mebel
                (
                    id integer PRIMARY KEY autoincrement, 
                    link text, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM mebel WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()


class CsvClient(DataClient):
    FILE_NAME = "mebel.csv"

    def get_connection(self):
        try:
            if os.path.exists(self.FILE_NAME):
                with open(self.FILE_NAME, 'a', newline='') as file:
                    return file
            else:
                with open(self.FILE_NAME, 'w', newline='') as file:
                    return file

        except Error:
            print(Error)

    def create_mebel_table(self, conn):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, 'a', newline='') as file:
                return file
        else:
            fields = ['link', 'price', 'description']
            with open(self.FILE_NAME, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                return file

    def get_items(self, conn, price_from=0, price_to=100):
        df = pandas.read_csv(self.FILE_NAME)
        df_list = []
        df["price"] = df["price"].astype(str).astype(int)
        df = df[df['price'].gt(0) & df['price'].lt(30)]
        df_list.append(df)
        return df_list

    def insert(self, conn, link, price, description):
        df = pandas.DataFrame({'link': [link], 'price': [price], 'description': [description]})
        df.to_csv(self.FILE_NAME, mode='a', index=False, header=False)


# data_client = PostgresClient()
# data_client = Sqlite3Client()
data_client = CsvClient()
data_client.run_test()

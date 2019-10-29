#!/usr/bin/python
import requests
import sqlite3
from sqlite3 import Error
import argparse
import contextlib

class DataLead():
    def __init__(self, dbname, API_KEY, args):
        self.dbname = dbname
        self.API_KEY = API_KEY
        self.args = args
        self.db = self.create_connection()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbname)
            print("Database is ready!")
        except Error as e:
            print(e)

        return conn

    def do_sth(self):
        print("This is test function")
        print(f"arg for that object is {self.args}")

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("The database connection has been closed.")


if __name__ == "__main__":
    API_KEY = '37ac9525'

    #DL = DataLead('movies.sqlite', API_KEY, 'randomargumentjustfortest')
    with contextlib.closing(DataLead('movies.sqlite', API_KEY, 'randomargumentjustfortest')) as DL:
        DL.do_sth()
    #DL.create_connection()


    # parser = argparse.ArgumentParser()
    # parser.add_argument("--sort_by", help="sort movies by columns")
    # args = parser.parse_args()
    # if args.sort_by:
    #     print("Sorted films go as follow...")

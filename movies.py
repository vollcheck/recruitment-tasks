#!/usr/bin/python
import sqlite3
from sqlite3 import Error
import requests, argparse, contextlib


class DataLead():
    def __init__(self, dbname, API_KEY, args):
        self.dbname = dbname
        self.API_KEY = API_KEY
        self.args = args
        self.db = self.open_connection()

    def open_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbname)
            print("Database is ready to go!")
        except Error as e:
            print(e)

        return conn

    def do_sth(self):
        print("do_sth function is printing")

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("The database connection has been closed.")


if __name__ == "__main__":
    API_KEY = '37ac9525'

    parser = argparse.ArgumentParser()
    parser.add_argument("--sort_by", help="sort movies by columns")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print("There are no arguments passed222!")
    elif args.sort_by:
        print("Sorted films go as follow...")

        with contextlib.closing(
                DataLead(
                    'movies.sqlite',
                    API_KEY,
                    args.sort_by)
        ) as DL:
            DL.do_sth()


    #DL.create_connection()
    #DL = DataLead('movies.sqlite', API_KEY, 'randomargumentjustfortest')

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

<<<<<<< HEAD
    # DB CONNECTION
    conn = sqlite3.connect('movies.sqlite')
    c = conn.cursor()
    c.execute('''SELECT title FROM movies''')
    con = c.fetchone()[0]

    # RESPONSE
    link = f'http://www.omdbapi.com/?t={con}&apikey={API_KEY}'
    response = requests.get(link)

    # TESTING
    # jr = response.json()
    d = response.json()
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(d)
    # print(d["Year"])

    f = open("response.txt", "w")
    f.write(str(d))

    columns = ['title', 'year', 'runtime',
               'genre', 'director', 'cast', 'writer',
               'language', 'country', 'awards',
               'imdb_rating', 'imdb_votes', 'box_office']


    #c.execute('''INSERT INTO movies ''')
    # print(type(response.json()))

    # END
    conn.close()

    for col, data in zip(columns, d):
        print(f"{col}: {data}")


    """


    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864
=======
    #DL = DataLead('movies.sqlite', API_KEY, 'randomargumentjustfortest')
    with contextlib.closing(DataLead('movies.sqlite', API_KEY, 'randomargumentjustfortest')) as DL:
        DL.do_sth()
    #DL.create_connection()
>>>>>>> b685657ea6005838b7b4060ac3f139267ba6669b


    # parser = argparse.ArgumentParser()
    # parser.add_argument("--sort_by", help="sort movies by columns")
    # args = parser.parse_args()
    # if args.sort_by:
    #     print("Sorted films go as follow...")

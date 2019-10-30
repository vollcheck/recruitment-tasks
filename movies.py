#!/usr/bin/python
import sqlite3
from sqlite3 import Error
import requests
import argparse
import contextlib


class DataLead():
    def __init__(self, dbname, API_KEY):
        self.dbname = dbname
        self.API_KEY = API_KEY
        self.db = self.open_connection()

    def open_connection(self):
        db = None
        try:
            db = sqlite3.connect(self.dbname)
            print("-- Database is ready to go!")
        except Error as e:
            print(e)

        return db

    def download_single_movie(self, _title):
        c = self.db.cursor()
        query = '''select title from movies where title=?'''
        c.execute(query, _title)
        return c.fetchall()

        # print(f"The '{_title}' movie will be downloaded now...")
        # link = f'http://www.omdbapi.com/?t={_title}&apikey={self.API_KEY}'
        # content = requests.get(link).json()
        # columns = ['Title', 'Year', 'Runtime',
        #            'Genre', 'Director', 'Actors', 'Writer',
        #            'Language', 'Country', 'Awards',
        #            'imdbRating', 'imdbVotes', 'BoxOffice']

        # dt = [content[col] for col in columns]
        # print(dt)

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("-- The database connection has been closed!")


if __name__ == "__main__":
    API_KEY = '37ac9525'

    parser = argparse.ArgumentParser()
    parser.add_argument("--sort_by", help="sort movies by columns")
    parser.add_argument("--download_single", help="download only one movie")
    args = parser.parse_args()

    with contextlib.closing(DataLead('movies.sqlite', API_KEY)) as DL:
        if not any(vars(args).values()):
            print("There are no arguments passed222!")
        elif args.download_single:
            DL.download_single_movie(args.download_single)

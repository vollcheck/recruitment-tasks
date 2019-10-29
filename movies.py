#!/usr/bin/python
import requests
import sqlite3
from sqlite3 import Error
import argparse


class DataLead():
    def __init__(self, db, API_KEY, args):
        self.db = db
        self.API_KEY = API_KEY
        self.args = args

    def download_single_movie(self):
        try:
            conn = sqlite3.connect(self.db)
            print("Database is ready!")
        except Error as e:
            print(e)

        # Make a cursor for playing with db
        c = conn.cursor()
        c.execute('''SELECT title FROM movies WHERE id=1;''')
        title = c.fetchall()

        # Requests response
        link = f'http://www.omdbapi.com/?t={title}&apikey={self.API_KEY}'
        content = requests.get(link).json()

        columns = ['Title', 'Year', 'Runtime',
                   'Genre', 'Director', 'Actors', 'Writer',
                   'Language', 'Country', 'Awards',
                   'imdbRating', 'imdbVotes', 'BoxOffice']

        dt = [content[col] for col in columns]

        print(dt)

        # query = '''UPDATE MOVIES ('Title', 'Year', 'Runtime',
        # 'Genre', 'Director', 'Cast', 'Writer',
        # 'Language', 'Country', 'Awards',
        # 'imdb_rating', 'imdb_votes', 'Box_office')
        # VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        # WHERE TITLE="The Shawshank Redemption"; '''

        # https://www.w3schools.com/sql/sql_update.asp

        # # conn.commit()
        # # END
        conn.close()


if __name__ == "__main__":
    API_KEY = '37ac9525'

    DL = DataLead('movies.sqlite', API_KEY, 'columns')
    DL.download_single_movie()

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--sort_by", help="sort movies by columns")
    # args = parser.parse_args()
    # if args.sort_by:
    #     print("Sorted films go as follow...")

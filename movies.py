#!/usr/bin/python
import requests
import sqlite3
from sqlite3 import Error
import argparse


class DataLead():
    def __init__(self, db, args):
        self.db = db
        self.args = args

    def check_db():
        """
        Used for checking if there is a film's missing data
        """
        pass

    def download_movie():
        """
        Used for filling the gaps for specified movie with the data from API
        """
        pass

    def sort_by():
        pass

    def filter_by():
        pass

    def compare_by():
        pass

    def add_movie():
        pass

    def show_highscores():
        pass

def db_con():
    conn = sqlite3.connect('movies.sqlite')
    c = conn.cursor()
    c.execute('''SELECT title FROM movies''')
    # con = c.fetchone()[0]
    data = c.fetchall()
    print(type(data))
    # conn.commit()
    # END
    conn.close()


def rest():
    # CONST
    API_KEY = '37ac9525'

    # RESPONSE
    link = f'http://www.omdbapi.com/?t={con}&apikey={API_KEY}'
    content = requests.get(link).json()

    columns = ['Title', 'Year', 'Runtime',  # 'Title' amd 'id' can be omitted
               'Genre', 'Director', 'Actors', 'Writer',
               'Language', 'Country', 'Awards',
               'imdbRating', 'imdbVotes', 'BoxOffice']

    dt = [content[col] for col in columns]

    query = '''INSERT INTO movies ('Title', 'Year', 'Runtime',
               'Genre', 'Director', 'Cast', 'Writer',
               'Language', 'Country', 'Awards',
               'imdb_rating', 'imdb_votes', 'Box_office')
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
               WHERE TITLE="The Shawshank Redemption"; '''

    # try:
    #     c.execute(query, dt)
    # except Error as e:
    #     print(e)




if __name__ == "__main__":

    # DB CONNECTION
    db_con()

    """
    http://www.omdbapi.com/?t=The Shawshank Redemption&apikey=37ac9525

    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864

    https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-in-python-how-to-map-json-keys-to-database-columns-prop

    """

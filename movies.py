#!/usr/bin/python
import sqlite3
import requests
import pprint
import json


if __name__ == "__main__":
    # CONST
    API_KEY = '37ac9525'

    # DB CONNECTION
    conn = sqlite3.connect('movies.sqlite')
    c = conn.cursor()
    c.execute('''SELECT title FROM movies''')
    con = c.fetchone()[0]

    # RESPONSE
    link = f'http://www.omdbapi.com/?t={con}&apikey={API_KEY}'
    content = requests.get(link).json()

    print(type(content))

    columns = ['Title', 'Year', 'Runtime',
               'Genre', 'Director', 'Actors', 'Writer',
               'Language', 'Country', 'Awards',
               'imdbRating', 'imdbVotes', 'BoxOffice']

    # END
    conn.close()

    # for col in columns:
    #     print(f"{col}: {content[col]}")

    dt = [f"{col}: {content[col]}" for col in columns]
    print(dt)

    """
    # for col, data in zip(columns, content):
    #     print(f"{col}: {data}")

    http://www.omdbapi.com/?t=The Shawshank Redemption&apikey=37ac9525

    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864

    https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-in-python-how-to-map-json-keys-to-database-columns-prop

    """

#!/usr/bin/python
import requests
import sqlite3
from sqlite3 import Error

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

    columns = ['Title', 'Year', 'Runtime',  # 'Title' amd 'id' can be omitted
               'Genre', 'Director', 'Actors', 'Writer',
               'Language', 'Country', 'Awards',
               'imdbRating', 'imdbVotes', 'BoxOffice']

    # dt = [f"{col}: {content[col]}" for col in columns]
    dt = [content[col] for col in columns]
    # print(dt)

    query = '''INSERT INTO movies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?); '''

    try:
        c.execute(query, dt)
    except Error as e:
        print(e)

    # END
    conn.close()

    """
    # for col, data in zip(columns, content):
    #     print(f"{col}: {data}")

    http://www.omdbapi.com/?t=The Shawshank Redemption&apikey=37ac9525

    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864

    https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-in-python-how-to-map-json-keys-to-database-columns-prop

    """

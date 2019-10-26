#!/usr/bin/python
import sqlite3
import requests
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
    response = requests.get(link)

    # TESTING
    # jr = response.json()
    downloaded = json.dumps(response.json())
    print(downloaded)
    #c.execute('''INSERT INTO movies ''')
    # print(type(response.json()))


    # CONVERT JSON TO SQLITE
    columns = ['id', 'title', 'year', 'runtime',
               'genre', 'director', 'cast', 'writer',
               'language', 'country', 'awards',
               'imdb_rating', 'imdb_votes', 'box_office']

    # END
    conn.close()

    """
    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864

    https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-in-python-how-to-map-json-keys-to-database-columns-prop

    """

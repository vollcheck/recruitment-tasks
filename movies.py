#!/usr/bin/python
import sqlite3
import requests


if __name__ == "__main__":
    API_KEY = '37ac9525'

    conn = sqlite3.connect('movies.sqlite')
    c = conn.cursor()
    c.execute('''SELECT title FROM movies''')

    con = c.fetchone()[0]

    link = f'http://www.omdbapi.com/?t={con}&apikey={API_KEY}'
    response = requests.get(link)

    print(response.status_code)
    jr = response.json()
    print(jr['Year'])

    conn.close()

    """
    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    https://medium.com/@mokashitejas/fetch-data-using-json-api-and-insert-into-sqlite3-db-83f25bc49864

    https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-in-python-how-to-map-json-keys-to-database-columns-prop

    """

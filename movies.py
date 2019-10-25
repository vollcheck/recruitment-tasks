#!/usr/bin/python
import sqlite3
import requests
import json


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

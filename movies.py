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
            print("---> Database is ready to go!")
        except Error as e:
            print(e)

        return db

    def download_single_movie(self, t):
        # Pull out the title from db
        c = self.db.cursor()
        c.execute("select title from movies where title=?", (t,))
        title_ = c.fetchone()[0]

        # Updating DB
        query_update = '''update movies set year=?, runtime=?, genre=?,
        director=?, cast=?, writer=?, language=?, country=?, awards=?,
        imdb_rating=?, imdb_votes=?, box_office=? where title=?'''
        c.execute(query_update, dt)
        self.db.commit()
        print("The movie has been downloaded.")

    def movie_json(self, title_):
        print(f"The '{title_}' is being downloaded now...")
        link = f'http://www.omdbapi.com/?t={title_}&apikey={self.API_KEY}'
        content = requests.get(link).json()
        # Pull the data from JSON
        columns = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer',
                   'Language', 'Country', 'Awards', 'imdbRating',
                   'imdbVotes', 'BoxOffice', 'Title']

        dt = [content[col] for col in columns]
        return dt

    def download_all_movies(self):
        c = self.db.cursor()
        c.execute("select title from movies")
        all_nested = c.fetchall()
        all_films = [film for sub in all_nested for film in sub]

        print(all_films)

        # query_update = '''update movies set year=?, runtime=?, genre=?,
        # director=?, cast=?, writer=?, language=?, country=?, awards=?,
        # imdb_rating=?, imdb_votes=?, box_office=? where title=?'''

        all = []
        for film in all_films:
            dt = self.movie_json(film)
            all.append(dt)

        print(all)

        # c.executemany(query_update, dt)
        # self.db.commit()
        # #print("The movie has been downloaded.")

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("---> The database connection has been closed!")


if __name__ == "__main__":
    API_KEY = '37ac9525'

    parser = argparse.ArgumentParser()
    parser.add_argument("--download_single", help="download one movie")
    parser.add_argument("--download_all", action='store_true', help="download all movies")
    parser.add_argument("--sort_by", help="sort movies by columns")
    args = parser.parse_args()

    with contextlib.closing(DataLead('movies.sqlite', API_KEY)) as DL:
        if not any(vars(args).values()):
            print("There are no arguments passed222!")
        elif args.download_all:
            DL.download_all_movies()
        elif args.download_single:
            DL.download_single_movie(args.download_single)

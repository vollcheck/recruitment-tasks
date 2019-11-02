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
        self.c = self.db.cursor()

    def open_connection(self):
        """Opens a connection with database for further data operations."""

        db = None
        try:
            db = sqlite3.connect(self.dbname)
            print("---> Database is ready to go!")
        except Error as e:
            print(e)

        return db

    def json_from_api(self, title):
        """Downloads the JSON movie's data from API with given title."""

        print(f"The '{title}' movie is being downloaded now...")
        link = f'http://www.omdbapi.com/?t={title}&apikey={self.API_KEY}'
        content = requests.get(link).json()

        # Pull the data from JSON
        columns = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer',
                   'Language', 'Country', 'Awards', 'imdbRating',
                   'imdbVotes', 'BoxOffice', 'Title']

        # dt = [content[col] for col in columns]
        dt = []
        for col in columns:
            # Ben Hur case, when there is no BoxOffice column
            if col in content:
                dt.append(content[col])
            else:
                dt.append(None)
        return dt

    def update_single_movie(self, title):
        """Function is made for easier development process."""

        # Pull out the title from db to check if the movie is in the base
        self.c.execute("select title from movies where title=?", (title,))
        title = self.c.fetchone()[0]

        dt = self.json_from_api(title)

        print(dt)  # Testing purposes; to delete before 'deploy'

        # Updating DB
        query_update = '''update movies set year=?, runtime=?, genre=?,
        director=?, cast=?, writer=?, language=?, country=?, awards=?,
        imdb_rating=?, imdb_votes=?, box_office=? where title=?'''
        self.c.execute(query_update, dt)
        self.db.commit()

        # Checking the newly added record
        cnew = self.db.cursor()
        cnew.execute("select * from movies where title=?", (title,))
        print(cnew.fetchone())
        print(f"The '{title}' movie has been downloaded.")

    def download_all_movies(self):
        """Function updating data about all movies appearing in the database."""

        all_nested = self.c.execute("select title from movies").fetchall()

        # Flatten the list of titles
        all_films = [film for sub in all_nested for film in sub]
        films_data = []
        for film in all_films:
            dt = self.json_from_api(film)
            films_data.append(dt)

        query_update = '''update movies set year=?, runtime=?, genre=?,
        director=?, cast=?, writer=?, language=?, country=?, awards=?,
        imdb_rating=?, imdb_votes=?, box_office=? where title=?'''

        self.c.executemany(query_update, films_data)
        self.db.commit()
        print("---> Database has been populated!")
        return self.c.lastrowid

    def sort_by(self, params):
        query = f'select title, {params} from movies order by {params}'
        result = self.c.execute(query).fetchall()
        for row in result:
            print(f'{row[0]:<38} {row[1]}')

    def filter_by(self, params):
        pass

    def compare(self, params):
        pass

    def add(self, title):
        "Adds a data of the movie with given title."
        query_select = f"""select * from movies where title='{title}'"""
        result = self.c.execute(query_select).fetchall()

        if not result:
            dt = self.json_from_api(title)
            dt.insert(0, dt.pop())  # Move last element to the front

            # Updating DB
            query_update = '''insert into movies(title, year, runtime, genre,
            director, cast, writer, language, country, awards, imdb_rating,
            imdb_votes, box_office) values(?,?,?,?,?,?,?,?,?,?,?,?,?)'''

            self.c.execute(query_update, dt)
            self.db.commit()
            print(f"The '{title}' movie has been downloaded.")
        else:
            print("The title is already in the database!\nDownloading aborted.")
        return self.c.lastrowid

    def highscores(self, args):
        categories = ['runtime', 'box_office', 'imdb_rating']
        query_select = f"""select title, runtime from movies order by cast(runtime as int) desc"""
        result1 = self.c.execute(query_select).fetchone()
        print(f'runtime {result1[0]:<38} {result1[1]}')

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("---> The database connection has been closed!")


if __name__ == "__main__":
    API_KEY = '37ac9525'
    DB_NAME = 'movies.sqlite'

    parser = argparse.ArgumentParser()
    parser.add_argument("--update_single", help="update one movie")
    parser.add_argument("--download_all", action='store_true', help="download all movies")
    parser.add_argument("--sort_by", help="sort movies by columns")
    parser.add_argument("--add", help="download and add a movie to the db")
    parser.add_argument("--highscores", action='store_true', help="shows highscores in many categories") # , action='store_true'
    args = parser.parse_args()

    with contextlib.closing(DataLead(DB_NAME, API_KEY)) as DL:
        if not any(vars(args).values()):
            print("There are no arguments passed!")
        elif args.download_all:
            DL.download_all_movies()
        elif args.update_single:
            DL.update_single_movie(args.update_single)
        elif args.sort_by:
            DL.sort_by(args.sort_by)
        elif args.add:
            DL.add(args.add)
        elif args.highscores:
            DL.highscores(args.highscores)

#!/usr/bin/python
import sqlite3
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
        except sqlite3.Error as e:
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

    def download_all_movies(self):
        """Populates data about all movies appearing in the database."""

        all_nested = self.c.execute("select trim(title) from movies").fetchall()

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
        """Sorts the database records by given column"""

        query = f"""select title, {params} from movies
        order by cast({params} as int) desc"""
        result = self.c.execute(query).fetchall()
        for row in result:
            print(f'{row[0]:<38} {row[1]}')

        return result

    def filter_by(self, params):
        """
        Function allows to filter movies by specified category
        included in the README.
        """

        simple_q = ['director', 'actor', 'language']
        if params[0] in simple_q:
            query = f"""select title, {params[0]} from movies
            where {params[0]} like '%{params[1]}%'"""
            result = self.c.execute(query).fetchall()
            print(f'title {params[0]:>35}')
            for row in result:
                print(f'{row[0]:<30} {row[1]}')

        elif params[0] == 'nominated':
            query = """select title, awards from movies
            where awards like 'Nominated for _ Oscars%'"""
            result = self.c.execute(query).fetchall()
            for row in result:
                print(f"{row[0]:<30} {row[1].split('.')[0]}")

        elif params[0] == 'percentage':
            query = """select title, awards from movies
            where awards like '%wins & %'"""
            result = self.c.execute(query).fetchall()
            print(f'title {params[0]:>40}')
            for row in result:
                newrow = row[1].split('.')
                if '&' in newrow[0]:
                    string = newrow[0]
                else:
                    string = newrow[1]
                numbers = [int(s) for s in string.split() if s.isdigit()]
                percentage = numbers[0]/numbers[1]
                if (float(percentage) >= 0.8):
                    print(f"{row[0]:<30} {percentage}")

        elif params[0] == 'earned_milion':
            query = """select title, box_office from movies
            where box_office like '$___,___,___%'"""
            result = self.c.execute(query).fetchall()
            print(f'title {params[0]:>35}')
            for row in result:
                print(f"{row[0]:<30} {row[1]}")

        return result

    def compare(self, params):
        """
        First argument should be the category of comparison, and last two
        args should be the titles of movies to compare.
        """

        query = f"""select title, {params[0]} from movies
        where title='{params[1]}' or title='{params[2]}'"""
        result = self.c.execute(query).fetchall()

        m1, m2 = result[0], result[1]
        num1, num2 = m1[1], m2[1]

        if params[0] == 'runtime':
            num1 = [int(s) for s in m1[1].split() if s.isdigit()][0]
            num2 = [int(s) for s in m2[1].split() if s.isdigit()][0]
        elif params[0] == 'box_office':
            num1 = 0 if 'N/A' in m1 else int(m1[1].replace(',', '').replace('$',''))
            num2 = 0 if 'N/A' in m2 else int(m2[1].replace(',', '').replace('$',''))
        elif params[0] == 'awards':
            if 'wins' in num1:
                num1 = num1.split(" wins")[0]
                s = num1.rfind(' ')
                num1 = int(num1[s+1:])
            else:
                num1 = 0
            if 'wins' in num2:
                num2 = num2.split(" wins")[0]
                s = num2.rfind(' ')
                num2 = int(num2[s+1:])
            else:
                num2 = 0

        if num1 is num2:
            res = f"Compared movies has the same score in {params[0]}."
            print(res)
        else:
            if num1 > num2:
                high = [m1[0], num1]
                low = [m2[0], num2]
            else:
                high = [m2[0], num2]
                low = [m1[0], num1]
            res = f"""'{high[0]}' ({high[1]}) has more awards
            than '{low[0]}' ({low[1]})"""
            print(res)

        return res

    def add(self, title: str):
        "Adds a data of the movie with given title."

        query_select = f"select * from movies where title='{title}'"
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
        categories = ['Runtime', 'Box_Office', 'IMDB_Rating', 'Awards']

        query1 = f"""select title, runtime from movies
        order by cast(runtime as int) desc"""
        query2 = f"""select title, box_office from movies
        order by cast(box_office as float) desc"""
        query3 = f"""select title, imdb_rating from movies
        order by imdb_rating desc"""
        query4 = f"""select title, awards from movies
        order by awards desc"""

        queries = [query1, query2, query3, query4]
        for q in queries:
            res = self.c.execute(q).fetchone()
            print(res[0], res[1])

        # print(f'{categories[2]} {result_awards[0]:<20} {result_awards[1]}')

    def close(self):
        if self.db:
            self.db.close()
            self.db = None
            print("---> The database connection has been closed!")


if __name__ == "__main__":
    API_KEY = '37ac9525'
    DB_NAME = 'movies.sqlite'

    parser = argparse.ArgumentParser()
    parser.add_argument("--download_all", action='store_true',
                        help="download all movies")
    parser.add_argument("--sort_by",
                        # nargs='+',
                        help="sort movies by columns")
    parser.add_argument("--filter_by",
                        nargs='+',
                        help="sort movies by columns")
    parser.add_argument("--compare",
                        nargs='+',
                        help="compare two movies by given value")
    parser.add_argument("--add", help="download and add a movie to the db")
    parser.add_argument("--highscores", action='store_true',
                        help="shows highscores in many categories")
    args = parser.parse_args()

    with contextlib.closing(DataLead(DB_NAME, API_KEY)) as DL:
        if not any(vars(args).values()):
            print("There are no arguments passed!")
        elif args.download_all:
            DL.download_all_movies()
        elif args.sort_by:
            DL.sort_by(args.sort_by)
        elif args.filter_by:
            DL.filter_by(args.filter_by)
        elif args.compare:
            DL.compare(args.compare)
        elif args.add:
            DL.add(args.add)
        elif args.highscores:
            DL.highscores(args.highscores)

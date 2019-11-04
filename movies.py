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

    def compare(self, params):
        """
        First argument should be the category of comparison, and last two
        args should be the titles of movies to compare.
        """

        print(params)
        query = f"""select title, {params[0]} from movies
        where title='{params[1]}' or title='{params[2]}'"""
        result = self.c.execute(query).fetchall()

        print("result: ", result)
        m1 = result[0]
        m2 = result[1]

        #if isinstance(m1[1], str):
        if params[0] == 'runtime':
            num1 = [int(s) for s in m1[1].split() if s.isdigit()]
            num2 = [int(s) for s in m2[1].split() if s.isdigit()]
            print(num1)
            print(num2)

        elif params[0] == 'imdb_rating':
            num1 = m1[1]
            num2 = m2[1]
            high, low = [m1, m2] if num1 > num2 else [m2, m1]
            # low = m1 if num1 < num2 else m2

            print("high", high)
            print("low", low)
            # if num1 == num2:
            #     print(f"Movies are equal to each other comparing on {params[0]}")
            # elif num1 > num2:
            #     high = m1
            #     low = m2
            #     print(f"{m1[0]}({m1[1]}) has higher {params[0]} than {m2[0]}({m2[1]})")
            # else:
            #     high = m2
            #     low = m1

        elif params[0] == 'box_office':

            if num1 == num2:
                print(f"Movies are equal to each other comparing on {params[0]}")
            elif num1 > num2:
                high = m1
                low = m2
                print(f"{m1[0]}({m1[1]}) has higher {params[0]} than {m2[0]}({m2[1]})")
            else:
                high = m2
                low = m1

            print(f"{high[0]}({high[1]}) has higher {params[0]} than {low[0]}({low[1]})")

        #     if not int(movie1[1]) == int(movie2[1]):
        #         print(f"Movies are equal to each other comparing on {params[0]}")
        #         return result
        #     elif int(movie1[1]) > int(movie2[1]):
        #         high = movie1
        #         low = movie2
        #     else:
        #         high = movie2
        #         low = movie1

        #     print(f"'{movie1[0]}'({movie1[1]}) has higher {params[0]} than '{movie2[0]}'({movie2[1]})")
        #     return result


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
    parser.add_argument("--update_single", help="update one movie")
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
        elif args.update_single:
            DL.update_single_movie(args.update_single)
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

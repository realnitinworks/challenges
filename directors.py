import csv
from collections import defaultdict, namedtuple
import os
from urllib.request import urlretrieve
import statistics

BASE_URL = 'https://bites-data.s3.us-east-2.amazonaws.com/'
TMP = '/tmp'

fname = 'movie_metadata.csv'
remote = os.path.join(BASE_URL, fname)
local = os.path.join(TMP, fname)
urlretrieve(remote, local)

MOVIE_DATA = local
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    movies_by_director = defaultdict(list)
    with open(local, encoding="utf8") as f:
        reader = csv.DictReader(f)
        for movie in reader:
            title_year = movie['title_year'] and int(movie['title_year']) or 0
            if title_year >= 1960:
                director_name = movie['director_name']
                movie_title = movie['movie_title'].strip()[:-1]
                imdb_score = float(movie['imdb_score'])
                movies_by_director[director_name].append(Movie(movie_title, title_year, imdb_score))
    return movies_by_director


def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    mean_score = statistics.mean(
        movie.score
        for movie in movies
    )

    return round(mean_score, 1)


def get_average_scores(directors):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    interested_directors = {
        director: movies
        for director, movies in get_movies_by_director().items()
        if len(movies) >= MIN_MOVIES
    }

    average_scores_by_director = [
        (director, calc_mean_score(movies))
        for director, movies in interested_directors.items()
    ]

    return sorted(average_scores_by_director, key=lambda x: x[1], reverse=True)

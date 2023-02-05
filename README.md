# KNN Recommender

By using [MovieLens Datasets](https://grouplens.org/datasets/movielens/latest/) we build a recommender system based on KNN Item-Based Collaborative Filtering.

## Enviroment Setup

Use [poetry](https://python-poetry.org/) to set up the Python environment (Python >= 3.9)

Get the full data set from [MovieLens Datasets](https://grouplens.org/datasets/movielens/latest/) and put the `movies.csv` and `ratings.csv` in this repo.

## Migrate data into database

Using the [Django admin](https://docs.djangoproject.com/en/4.1/ref/django-admin/) [custom management CLI commands](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/):

- python manage.py load_movies --path <path_to_movies.csv>
- python manage.py load_ratings --path <path_to_ratings.csv>

## Training data

Using the [Django admin](https://docs.djangoproject.com/en/4.1/ref/django-admin/) [custom management CLI commands](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/):

- python manage.py prep_data --path <path_to_static_folder>

Train and produce the `hashmap.p`, `movie_user_mat_sparse.p` for deployment. Put in the path you want them to be stored. (e.g. recommender/static/model/)

## Run the app

Start the server:

- python manage.py runserver

App runs in url: http://127.0.0.1:8000/recommender/

---

*Credit to Kevin Laio ([KevinLiao159](https://github.com/KevinLiao159)) for [original code](https://github.com/KevinLiao159/MyDataSciencePortfolio/blob/master/movie_recommender/src/knn_recommender.py) and [blog post](https://towardsdatascience.com/prototyping-a-recommender-system-step-by-step-part-1-knn-item-based-collaborative-filtering-637969614ea)*

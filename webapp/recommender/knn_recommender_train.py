# originally from https://github.com/KevinLiao159/MyDataSciencePortfolio/blob/master/movie_recommender/src/knn_recommender.py

import gc
import pickle

# data science imports
import pandas as pd
from scipy.sparse import csr_matrix

# data imports
from recommender.models import Movies, Ratings

def prep_data(movie_rating_thres, user_rating_thre):
    """
    prepare data for recommender

    1. movie-user scipy sparse matrix
    2. hashmap of movie to row index in movie-user scipy sparse matrix
    """

    # read data
    print("read data...")

    df_movies = pd.DataFrame(list(Movies.objects.all().values('movie_id', 'title')))
    df_movies = df_movies.astype(dtype={'movie_id': 'int32', 'title': 'str'})

    df_ratings = pd.DataFrame(list(Ratings.objects.all().values('user_id', 'movie_id','rating')))
    df_ratings = df_ratings.astype(dtype={'user_id': 'int32', 'movie_id': 'int32', 'rating': 'float32'})

    print(df_movies.head())
    print(df_ratings.head())

    # filter data
    print("filter data...")
    df_movies_cnt = pd.DataFrame(
        df_ratings.groupby('movie_id').size(),
        columns=['count'])
    popular_movies = list(set(df_movies_cnt.query('count >= @movie_rating_thres').index))  # noqa
    movies_filter = df_ratings.movie_id.isin(popular_movies).values

    df_users_cnt = pd.DataFrame(
        df_ratings.groupby('user_id').size(),
        columns=['count'])
    active_users = list(set(df_users_cnt.query('count >= @user_rating_thres').index))  # noqa
    users_filter = df_ratings.user_id.isin(active_users).values

    df_ratings_filtered = df_ratings[movies_filter & users_filter]

    # pivot and create movie-user matrix
    print("pivot and create movie-user matrix...")
    movie_user_mat = df_ratings_filtered.pivot(
        index='movie_id', columns='user_id', values='rating').fillna(0)
    # create mapper from movie title to index
    print("create mapper from movie title to index...")
    hashmap = {
        movie: i for i, movie in
        enumerate(list(df_movies.set_index('movie_id').loc[movie_user_mat.index].title)) # noqa
    }
    # transform matrix to scipy sparse matrix
    print("transform matrix to scipy sparse matrix...")
    movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

    # clean up
    print("clearn up...")
    del df_movies, df_movies_cnt, df_users_cnt
    del df_ratings, df_ratings_filtered, movie_user_mat
    gc.collect()
    return movie_user_mat_sparse, hashmap

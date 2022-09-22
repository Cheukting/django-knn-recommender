# originally from https://github.com/KevinLiao159/MyDataSciencePortfolio/blob/master/movie_recommender/src/knn_recommender.py

import os
import pickle

# data science imports
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz

class KnnRecommender:
    """
    This is an item-based collaborative filtering recommender with
    KNN implmented by sklearn
    """
    def __init__(self, path_hashmap, path_movie_user_mat_sparse):
        """
        Recommender requires path to data: movies data and ratings data

        Parameters
        ----------
        path_movies: str, movies data file path

        path_ratings: str, ratings data file path
        """
        self.path_hashmap = path_hashmap
        self.path_movie_user_mat_sparse = path_movie_user_mat_sparse
        self.model = NearestNeighbors()

    def set_model_params(self, n_neighbors, algorithm, metric, n_jobs=None):
        """
        set model params for sklearn.neighbors.NearestNeighbors

        Parameters
        ----------
        n_neighbors: int, optional (default = 5)

        algorithm: {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional

        metric: string or callable, default 'minkowski', or one of
            ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']

        n_jobs: int or None, optional (default=None)
        """
        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _fuzzy_matching(self, hashmap, fav_movie):
        """
        return the closest match via fuzzy ratio.
        If no match found, return None

        Parameters
        ----------
        hashmap: dict, map movie title name to index of the movie in data

        fav_movie: str, name of user input movie

        Return
        ------
        index of the closest match
        """
        match_tuple = []
        # get match
        for title, idx in hashmap.items():
            ratio = fuzz.ratio(title.lower(), fav_movie.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
        else:
            print('Found possible matches in our database: '
                  '{0}\n'.format([x[0] for x in match_tuple]))
            return match_tuple[0][1]

    def _inference(self, model, data, hashmap,
                   fav_movie, n_recommendations):
        """
        return top n similar movie recommendations based on user's input movie

        Parameters
        ----------
        model: sklearn model, knn model

        data: movie-user matrix

        hashmap: dict, map movie title name to index of the movie in data

        fav_movie: str, name of user input movie

        n_recommendations: int, top n recommendations

        Return
        ------
        list of top n similar movie recommendations
        """
        # fit
        model.fit(data)
        # get input movie index
        idx = self._fuzzy_matching(hashmap, fav_movie)
        # inference
        distances, indices = model.kneighbors(
            data[idx],
            n_neighbors=n_recommendations+1)
        # get list of raw idx of recommendations
        raw_recommends = \
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                ),
                key=lambda x: x[1]
            )[:0:-1]
        # return recommendation (movieId, distance)
        return raw_recommends

    def make_recommendations(self, fav_movie, n_recommendations):
        """
        make top n movie recommendations

        Parameters
        ----------
        fav_movie: str, name of user input movie

        n_recommendations: int, top n recommendations
        """
        # get data
        movie_user_mat_sparse = pickle.load(open(self.path_movie_user_mat_sparse, "rb"))
        hashmap = pickle.load(open(self.path_hashmap, "rb"))
        # get recommendations
        raw_recommends = self._inference(
            self.model, movie_user_mat_sparse, hashmap,
            fav_movie, n_recommendations)
        reverse_hashmap = {v: k for k, v in hashmap.items()}
        return [reverse_hashmap[recommend[0]] for recommend in raw_recommends]

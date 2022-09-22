import csv
import pickle
from django.core.management import BaseCommand
from recommender.knn_recommender import KnnRecommender

class Command(BaseCommand):
    help = 'Train the model and deploy to path'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        base_path = kwargs['path'].rstrip('/')
        path_hashmap = base_path + "/hashmap.p"
        path_movie_user_mat_sparse = base_path + "/movie_user_mat_sparse.p"
        movie_user_mat_sparse, hashmap = prep_data(50, 50)
        pickle.dump(movie_user_mat_sparse, open(path_movie_user_mat_sparse, "wb"))
        pickle.dump(hashmap, open(path_hashmap, "wb"))

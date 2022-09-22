import csv
from django.core.management import BaseCommand
from recommender.models import Movies

class Command(BaseCommand):
    help = 'Load a movies csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            next(reader, None)
            bulk_movies=[]
            for row in reader:
                bulk_movies.append(
                            Movies(
                                movie_id=row[0],
                                title=row[1],
                            )
                        )
                if len(bulk_movies) > 5000:
                    Movies.objects.bulk_create(bulk_movies)
                    bulk_movies=[]
            if bulk_movies:
                Movies.objects.bulk_create(bulk_movies)

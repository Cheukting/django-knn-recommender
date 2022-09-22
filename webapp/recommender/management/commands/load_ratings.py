import csv
from django.core.management import BaseCommand
from recommender.models import Ratings

class Command(BaseCommand):
    help = 'Load a ratings csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            next(reader, None)
            bulk_ratings=[]
            for row in reader:
                bulk_ratings.append(
                            Ratings(
                                user_id=row[0],
                                movie_id=row[1],
                                rating=row[2],
                            )
                        )
                if len(bulk_ratings) > 5000:
                    Ratings.objects.bulk_create(bulk_ratings)
                    bulk_ratings=[]
            if bulk_ratings:
                Ratings.objects.bulk_create(bulk_ratings)

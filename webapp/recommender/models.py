from django.db import models


class Movies(models.Model):
    movie_id = models.CharField(max_length=10)
    title = models.CharField(max_length=200)


class Ratings(models.Model):
    user_id = models.CharField(max_length=10)
    movie_id = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=5, decimal_places=2)

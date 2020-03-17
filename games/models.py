from django.db import models
from django.contrib import admin
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=50, db_index=True, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # slug = models.SlugField(max_length=70, db_index=True)
    game_url = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RegisterUser(models.Model):
    number = models.CharField(max_length=18, blank=True, null=True)

    def __str__(self):
        return str(self.number)


class RecentlyPlayed(models.Model):
    user = models.ForeignKey(RegisterUser, models.DO_NOTHING)
    game = models.ForeignKey(Game, models.DO_NOTHING)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.game)

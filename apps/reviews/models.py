from __future__ import unicode_literals

from django.db import models
from ..loginreg.models import User
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)

class Review(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    rating = models.IntegerField()
    review = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)

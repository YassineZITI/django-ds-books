from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator ,MinLengthValidator
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000,blank=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=13,validators=[MinLengthValidator(13)])
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=8000,default='')
    author = models.CharField(max_length=255)
    publisher = models.CharField(default='',max_length=255)
    published = models.CharField(default='',max_length=255)
    pages = models.CharField(default='-',max_length=50)
    stars = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.CharField(max_length=50)
    image = models.URLField(max_length=200)
    category = models.ForeignKey(Category,related_name='Books',on_delete=models.CASCADE)
    similar_books = models.CharField(max_length=300)
    embedding = ArrayField(models.FloatField(),size=300,null=True,blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('home')



class ReviewRating(models.Model):
    book = models.ForeignKey(Book,on_delete = models.CASCADE,related_name='bookreview')
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='userreview')
    rating = models.IntegerField()
    subject = models.CharField(max_length=255,blank=True)
    review = models.TextField(max_length=2000,blank=True)
    def __str__(self):
        return self.subject
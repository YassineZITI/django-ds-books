from django.contrib import admin
from .models import Book,ReviewRating,Category
# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(ReviewRating)
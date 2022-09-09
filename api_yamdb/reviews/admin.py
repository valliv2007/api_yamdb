from django.contrib import admin

from .models import Category, Titles, Genre, GenreTitle, Review, Comment

admin.site.register(Titles)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)

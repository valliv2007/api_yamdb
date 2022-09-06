from django.contrib import admin

from .models import Category, Titles, Genre, GenreTitle

admin.site.register(Titles)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)

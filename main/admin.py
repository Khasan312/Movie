from django.contrib import admin

from .models import *


class FilmImageInline(admin.TabularInline):
    model = FilmImage
    max_num = 10
    min_num = 1


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [FilmImageInline, ]


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Favorite)

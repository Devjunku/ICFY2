from django.contrib import admin
from .models import Movie, Review


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'vote_average',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'review_score', 'content', 'created_at', 'updated_at',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Movie, MovieAdmin)

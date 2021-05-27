from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Movie(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    adult = models.BooleanField()
    # genre_id
    genre_ids = models.TextField()
    popularity = models.DecimalField(max_digits=20, decimal_places=10)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.TextField(null=True)
    vote_average = models.DecimalField(max_digits=4, decimal_places=2)
    vote_count = models.PositiveIntegerField()
    # upcoming 같은 것을 저장할 필드를 추가할 예정이다.

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review_score = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

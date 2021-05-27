from rest_framework import serializers
from .models import Movie, Review, Comment


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'poster_path', 'vote_average', 'adult', 'vote_count', 'genre_ids')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)


class ReviewListSerializer(serializers.ModelSerializer):

    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user',)




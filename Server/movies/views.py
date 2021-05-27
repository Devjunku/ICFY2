from re import I
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Movie, Review, Comment
from .serializers import MovieListSerializer, ReviewListSerializer, CommentSerializer

import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
@api_view(['GET', 'POST'])
def movie_index(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 로그인한 사용자만 볼 수 있도록
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = MovieListSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def community(request, movie_id):
    # GET 방식이면 리뷰를 보는 행위
    if request.method == 'GET':
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = movie.review_set.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.vote_count += 1

    # 리뷰 점수 반영
    new_score = (movie.vote_average * movie.vote_count + request.data.get('review_score')) / (movie.vote_count + 1)
    new_score = round(new_score, 2)
    movie.vote_average = new_score
    
    movie.save()

    serializers = ReviewListSerializer(data=request.data)
    if serializers.is_valid(raise_exception = True):
        serializers.save(movie=movie, user=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # GET 방식이면, detail 페이지 데이터 전송
    if request.method == 'GET':
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    elif request.method == 'POST':
        review = get_object_or_404(Review, id=review_pk)
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid(raise_exception = True):
            serializers.save(review=review, user=request.user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
           

    # PUT 방식이면 리뷰를 작성 데이터를 DB에 수정 후 전송
    elif request.method == 'PUT':
        movie = get_object_or_404(Movie, id=review.movie_id)
        new_score = (movie.vote_average * movie.vote_count + request.data.get('review_score') -request.data.get('storage')) / (movie.vote_count)
        new_score = round(new_score, 2)
        movie.vote_average = new_score
        movie.save()

        new_data = {
            "title" : request.data.get('title'),
            "content" :request.data.get('content'),
            "review_score" : request.data.get('review_score')
        }
        serializer = ReviewListSerializer(review, data=new_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_delete(request, review_pk, score):
    review = get_object_or_404(Review, pk=review_pk)
    # DELETE 방식이면 리뷰를 작성 데이터를 DB에 삭제 후 전송
    movie = Movie.objects.get(id=review.movie_id)

    new_score = (movie.vote_average * movie.vote_count - score ) / (movie.vote_count - 1)
    movie.vote_count -= 1
    new_score = round(new_score, 2)
    movie.vote_average = new_score
    movie.save()

    review.delete()
    return Response({'movie_id': review.movie_id})

@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['DELETE', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'DELETE':
        comment.delete()
        return Response({'comment_id': comment.id})

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_info(request, user_id):
    
    # 작성한 리뷰가 없으면 404 에러가 난다.
    # reviews = get_list_or_404(Review, user_id=user_id)
    # comments = get_list_or_404(Comment, user_id=user_id)

    # 그래서 이렇게 쓰겠다.
    reviews = Review.objects.filter(user_id=user_id)
    comments = Comment.objects.filter(user_id=user_id)

    if request.method == 'GET':
        review_serializer = ReviewListSerializer(reviews,  many=True)
        comment_serializer = CommentSerializer(comments, many=True)
        # [{}, {}] 이런 형태로 들어오는데 이렇게 해줘야 구분할 수 있다.
        return Response({
            'review': review_serializer.data,
            'comment': comment_serializer.data,
        })

def get_recommend_movie_list(movie, movies, similar, top=30):
    search_movie_idx = movie.index.values
    similar_idx = similar[search_movie_idx, :top].reshape(-1)
    similar_idx = similar_idx[similar_idx != search_movie_idx] # 제목이 movie_title 인 영화 제외
    res_idx = list(similar_idx)
    random.shuffle(res_idx)
    input_idx = res_idx[:6]
    result = movies.iloc[input_idx].sort_values('popularity', ascending=False)[:6]
    print(result.index.values)
    return result


@api_view(['GET'])
# 아직은 프로토 타입
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def recommend(request, movie_id):
    if Movie.objects.get(id=movie_id):

        movies = pd.DataFrame(list(Movie.objects.all().values()))
        movie = movies[movies['id'] == movie_id]

        transformer = CountVectorizer()
        genres_vector = transformer.fit_transform(movies['genre_ids'])
        similar = cosine_similarity(genres_vector, genres_vector)
        similar = similar.argsort()
        similar = similar[:, ::-1]
        res = get_recommend_movie_list(movie, movies, similar)

        res_dict = []
        # print(list(res['id']))
        for i in range(6):
            r_d = {
            'id': list(res['id'])[i],
            'adult': list(res['adult'])[i],
            'genre_ids': list(res['genre_ids'])[i],
            'popularity': list(res['popularity'])[i],
            'title': list(res['title'])[i],
            'overview': list(res['overview'])[i],
            'poster_path': list(res['poster_path'])[i],
            'vote_average': list(res['vote_average'])[i],
            'vote_count': list(res['vote_count'])[i],
            }
            res_dict.append(r_d)

        return Response(res_dict)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    me = request.user
    # 목록에 있다.
    flag = 1
    # 요청을 보낸 유저의 좋아요 목록에 이 영화가 있다면
    if me.like_movies.filter(id=movie_id).exists():
        # 목록에서 빼기
        me.like_movies.remove(movie)
        # 이제 없다.
        flag = 0

    # 없다면
    else:
        # 목록에 넣기
        me.like_movies.add(movie)

    return Response({"flag": flag, "vote_count": movie.vote_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def show_like_movies(request):
    me = request.user
    movies = me.like_movies.all()
    serializer = MovieListSerializer(movies,  many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def similarity(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)
    me = request.user
    movies = me.like_movies.all()

    if movies:

        if not me.like_movies.filter(id=movie_id).exists():
            movies = pd.DataFrame(list(movies.values()))
            movie = pd.DataFrame(list(Movie.objects.filter(id=movie_id).values()))
            movies = movies.append(movie)
            
            transformer = CountVectorizer()
            genres_vector = transformer.fit_transform(movies['genre_ids'])
            similar = cosine_similarity(genres_vector, genres_vector)
            
            res_value = 0
            N = len(similar[-1])
            N_value = 0
            for a in range(N-1):
                if similar[-1][a]:
                    res_value += similar[-1][a]
                    N_value += 1
                    print(similar[-1][a])
            
            if not N_value:
                return Response({
                    'similar': f'{request.user.username}님의 정보가 부족해서 {request.user.username}님의 취향을 알 수 없어요!'
                })

            res_value /= N_value
            res_value *= 100

            if 0.4 < res_value:
                return Response({
                    'similar': f'{request.user.username}님의 취향저격{res_value:.0f}%!'
                })     
            else:
                return Response({
                    'similar': f'{request.user.username}님의 취향과 너무 거리가 있네요! 하지만 진정한 영화인은 모든 영화를 섭렵하는법! 취향저격{res_value:.0f}%!'
                })

        return Response({
                'similar': f'좋아요!'
            })
    else:
        return Response({
                'similar': f'좋아요를 누른 영화로 {request.user.username}님의 취향을 알아가 볼게요!'
            })

@api_view(['GET'])
def search(request):
    search = request.GET.get('q')
    results = Movie.objects.filter(title__icontains=search)
    serializer = MovieListSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def show_like_other_movies(request, user_id):
    person = get_object_or_404(get_user_model(), id=user_id)
    movies = person.like_movies.all()
    serializer = MovieListSerializer(movies,  many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def checkHeart(request, movie_id):
    flag = 0
    # 좋아요 된 상황
    if request.user:
        return Response({'flag': flag}, status=status.HTTP_200_OK)
    if request.user.like_movies.filter(id=movie_id).exists():
        flag =1 
    return Response({'flag': flag}, status=status.HTTP_200_OK)


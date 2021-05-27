from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # 메인 페이지 (여러 가지 추천 영화가 나온다.)
    path('', views.movie_index),
    # 단일 영화 페이지
    path('<int:movie_id>/', views.movie_detail),
    # GET : 특정 영화에 대한 커뮤니티
    path('<int:movie_id>/community/', views.community),
    # POST: 특정 영화에 대한 리뷰 생성
    path('<int:movie_id>/reviews/', views.review_create),
    # GET : 특정 리뷰 보기, 댓글들이 같이 나온다.
    # PUT : 특정 리뷰 수정
    # POST: 특정 댓글 생성
    path('community/<int:review_pk>/', views.review_detail),
    
    # DELETE : 특정 리뷰 삭제 
    path('community/<int:review_pk>/<int:score>/', views.review_delete),

    # PUT : 특정 댓글 수정
    # DELETE : 특정 댓글 삭제
    path('comments/<int:comment_id>/', views.change_comment),

    # 추천 영화
    path('<int:movie_id>/recommend/', views.recommend),

    # 하트 정보 가져오기
    path('checkheart/<int:movie_id>/', views.checkHeart),

    # 유저 유사도
    path('<int:movie_id>/similarity/', views.similarity),
    # GET : 특정 유저가 작성한 리뷰 댓글 조회
    # 유저도 관련되지만 중점은 리뷰와 댓글이기에 이곳에 작성하겠다.
    path('profile/<int:user_id>/', views.profile_info),

    # like 기능 (디테일에서 하트 표시용)
    path('like/<int:movie_id>/', views.like_movie),
    # like 기능 (마이 프로필에서 하트 누른 영화들 보여주기용)
    path('like/show/', views.show_like_movies),
    # like 기능 (다른 사람 프로필에서 하트 누른 영화들 보여주기용)
    path('like/show/<int:user_id>/', views.show_like_other_movies),
    # 검색 데이터 연산
    path('search/', views.search),

]
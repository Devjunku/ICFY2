from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api-token-auth/',  obtain_jwt_token),
    
    # 비밀번호 변경
    path('password/', views.password, name='password'),

    # 회원 탈퇴
    path('delete/', views.delete, name='delete'),

    # 둘을 같게 해주었더니 앞의 url로만 요청이 간다.
    # path('check/<str:username>/', views.check, name='check'),
    # path('check/<int:user_id>/', views.find_username, name='find_username'),
    
    path('check/<str:username>/', views.check, name='check'),
    path('find/<int:user_id>/', views.find_username, name='find_username'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('followinfo/<int:user_id>/', views.follow, name='follow'),
    path('follow/<int:user_id>/', views.follow_change, name='follow_change'),
    # path('delete/', views.delete, name='delete'),
    # path('update/', views.update, name='update'),
    # path('password/', views.change_password, name='change_password'),
    # path('<int:user_pk>/follow/', views.follow, name='follow'),
]
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileSerializer, UserCheckSerializer, FollowSerializer
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    serializer = UserProfileSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def check(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    serializer = UserCheckSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def find_username(request, user_id):
    person = get_object_or_404(get_user_model(), id=user_id)
    serializer = UserCheckSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    # 팔로우 받는 사람
    you = get_object_or_404(get_user_model(), id=user_id)
    
    followings = you.followings.all()
    followers = you.followers.all()
    
    flag = 0
    if you.followers.filter(id=request.user.id).exists():
        flag = 1

    followings_serializer = FollowSerializer(followings, many=True)
    followers_serializer = FollowSerializer(followers, many=True)


    return Response({
        "followings": followings_serializer.data,
        "followers": followers_serializer.data,
        "followings_num": len(followings_serializer.data),
        "followers_num": len(followers_serializer.data),
        "flag": flag,
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_change(request, user_id):
    # 팔로우 받는 사람
    you = get_object_or_404(get_user_model(), id=user_id)
    me = request.user
    
    # 나 자신은 팔로우 할 수 없다.
    if you != me:
        if you.followers.filter(id=me.id).exists():
            # 팔로우 끊음
            you.followers.remove(me)
        else:
            # 팔로우 신청
            you.followers.add(me)

    followings = you.followings.all()
    followers = you.followers.all()
    followings_serializer = FollowSerializer(followings, many=True)
    followers_serializer = FollowSerializer(followers, many=True)

    return Response({
        "followings": followings_serializer.data,
        "followers": followers_serializer.data,
        "followings_num": len(followings_serializer.data),
        "followers_num": len(followers_serializer.data),
        }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def password(request):
    password = request.data.get("password")
    newPassword = request.data.get("newPassword")

    # 현재 패스워드 입력한 것이 맞는지 검증하기
    if check_password(password, request.user.password):
        request.user.set_password(newPassword)
        request.user.save()
        return Response({"message": 1}, status=status.HTTP_200_OK)
    # 잘못된 현재 패스워드 입력
    else:
        return Response({"message": "현재 비밀번호가 틀렸습니다."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    password = request.data.get("password")
    # 현재 패스워드 입력한 것이 맞는지 검증하기
    if check_password(password, request.user.password):
        request.user.delete()
        return Response({"message": 1}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_200_OK)
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import SignUpSerializer, UserActivationSerializer, LoginSerializer, UserProfileSerializer, UserManageSerializer
from .serializers import UsersListAPI
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema
from django.db.models import Q


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @extend_schema(
            summary="Registration",
            description="This endpoint allows you to register by providing email, username and password",
    )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verification')
        abs_url = 'http://'+current_site+relative_link+"?token="+str(token)
        subject = 'Verify your email'
        message = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + abs_url
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(APIView):
    serializer_class = UserActivationSerializer

    @extend_schema(
            summary="Email Verification",
            description="This endpoint allows user to activate their account using the token sent by email",
    )

    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
            summary="Login",
            description="This endpoint allows users to post their username and password and get access token for logging in",
    )

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified, please activate')

        return Response(
            {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens()
            }, status=status.HTTP_200_OK
        )


class UsersListAPIView(APIView):
    serializer_class = UsersListAPI
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Displaying total list of users",
            description="This endpoint allows you to get information about total list of users",
    )
    def get(self, request, *args, **kwargs):
        # Get the search query parameter from the request
        search_query = request.query_params.get('search', None)

        if search_query:
            # Filter recipes based on search query
            users = User.objects.filter(
                Q(username__icontains=search_query)
            )
        else:
            # If no search query provided, return all recipes
            users = User.objects.all()

        users_api = self.serializer_class(users, many=True)
        content = {"Users": users_api.data}
        return Response(content, status=status.HTTP_200_OK)


class ProfileShowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Displaying profile of the chosen user",
        description="This endpoint allows you to get detailed information about the profile of the users by their id",
    )
    def get(self, request, *args, **kwargs):
        try:
            profile = User.objects.get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response({'data': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        profile_api = UserProfileSerializer(profile)
        content = {"Profile Info": profile_api.data}
        return Response(content, status=status.HTTP_200_OK)


class MyPageShowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Displaying my-page of the user",
            description="This endpoint allows you to get detailed information about the my-page of the user",
    )
    def get(self, request, *args, **kwargs):
        try:
            profile = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({'data': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        profile_api = UserProfileSerializer(profile)
        content = {"Profile Info": profile_api.data}
        return Response(content, status=status.HTTP_200_OK)


class MyPageManageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Managing and editing user profile",
            description="This endpoint allows you to edit and manage your user profile",
    )
    def post(self, request, *args, **kwargs):
        try:
            profile = User.objects.all().get(id=request.user.id)
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserManageSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Profile has been edited successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors, "message": "There is an error"},
                        status=status.HTTP_400_BAD_REQUEST)


class ProfileFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Posts when current user follows the another user",
            description="This endpoint is used for posting when the current user follows the another user",
    )
    def post(self, request, *args, **kwargs):
        try:
            following_user = User.objects.all().get(id=kwargs['pk'])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

        follower = request.user

        if follower == following_user:
            return Response({"message": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if follower in following_user.followers.all():
            return Response({"message": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        following_user.followers.add(follower)
        follower.following.add(following_user)

        return Response({"message": "You are now following this user"}, status=status.HTTP_201_CREATED)


class ProfileUnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Posts when current user unfollows the another user",
            description="This endpoint is used for posting when the current user unfollows the another user",
    )
    def post(self, request, *args, **kwargs):
        try:
            following_user = User.objects.all().get(id=kwargs['pk'])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

        follower = request.user

        if follower not in following_user.followers.all():
            return Response({"message": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)

        following_user.followers.remove(follower)
        follower.following.remove(following_user)

        return Response({"message": "You have unfollowed this user"}, status=status.HTTP_200_OK)




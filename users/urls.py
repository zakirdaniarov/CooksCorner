from django.urls import path
from .views import RegisterAPIView, EmailVerificationAPIView, LoginAPIView, ProfileShowAPIView, ProfileFollowAPIView
from .views import MyPageShowAPIView, MyPageManageAPIView, ProfileUnfollowAPIView, UsersListAPIView, ResendActivationEmailAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('resend-activation-email/', ResendActivationEmailAPIView.as_view(), name='resend_activation_email'),
    path('email-activate/', EmailVerificationAPIView.as_view(), name='email-verification'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('', UsersListAPIView.as_view(), name='users_list'),
    path('<int:pk>/show/', ProfileShowAPIView.as_view(), name='profile_show'),
    path('my-page/', MyPageShowAPIView.as_view(), name='my_page'),
    path('my-page/manage/', MyPageManageAPIView.as_view(), name='profile_manage'),
    path('<int:pk>/follow/', ProfileFollowAPIView.as_view(), name='profile_follow'),
    path('<int:pk>/unfollow/', ProfileUnfollowAPIView.as_view(), name='profile_unfollow'),
]

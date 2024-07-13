# users/urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),  # Add home URL
    path('api/csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('users/', views.user_list, name='user-list'),
    path('interests/', views.InterestViewSet.as_view({'get': 'list', 'post': 'create'}), name='interest-list'),
    path('interests/<int:pk>/', views.InterestViewSet.as_view({'put': 'update'}), name='interest-detail'),
    path('interests/<int:pk>/accept/', views.InterestViewSet.as_view({'post': 'accept'}), name='interest-accept'),
    path('interests/<int:pk>/reject/', views.InterestViewSet.as_view({'post': 'reject'}), name='interest-reject'),
    path('chats/', views.ChatViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', views.Registration.as_view(), name='register'),

    # Login
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:id>', views.UserDetail.as_view(), name='user'),
]

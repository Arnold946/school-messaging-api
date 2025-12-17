from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from accounts.views.user import UserViewSet
from accounts.views.auth import CustomTokenObtainPairView, ChangePasswordView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [

    # ------------------------------
    # JWT AUTHENTICATION ENDPOINTS
    # ------------------------------
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='jwt-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # ------------------------------
    # USER CRUD (ViewSet)
    # ------------------------------
    path('', include(router.urls)),
]


from django.urls import path
from .views import RegisterAPIView
from .views import RegisterAPIView, ProfileAPIView,AdminDashboardAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/profile/', ProfileAPIView.as_view(), name='profile'),
    path('admin/dashboard/', AdminDashboardAPIView.as_view(), name='admin-dashboard'),
]

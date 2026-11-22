from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from accounts.permissions import IsAdminRole

# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminRole]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductSerializer
from accounts.permissions import IsAdminRole

# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    
class ProductListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    filter_backends = [SearchFilter]
    search_fields = ['name', 'sku', 'description']

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_active=True
        ).order_by('-created_at')

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminRole]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and (
            user.role == 'ADMIN' or user.is_superuser
        ):
            return Product.objects.all()

        return Product.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminRole]

        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])



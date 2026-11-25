from django.urls import path
from .views import CartDetailAPIView, AddToCartAPIView

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/items/', AddToCartAPIView.as_view(), name='add-to-cart'),
]
from django.urls import path
from .views import CartDetailAPIView, AddToCartAPIView, UpdateCartItemAPIView, DeleteCartItemAPIView

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/items/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/items/<int:pk>/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    path('cart/items/<int:pk>/delete/', DeleteCartItemAPIView.as_view(), name='delete-cart-item'),
]
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import CartItem
from .serializers import AddToCartSerializer
from .serializers import UpdateCartItemSerializer

from .models import Cart
from .serializers import CartSerializer

# Create your views here.

class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )
        return cart

class AddToCartAPIView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not item_created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {
                        'message': 'Not enough stock available.',
                        'available_stock': product.stock,
                        'current_cart_quantity': cart_item.quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            {
                'message': 'Product added to cart successfully.',
                'product': product.name,
                'sku': product.sku,
                'quantity': cart_item.quantity
            },
            status=status.HTTP_201_CREATED
        )

class UpdateCartItemAPIView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'head', 'options']

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
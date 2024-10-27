from .serializers import BookSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render
from rest_framework import viewsets, permissions
from product_catalog.models import Book
from order.models import Order, OrderItem
from rest_framework.generics import ListAPIView
from rest_framework.views import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class UserOrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        queryset = Order.objects.filter(customer__user__id=user_id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

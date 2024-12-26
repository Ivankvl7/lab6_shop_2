import json

from .serializers import BookSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render
from rest_framework import viewsets, permissions
from product_catalog.models import Book
from order.models import Order, OrderItem
from rest_framework import generics
from rest_framework.views import Response
from lab6_shop.settings import redis
from rest_framework import generics, permissions

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAdminUser,)



class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        queryset = Order.objects.filter(customer__user__id=user_id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class CartListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = redis.hgetall('user_cart')
        if queryset:
            queryset = {key.decode(): val.decode() for key, val in queryset.items()}
        else:
            queryset = {}
        return Response(json.dumps(queryset), status=200)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        queryset = redis.hget('user_cart', user_id)
        if queryset:
            queryset = [book_id for book_id in json.loads(queryset.decode())]
        else:
            queryset = []
        return Response(json.dumps(queryset), status=200)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        book_id = kwargs.get('book_id')

        user_cart_redis = redis.hget('user_cart', user_id)
        if not user_cart_redis:
            user_cart = []
        else:
            user_cart = json.loads(user_cart_redis.decode())
        user_cart.append(book_id)
        updated_cart = json.dumps(user_cart)
        redis.hset('user_cart', user_id, updated_cart)
        return Response(updated_cart, status=201)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        redis.hdel('user_cart', user_id)
        return Response(status=204)


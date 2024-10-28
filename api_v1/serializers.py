from django.contrib.auth.models import Group, User
from rest_framework import serializers
from product_catalog.models import Book
from order.models import Order, OrderItem


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'stock', 'isbn', 'publication_date']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(many=True, source='items', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'status', 'total_price', 'ordered_items']

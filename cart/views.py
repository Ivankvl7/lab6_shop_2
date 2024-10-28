import json

from collections import defaultdict
from .models import CartItem
from django.shortcuts import redirect
from django.views.generic import ListView

from lab6_shop.settings import redis
from product_catalog.models import Book


def get_cart_items(user_id):
    res = []
    items = defaultdict(int)
    user_cart = redis.hget('user_cart', user_id)
    # print(f"user_cart = {user_cart}")
    if user_cart is not None:
        user_cart = json.loads(user_cart.decode())
        for index, item_id in enumerate(user_cart):
            items[item_id] = items[item_id] + 1
            # print(f"items={items}")
        for item_id, quantity in items.items():
            book = Book.objects.get(pk=item_id)
            res.append(CartItem(book=book, quantity=items[item_id]))

    print(f"res in get_cart_items = {res}")
    return res

def get_total_price(user_id):
    items = get_cart_items(user_id)
    total_price = 0
    for item in items:
        total_price += (item.quantity * item.book.price)
    return total_price

class CartListView(ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'
    paginate_by = 5

    def get_queryset(self):
        user_id = self.request.user.id
        res = get_cart_items(user_id)
        print(f"query_set = {res}")
        return res

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Bookstore'
        context['total_price'] = get_total_price(user_id)
        return context


def add_to_cart(request, user_id, book_id):
    # по id юзера достаем id книг из корзины
    user_cart_redis = redis.hget('user_cart', user_id)
    if not user_cart_redis:
        user_cart = []
    else:
        user_cart = json.loads(user_cart_redis.decode())
    user_cart.append(book_id)
    redis.hset('user_cart', user_id, json.dumps(user_cart))
    return redirect('cart_detail', user_id=user_id)


def delete_from_cart(request, user_id, book_id):
    user_cart = redis.hget('user_cart', user_id)
    if user_cart is not None:
        user_cart = json.loads(user_cart.decode())
    else:
        user_cart = []
    if user_cart:
        for index, item in enumerate(user_cart):
            if item == book_id:
                user_cart.pop(index)
                break
    redis.hset('user_cart', user_id, json.dumps(user_cart))
    return redirect('cart_detail', user_id=user_id)

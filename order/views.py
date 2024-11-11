import requests

from .models import OrderItem, Order
from accounts.models import Profile

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cart.views import get_cart_items
from django.db.models import Max
from django.views.generic import ListView, View
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from cart.views import get_cart_items
from lab6_shop.settings import redis


class OrderPaymentView(View):
    @staticmethod
    def get_order_info(user_id):
        cart_items = get_cart_items(user_id)
        total_price = 0
        new_order = Order(
            customer=Profile.objects.get(user__id=user_id),
            created_at=timezone.now(),
            total_price=total_price
        )
        order_items = []
        for item in cart_items:
            total_price += item.book.price * item.quantity
            order_item = OrderItem(order=new_order, book=item.book, quantity=item.quantity,
                                   price=item.quantity * item.book.price
            )
            order_items.append(order_item)
        return total_price, new_order, order_items

    def post(self, request, *args, **kwargs):

        user_id = kwargs.get('user_id')
        total_price, new_order, order_items = self.get_order_info(user_id)

        # Формируем данные для POST запроса
        data = {
            'user_slug': Profile.objects.filter(user__pk=user_id)[0].slug,
            'total_price': float(total_price),
        }
        message = 'Payment failed. Insufficient funds. Please try again.'

        try:
            response = requests.post('http://localhost:8080/api/v1/payment/', json=data)

            # !!!
            print(response.status_code)
            # Обрабатываем ответ
            if response.status_code == 200:
                # сохраняем заказ
                new_order.total_price = total_price
                new_order.save()

                for item in order_items:
                    item.save()
                redis.hdel('user_cart', user_id)
                return HttpResponseRedirect(reverse('order_history', kwargs={'user_id': user_id}))

            else:
                return render(request, 'cart/cart.html',
                              {'user_id': user_id, 'message': message, 'cart_items': get_cart_items(user_id)})
        except Exception:
            # messages.error(request, 'Payment failed. Please try again.')
            return render(request, 'cart/cart.html',
                          {'user_id': user_id, 'message': "Ошибка выполнение запроса", 'cart_items': get_cart_items(user_id)})


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        # print(user_id)
        profile = Profile.objects.get(user__id=user_id)
        return Order.objects.filter(customer=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Orders'
        return context

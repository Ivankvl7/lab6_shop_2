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


class OrderPaymentView(View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

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
            order_item = OrderItem(
                order=new_order,
                book=item.book,
                quantity=item.quantity,
                price=item.quantity * item.book.price
            )
            order_items.append(order_item)


        # Формируем данные для POST запроса
        data = {
            'user_slug': Profile.objects.filter(user__pk=user_id)[0].slug,
            'total_price': float(total_price),
        }
        message = 'Payment failed. Insufficient funds. Please try again.'

        try:
            response = requests.post('http://localhost:8080/api/v1/payment_proceed', json=data)
            print(response)

            # Обрабатываем ответ
            if response.status_code == 200:
                # сохраняем заказ
                new_order.total_price = total_price
                new_order.save()

                for item in order_items:
                    item.save()
                return HttpResponseRedirect(reverse('order_list', kwargs={'user_id': user_id}))

            else:
                return render(request, 'cart/cart.html', {'user_id': user_id, 'message': message, 'cart_items': get_cart_items(user_id)})
        except Exception:
            # messages.error(request, 'Payment failed. Please try again.')
            return render(request, 'cart/cart.html', {'user_id': user_id, 'message': message, 'cart_items': get_cart_items(user_id)})


def order_payment(request):
    user_id = request.user.id
    cart_items = get_cart_items(user_id)
    total_price = 0
    for item in cart_items:
        total_price += item.book.price * item.quantity

    max_id = Order.objects.aggregate(Max('id'))['id__max']

    # Если записи нет (max_id равен None), начинаем с 1
    if max_id is None:
        max_id = 1
    else:
        max_id += 1

    new_order = Order(customer=Profile.objects.get(user__id=user_id), total_price=total_price)
    new_order.save()


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'  # Укажите шаблон для отображения заказов
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        print(user_id)
        profile = Profile.objects.get(user__id=user_id)
        return Order.objects.filter(customer=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Orders'
        return context

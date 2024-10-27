from django.urls import path
from django.http import HttpResponse
from order.views import  OrderListView, OrderPaymentView


urlpatterns = [
    path('order_payment/<int:user_id>/', OrderPaymentView.as_view(), name='order_payment'),
    path('order_history/<int:user_id>/', OrderListView.as_view(), name='order_history')
]
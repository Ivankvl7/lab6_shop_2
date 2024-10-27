from django.urls import path
from django.http import HttpResponse
from cart.views import add_to_cart, CartListView, delete_from_cart


urlpatterns = [
    # передаем user_id в качестве pk
    path('cart_detail/<int:user_id>/', CartListView.as_view(), name='cart_detail'),

    # 1 - user_id, 2 - item_id
    path('add_to_cart/<int:user_id>/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove_item/<int:user_id>/<int:book_id>/', delete_from_cart, name='remove_item'),
]
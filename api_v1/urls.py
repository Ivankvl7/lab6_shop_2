from django.urls import include, path
from rest_framework import routers

from api_v1 import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book'),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:user_id>/', views.UserOrderListView.as_view())
]

from django.urls import include, path
from rest_framework import routers

from api_v1 import views


router = routers.DefaultRouter()
router.register(r'books', viewset=views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:user_id>/', views.UserOrderListView.as_view())
]

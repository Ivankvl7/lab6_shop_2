from django.urls import path
from product_catalog.views import CatalogListView, CatalogBookDetail


urlpatterns = [
    path('', CatalogListView.as_view(), name='home'),
    path('book/<int:pk>/', CatalogBookDetail.as_view(), name='book_detail')
]
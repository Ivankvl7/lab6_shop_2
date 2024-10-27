from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from product_catalog.models import Book


class CatalogListView(ListView):
    model = Book
    template_name = 'product_catalog/catalog_list.html'
    context_object_name = 'books'
    queryset = Book.objects.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Bookstore'
        return context

class CatalogBookDetail(DetailView):
    model = Book
    template_name = 'product_catalog/book_detail.html'
    context_object_name = 'book'

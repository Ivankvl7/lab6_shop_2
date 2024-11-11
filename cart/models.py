from django.db import models
from product_catalog.models import Book
from accounts.models import Profile


class CartItem(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in cart"

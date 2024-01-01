from django.db import models
from books.models import Book
from django.contrib.auth.models import User
# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    # bank = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='bankinfo')
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total_price before saving
        self.total_price = self.product.borrowing_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
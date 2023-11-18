from django.db import models
from django.contrib.auth.models import User
from item.models import Item

# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(User, related_name='wallet', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        buyer_wallet = Wallet.objects.get(user=self.buyer)
        seller_wallet = Wallet.objects.get(user=self.seller)
        
        buyer_wallet.balance -= self.amount
        seller_wallet.balance += self.amount
        
        buyer_wallet.save()
        seller_wallet.save()
        
        super(Transaction, self).save(*args, **kwargs)
 
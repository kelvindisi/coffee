from django.db import models
from account.models import UserModel
from staff.models import Factory


class NotificationMessage(models.Model):
    farmer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300, verbose_name="title")
    message = models.TextField(verbose_name="body")
    sender = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="message_sender")

    def __str__(self):
        return f"{self.farmer.username} Message"


class Product(models.Model):
    scheduler = [
        ('0', 'No'),
        ('1', 'Yes'),
        ('2', 'Pending')
    ]
    collected = [
        ('0', 'No'),
        ('1', 'Yes')
    ]

    farmer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    approximate_quantity = models.IntegerField(default=0)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name="coffee")
    price_per_kg = models.IntegerField(default=0, verbose_name="price")
    date = models.DateField(auto_now_add=True)
    scheduled = models.CharField(max_length=2, choices=scheduler, default='2')
    date_scheduled = models.DateField(null=True)
    collected = models.CharField(max_length=2, choices=collected, default='0')

    def __str__(self):
        return f"{self.farmer.username} - {self.quantity}Kgs"


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.id} {self.total_amount}"


class Transaction(models.Model):
    transaction_types = [
        ('deposit', 'Deposit'),
        ('cancel', 'Cancel'),
        ('correction', 'Correction')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    initiated_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="accountant")
    transaction_type = models.CharField(
        max_length=20, choices=transaction_types)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.transaction_type}"

    def get_absolute_url(self):
        pass

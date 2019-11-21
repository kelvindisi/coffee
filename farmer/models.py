from django.db import models
from django.contrib.auth.models import User
from staff.models import Factory


class NotificationMessage(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300, verbose_name="title")
    message = models.TextField(verbose_name="body")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_sender")

    def __str__(self):
        return f"{self.farmer.username} Message"


class Product(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name="coffee")
    price_per_kg = models.IntegerField(default=0, verbose_name="price")
    date_delivered = models.DateField()
    factory = models.OneToOneField(Factory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.farmer.username} - {self.quantity}Kgs"

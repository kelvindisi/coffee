from django.db import models
from django.urls import reverse
from account.models import UserModel


class Factory(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    date_registered = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('staff:factories')

    def __str__(self):
        return f"{self.name} - {self.email}"


class FactoryPrice(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    previous_price = models.IntegerField(default=None, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.factory.name} - {self.price}"


class FactoryStaff(models.Model):
    staff = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)

    def __str__(self):
        return f"STAFF ID: {self.staff.username} -IN- {self.factory.name}"


class Account(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance}"
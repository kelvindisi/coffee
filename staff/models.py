from django.db import models
from django.urls import reverse


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

from django.urls import path
from . import views

app_name = "farmer"

urlpatterns = [
    path('', views.index, name="index"),
    path('factories/', views.factories, name="factories")
]

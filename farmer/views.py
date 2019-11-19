from django.shortcuts import render
from django.views import generic

def index(request):
    return render(request, 'farmer/home.html')

def factories(request):
    return render(request, 'farmer/factories.html')
from django.shortcuts import render


def index(request):
    return render(request, 'farmer/home.html')

from django.urls import path
from . import views
from django.contrib.auth import views as authView

app_name = 'user'

urlpatterns = [
    path('', authView.LoginView.as_view(), name="login"),
    path('register/', views.CreateAccountView.as_view(), name="register"),
    path('logout/', authView.LogoutView.as_view(), name="logout")
]

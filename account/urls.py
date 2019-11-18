from django.urls import path
from . import views
from django.contrib.auth import views as authView

app_name = 'account'

urlpatterns = [
    path('', authView.LoginView.as_view(
        template_name="account/login.html"), name="login"),
    path('register/', views.CreateAccountView.as_view(), name="register"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('logout/', authView.LogoutView.as_view(), name="logout")
]

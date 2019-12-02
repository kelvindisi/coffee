from django.urls import path
from . import views

app_name = "farmer"

urlpatterns = [
    path('', views.HomePageView.as_view(), name="index"),
    path('factories/', views.FactoryList.as_view(), name="factories"),
    path('product/', views.CreateCollectionScheduler.as_view(), name='product'),
    path('schedules/', views.ScheduleList.as_view(), name='schedules'),
    path('pending_payment/', views.PendingPayment.as_view(), name="pending_payment"),
    path('payment_history/', views.PaymentHistory.as_view(), name="payment_history")
]
